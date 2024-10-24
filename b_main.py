import os, time
from print_tricks import pt
from rich import print as rprint

from b_find_seasons import find_seasons, print_series
from b_process_videos import process_videos
from b_compile_vids import compile_videos_from_dict
from b_sort_data import sort_data
from b_merge_data import get_merged_data
from merge_extras import merge_extras_into_sequences
from merge_remaining_sequences import merge_all_sequences
from utilities import add_to_hashes_db

def debug_print(
    video_hashes, 
    conflicting_frame_hashes, 
    sorted_data, 
    merged, 
    extras, 
    merged_w_extras, 
    new_extras, 
    possible_conflicting_sequences, 
    test_full_vids=False
):
    data_labels = [
        ("video hashes", video_hashes),
        ("conflicting frame hashes", conflicting_frame_hashes),
        ("sorted data", sorted_data),
        ("merged", merged),
        ("extras", extras),
        ("merged with extras", merged_w_extras),
        ("new extras", new_extras),
        ("possible conflicting sequences", possible_conflicting_sequences),
    ]
    
    if test_full_vids:
        with open('log.txt', 'w') as log_file:
            for label, data in data_labels:
                print(f'\n{label}:\n', file=log_file)
                print(data, file=log_file)
    else:
        for label, data in data_labels:
            rprint(f'\n{label}:\n', data)

def process_series(series, test_full_vids=False, db_path='hashes.db'):
    frame_hashes = {}
    conflicting_frame_hashes = {}
    
    for series_name, seasons in series.items():
        for season, video_paths in seasons.items():
            
            pt.t()
            
            pt(video_paths)
            use_disk = True
            
            ## TEST TEMP DELET TODO ##
            ## if database already exists, delete it. 
            if os.path.exists(db_path):
                os.remove(db_path)
                time.sleep(0.1)
                pt('deleted database!')
                
            ## process videos
            video_hashes, conflicting_frame_hashes = process_videos(
                frame_hashes, conflicting_frame_hashes, video_paths, use_disk=use_disk, db_path=db_path)
            
            sorted_data = sort_data(conflicting_frame_hashes)
            merged, extras = get_merged_data(sorted_data)
            merged_w_extras, new_extras = merge_extras_into_sequences(merged, extras)
            possible_conflicting_sequences = merge_all_sequences(merged_w_extras)
            
            
            
            add_to_hashes_db(possible_conflicting_sequences, db_path)
            
            debug_print(
                video_hashes, 
                conflicting_frame_hashes, 
                sorted_data, 
                merged,
                extras,
                merged_w_extras,
                new_extras,
                possible_conflicting_sequences, 
                test_full_vids
            )
            # pt.ex()
            compile_videos_from_dict(possible_conflicting_sequences, video_paths, per_sequence=False)
            
            pt.t()

if __name__ == "__main__":
    
    test_full_vids = False
    if test_full_vids:
        series_path = fr'C:\Users\user\Downloads\_Tor\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\_vids_for_python_automatic_editing'
        db_path = 'hashes_full_vids.db'
    else:
        # series_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_tiny_videos_for_testing', 'compiled')
        main_folder = 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\'
        series_path = os.path.join(main_folder, '1_clips_to_build_vids')

        db_path = 'hashes_tiny_vids.db'
        
    series = find_seasons(series_path)
    pt(series)
    print_series(series)
    
    
    if series is not None:
        process_series(series, test_full_vids=test_full_vids, db_path=db_path)
    else:
        print("Error: find_seasons returned None. Please check the function implementation.")



'''















'''