import os, time
from print_tricks import pt
from rich import print as rprint

from b_find_seasons import find_seasons, print_series
from b_process_videos import process_videos
from b_compile_vids import extract_subclips, compile_originals_without_subclips
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
    test_full_vids=False,
    print_data=False,  # Controls printing of data structures
    print_key_totals=False,  # Controls printing of total items per key
    print_totals=False,  # Controls printing of total items
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
            def log_print(message):
                print(message, file=log_file)
            print_func = log_print
    else:
        print_func = rprint

    def print_dict_details(data, label, print_func):
        total_items = 0
        subkey_totals = {}

        for key, subdict in data.items():
            if isinstance(subdict, dict):
                sub_total = 0
                for subkey, items in subdict.items():
                    item_count = len(items)
                    sub_total += item_count
                    if print_data:
                        print_func(f'  {subkey}: {items} ({item_count} items)')
                    if print_key_totals:
                        subkey_totals[subkey] = subkey_totals.get(subkey, 0) + item_count
                if print_key_totals:
                    print_func(f'  Total in {key}: {sub_total} items')
                total_items += sub_total
            else:
                item_count = len(subdict)
                if print_data:
                    print_func(f'  {key}: {subdict} ({item_count} items)')
                total_items += item_count

        if print_totals:
            print_func(f'Total items in {label}: {total_items}')
        if print_key_totals:
            for subkey, total in subkey_totals.items():
                print_func(f'Total items in {label} {subkey}: {total} items')

    # Moved outside the `if print_data` block
    for label, data in data_labels:
        print_func(f'\n{label}:\n')
        if isinstance(data, dict):
            print_dict_details(data, label, print_func)
        else:
            if print_data:
                print_func(f'{label}: {data}')




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
                test_full_vids=False,
                print_data=False,
                print_key_totals=False,
                print_totals=True,
            )
            # pt.ex()
            # extract_subclips(possible_conflicting_sequences, video_paths, output_path=output_clips_path)
            # compile_originals_without_subclips(possible_conflicting_sequences, video_paths, output_path=output_full_vids_path)
            
            pt.t()






if __name__ == "__main__":
    
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




'''















'''