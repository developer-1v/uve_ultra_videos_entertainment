import os, time
from multiprocessing import Process

from print_tricks import pt
from rich import print as rprint

from gui import run as run_gui
from b_find_seasons import find_seasons, print_series
from b_process_videos import process_videos
from b_compile_vids import extract_subclips, compile_originals_without_subclips
from b_sort_data import sort_data
from b_merge_data import get_merged_data
from merge_extras import merge_extras_into_sequences
from merge_remaining_sequences import merge_all_sequences
from utilities import add_to_hashes_db
from debugging_module import debug_print
from simplify_sequences import simplify_sequences
from mark_videos import mark_videos, video_based_sequences_restructurer


def process_series(series, test_full_vids=False, db_path='hashes.db', output_clips_path='', output_full_vids_path=''):
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
            simplified_possible_conflicting_sequences, missing_frames = simplify_sequences(possible_conflicting_sequences)
            video_based_sequences = video_based_sequences_restructurer(simplified_possible_conflicting_sequences)
            # mark_videos(series, video_based_sequences)
            
            
            
            debug_print(
                video_hashes, 
                conflicting_frame_hashes, 
                sorted_data,
                merged,
                extras,
                merged_w_extras,
                new_extras,
                possible_conflicting_sequences,
                simplified_possible_conflicting_sequences,
                video_based_sequences,
                test_full_vids=False,
                print_data=False,
                print_key_totals=False,
                print_totals=True,
            )
            # pt.ex()
            # add_to_hashes_db(possible_conflicting_sequences, db_path)
            # extract_subclips(simplified_possible_conflicting_sequences, video_paths, output_path=output_clips_path)
            # compile_originals_without_subclips(possible_conflicting_sequences, video_paths, output_path=output_full_vids_path)
            
            pt.t()



def test_process_series():

    test_full_vids = False
    if test_full_vids:
        series_path = fr'C:\Users\user\Downloads\_Tor\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\_vids_for_python_automatic_editing'
        db_path = 'hashes_full_vids.db'
    else:
        main_folder = 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\'
        # series_path = os.path.join(main_folder, 'compiled_tiny_videos_for_testing', 'compiled')
        series_path = os.path.join(main_folder, 'tiny_vids','3_complete_vids_to_test')

        db_path = 'hashes_tiny_vids.db'
        
    series = find_seasons(series_path)
    pt(series)
    print_series(series)
    
    output_clips_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\4_clips_to_remove'
    output_full_vids_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\6_final_uve_edited_vids'
    if series is not None:
        process_series(series, test_full_vids=test_full_vids, db_path=db_path, output_clips_path=output_clips_path, output_full_vids_path=output_full_vids_path)
    else:
        print("Error: find_seasons returned None. Please check the function implementation.")


if __name__ == "__main__":
    gui_mode = False
    # gui_mode = input("Do you want to launch the GUI? (yes/no): ").lower() == 'yes'
    

    if gui_mode:
        gui_process = Process(target=run_gui)
        gui_process.start()
        processing_process = Process(target=test_process_series)
        processing_process.start()
    
    else:
        test_process_series()



'''















'''