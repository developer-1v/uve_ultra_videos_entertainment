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
            
            ## TEST
            ## if database already exists, delete it. 
            if os.path.exists(db_path):
                os.remove(db_path)
                time.sleep(0.1)
                pt('deleted database!')
                
            ## process videos
            video_hashes, conflicting_frame_hashes = process_videos(
                frame_hashes, conflicting_frame_hashes, video_paths, use_disk=use_disk, db_path=db_path)
            
            # print('conflicting_frame_hashes:')
            # rprint(conflicting_frame_hashes)
            
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
            pt.ex()
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


'''
providence milwaukie imaging
503-513-8350


from rich import print as rprint
from copy import deepcopy

def can_merge_sequences(seq1, seq2, key, max_gap):
    """Check if two sequences can be merged based on the given key and max_gap."""
    if not seq1[key] or not seq2[key]:  # Check if either sequence is empty
        return False  # Cannot merge if one of the sequences is empty

    last_num_seq1 = seq1[key][-1]
    first_num_seq2 = seq2[key][0]
    first_num_seq1 = seq1[key][0]
    last_num_seq2 = seq2[key][-1]

    # Check if seq1 can merge into seq2 or seq2 can merge into seq1
    return (last_num_seq1 + 1 <= first_num_seq2 <= last_num_seq1 + max_gap) or \
            (last_num_seq2 + 1 <= first_num_seq1 <= last_num_seq2 + max_gap)

def merge_sequences(seq1, seq2, key):
    """Merge two sequences ensuring numerical order and minimal disruption, and remove the merged data from the source."""
    if seq1[key][-1] < seq2[key][0]:  # seq1 ends before seq2 starts
        seq1[key].extend(seq2[key])
        seq2[key] = []  # Clear the data from seq2 after merging
    elif seq2[key][-1] < seq1[key][0]:  # seq2 ends before seq1 starts
        seq2[key].extend(seq1[key])
        seq1[key] = seq2[key]  # Move all to seq1
        seq2[key] = []  # Clear the original data from seq2
    else:  # Overlapping or touching sequences
        combined = sorted(set(seq1[key] + seq2[key]))  # Merge and sort to remove duplicates
        seq1[key] = combined
        seq2[key] = []  # Clear the data from seq2 after merging

def merge_all_sequences(sequences, max_gap=1):
    sequences = deepcopy(sequences)  # Deep copy to avoid modifying the original

    if isinstance(sequences, dict):
        sequences = list(sequences.values())

    keys = set(k for seq in sequences for k in seq.keys())
    for key in keys:
        sequences_copy = [seq.copy() for seq in sequences]  # Use deep copy to avoid modifying original during iteration

        i = 0
        while i < len(sequences_copy):
            if key in sequences_copy[i]:
                j = 0
                while j < len(sequences_copy):
                    if i != j and key in sequences_copy[j] and can_merge_sequences(sequences_copy[i], sequences_copy[j], key, max_gap):
                        # Decide which sequence to merge into based on length
                        if len(sequences_copy[i][key]) >= len(sequences_copy[j][key]):
                            merge_sequences(sequences[i], sequences[j], key)
                        else:
                            merge_sequences(sequences[j], sequences[i], key)
                        sequences_copy[j][key] = []  # Ensure the merged data is cleared
                        break
                    j += 1
            i += 1

        # Clean up sequences with no remaining keys under 'key'
        sequences = [seq for seq in sequences if any(seq.values())]

    labeled_sequences = {f'sequence {index}': seq for index, seq in enumerate(sequences)}
    return labeled_sequences


if __name__ == '__main__':
    # sequences = {
    #     "sequence 0": {
    #         "a": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    #         "b": [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
    #         "c": [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
    #     },
    #     "sequence 1": {
    #         "a": [23, 24, 25],
    #         "b": [4, 5, 6],
    #         "c": [42, 43, 44]
    #     },
    #     "sequence 2": {
    #         "a": [34, 35, 36],
    #         "b": [35, 36, 37],
    #         "c": [53, 54, 55]
    #     },
    #     "sequence 3": {
    #         "a": [26, 27, 28, 29],
    #         "b": [7, 8, 9],
    #         "c": [45, 46, 48]
    #     },
    #     "sequence 4": {
    #         "a": [37, 38, 39],
    #         "b": [38, 39, 40, 41]
    #     }
    # }

    # updated_extras = {
    #     "a": [91, 95],
    #     "b": [92, 96, 27, 30],
    #     "c": [59, 93, 98, 15, 18]
    # }

    sequences = {
        'sequence 0': {
            'compiled_tiny_original_15a.mkv': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            'compiled_tiny_original_15b.mkv': [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
            'compiled_tiny_original_15c.mkv': [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
        },
        'sequence 1': {'compiled_tiny_original_15a.mkv': [23, 24, 25, 26, 27, 28, 29, 30, 26, 27, 28, 29, 30], 'compiled_tiny_original_15b.mkv': [4, 5, 6, 7, 8, 9, 7, 8, 9], 'compiled_tiny_original_15c.mkv': [42, 43, 44, 45, 46, 45, 46]},
        'sequence 2': {'compiled_tiny_original_15a.mkv': [34, 35, 36, 37, 38, 39, 37, 38, 39], 'compiled_tiny_original_15b.mkv': [35, 36, 37, 38, 39, 40, 41, 42, 38, 39, 40, 41, 42], 'compiled_tiny_original_15c.mkv': [53, 54, 55, 56, 57, 56, 57]},
        'sequence 3': {},
        'sequence 4': {},
        'sequence 5': {'compiled_tiny_original_15b.mkv': [10, 11]}
    }
    extras = {'a': [91, 95], 'b': [92, 96, 27, 30], 'c': [59, 93, 98, 15, 18]}

    # Example usage:
    merged_sequences = merge_all_sequences(sequences)
    print('merged sequences:')
    rprint(merged_sequences)



'''