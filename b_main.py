import os, time
from print_tricks import pt
from rich import print as rprint

from b_find_seasons import find_seasons, print_series
from b_process_videos import process_videos
import b_calculate_sequences
from b_compile_vids import compile_videos_from_dict
from utilities import add_to_hashes_db

def debug_print(video_hashes, conflicting_frame_hashes, possible_conflicting_sequences, test_full_vids=False):
    if test_full_vids:
        with open('log.txt', 'w') as log_file:
            print('video hashes:\n\n', file=log_file)
            print(video_hashes, file=log_file)
            print('conflicting frame hashes:\n\n', file=log_file)
            print(conflicting_frame_hashes, file=log_file)
            print('possible conflicting sequences:\n\n', file=log_file)
            print(possible_conflicting_sequences, file=log_file)
            
    else:
        rprint('video hashes:\n\n', video_hashes)
        rprint('conflicting frame hashes:\n\n', conflicting_frame_hashes)
        rprint('possible conflicting sequences:\n\n', possible_conflicting_sequences)
    
    pt.ex()

def process_series(series, test_full_vids=False, db_path='hashes.db'):
    frame_hashes = {}
    conflicting_frame_hashes = {}
    
    for series_name, seasons in series.items():
        for season, video_paths in seasons.items():
            
            pt.t()
            
            pt(video_paths)
            use_disk = True
            
            ## TEST
            ## if database already exists, delete it. 
            if os.path.exists(db_path):
                os.remove(db_path)
                time.sleep(0.1)
                pt('deleted database!')
                
            ## process videos
            video_hashes, conflicting_frame_hashes = process_videos(
                frame_hashes, conflicting_frame_hashes, video_paths, use_disk=use_disk, db_path=db_path)
            
            possible_conflicting_sequences = b_calculate_sequences.find_possible_sequences(conflicting_frame_hashes)
            
            add_to_hashes_db(possible_conflicting_sequences, db_path)
            
            debug_print(video_hashes, conflicting_frame_hashes, possible_conflicting_sequences, test_full_vids)
            
            compile_videos_from_dict(possible_conflicting_sequences, video_paths, per_sequence=False)
            
            pt.t()

if __name__ == "__main__":
    
    test_full_vids = False
    if test_full_vids:
        series_path = fr'C:\Users\user\Downloads\_Tor\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\_vids_for_python_automatic_editing'
        db_path = 'hashes_full_vids.db'
    else:
        series_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_tiny_videos_for_testing', 'compiled')
        db_path = 'hashes_tiny_vids.db'
        
    series = find_seasons(series_path)
    pt(series)
    print_series(series)
    
    
    if series is not None:
        process_series(series, test_full_vids=test_full_vids, db_path=db_path)
    else:
        print("Error: find_seasons returned None. Please check the function implementation.")
    

# {'compiled': {'compiled': ['C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15a_normal.mkv',
# 'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15b_reverse.mkv']}}

# ['C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15a_normal.mkv',
# 'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15b_reverse.mkv']