from rich.pretty import pprint
from rich import print as rprint
from print_tricks import pt




def sort_data(input_data):
    pt(input_data)
    # Initialize sorted_data with keys from input_data
    sorted_data = {key: [] for key in input_data[next(iter(input_data))]}
    
    # Collect all frames
    frames = []
    for key in input_data:
        frames.append(tuple(input_data[key][sub_key] for sub_key in input_data[key]))
    
    pt(frames)
    # Sort frames by the first element of the first key to maintain order
    frames.sort(key=lambda x: x[0][0] if x[0] else float('inf'))
    pt(frames)
    
    # Find sorted data
    for frame in frames:
        for sub_key, seq in zip(sorted_data.keys(), frame):
            sequence = []
            last_num = None
            
            for num in seq:
                if last_num is not None and num != last_num + 1:
                    sorted_data[sub_key].append(sequence)
                    sequence = []
                sequence.append(num)
                last_num = num
            
            # Append the last sequence
            if sequence:
                sorted_data[sub_key].append(sequence)
    
    return sorted_data


def merge_and_extract_extras(data):
    merged = {}
    extras = {key: [] for key in data}
    sequence_count = 0

    # Initialize pointers for each key
    pointers = {key: 0 for key in data}
    max_length = max(len(data[key]) for key in data)

    while any(pointers[key] < len(data[key]) for key in data):
        current_sequence = {key: [] for key in data}
        min_start = None

        # Determine the minimum start value for the next sequence
        for key in data:
            if pointers[key] < len(data[key]):
                if min_start is None or data[key][pointers[key]][0] < min_start:
                    min_start = data[key][pointers[key]][0]

        # Build sequences starting from the minimum start value
        for key in data:
            while pointers[key] < len(data[key]) and (not current_sequence[key] or data[key][pointers[key]][0] == current_sequence[key][-1] + 1):
                current_sequence[key].extend(data[key][pointers[key]])
                pointers[key] += 1

        # Store the sequences or move to extras if only one frame
        for key in current_sequence:
            if len(current_sequence[key]) > 1:
                if f"sequence {sequence_count}" not in merged:
                    merged[f"sequence {sequence_count}"] = {}
                merged[f"sequence {sequence_count}"][key] = current_sequence[key]
            elif current_sequence[key]:
                extras[key].extend(current_sequence[key])

        if any(len(current_sequence[key]) > 1 for key in current_sequence):
            sequence_count += 1

    return merged, extras



def find_possible_sequences(conflicting_frame_hashes, max_gap=1):
    
    sorted_data = sort_data(conflicting_frame_hashes)
    merged, extras = merge_and_extract_extras(sorted_data)
    pt(sorted_data)
    pt(merged)
    pt(extras)
    # frame_matches = get_frame_matches(conflicting_frame_hashes)
    # pprint('frame_matches:')
    # pprint(frame_matches)

    # video_names = extract_video_names(conflicting_frame_hashes)
    # sequences = identify_continuous_sequences(conflicting_frame_hashes, max_gap)
    # possible_sequences = reorganize_sequences(sequences)

    # pprint('possible_sequences:')
    # pprint(possible_sequences)
    # pt()
    return merged, extras
    


if __name__ == "__main__":
    # conflicting_frame_hashes = {
    #     '0000003010000000': {'tiny_compiled_15a_normal.mkv': [8], 'tiny_compiled_15b_reverse.mkv': [29]},
    #     '0000409090848682': {'tiny_compiled_15a_normal.mkv': [9], 'tiny_compiled_15b_reverse.mkv': [30]},
    #     '0040c09090848686': {'tiny_compiled_15a_normal.mkv': [10], 'tiny_compiled_15b_reverse.mkv': [31]},
    #     '4040c09094848686': {'tiny_compiled_15a_normal.mkv': [11], 'tiny_compiled_15b_reverse.mkv': [32]},
    #     '4004c49094868686': {'tiny_compiled_15a_normal.mkv': [12], 'tiny_compiled_15b_reverse.mkv': [33]},
    #     'c8d4c4d49486c686': {'tiny_compiled_15a_normal.mkv': [14, 15], 'tiny_compiled_15b_reverse.mkv': [35, 36]},
    #     'd9d1c5d49486c696': {'tiny_compiled_15a_normal.mkv': [16], 'tiny_compiled_15b_reverse.mkv': [37]},
    #     'd9d5c5d49486c696': {'tiny_compiled_15a_normal.mkv': [17], 'tiny_compiled_15b_reverse.mkv': [38]},
    #     'd8d5c5d49486c696': {'tiny_compiled_15a_normal.mkv': [18, 20, 21], 'tiny_compiled_15b_reverse.mkv': [39, 41, 42]},
    #     'd8d5cdd49486c696': {'tiny_compiled_15a_normal.mkv': [19], 'tiny_compiled_15b_reverse.mkv': [40]},
    #     '1119999494849696': {'tiny_compiled_15a_normal.mkv': [22], 'tiny_compiled_15b_reverse.mkv': [43]},
    #     '7619a4cc4dc3788c': {'tiny_compiled_15a_normal.mkv': [28], 'tiny_compiled_15b_reverse.mkv': [10]},
    #     '7691644c4dcb788c': {'tiny_compiled_15a_normal.mkv': [29, 30, 31], 'tiny_compiled_15b_reverse.mkv': [11, 12, 13]},
    #     '7691654c4dcb788c': {'tiny_compiled_15a_normal.mkv': [32, 33, 34, 35, 36, 37, 38], 'tiny_compiled_15b_reverse.mkv': [14, 15, 16, 17, 18, 19, 20, 21]},
    #     '7691654c4dcb780c': {'tiny_compiled_15a_normal.mkv': [39, 40], 'tiny_compiled_15b_reverse.mkv': [22]}
    # }




    conflicting_frame_hashes = {
        '7619a4cc4dc3788c': {'compiled_tiny_original_15a.mkv': [6], 'compiled_tiny_original_15b.mkv': [47], 'compiled_tiny_original_15c.mkv': [25]},
        '7691644c4dcb788c': {'compiled_tiny_original_15a.mkv': [7, 8, 9], 'compiled_tiny_original_15b.mkv': [48, 49, 50], 'compiled_tiny_original_15c.mkv': [26, 27, 28]},
        '7691654c4dcb788c': {'compiled_tiny_original_15a.mkv': [10, 11, 12, 13, 14, 15], 'compiled_tiny_original_15b.mkv': [51, 52, 53, 54, 55, 56, 57, 58], 'compiled_tiny_original_15c.mkv': [29, 30, 31, 32, 33, 34]},
        '7691654c4dcb780c': {'compiled_tiny_original_15a.mkv': [16, 17, 18], 'compiled_tiny_original_15b.mkv': [59], 'compiled_tiny_original_15c.mkv': [35, 36, 37]},
        '24010080808582cb': {'compiled_tiny_original_15a.mkv': [23, 34], 'compiled_tiny_original_15b.mkv': [4, 35], 'compiled_tiny_original_15c.mkv': [42, 53]},
        '24010000808582cb': {'compiled_tiny_original_15a.mkv': [24, 25, 35, 36], 'compiled_tiny_original_15b.mkv': [5, 6, 36, 37], 'compiled_tiny_original_15c.mkv': [43, 44, 54, 55]},
        '24000000808582cb': {'compiled_tiny_original_15a.mkv': [26, 27, 28, 29, 37, 38, 39], 'compiled_tiny_original_15b.mkv': [7, 8, 9, 38, 39, 40, 41], 'compiled_tiny_original_15c.mkv': [45, 46, 48, 56, 57, 59]},
        '24000000808582ca': {'compiled_tiny_original_15a.mkv': [30, 40, 41], 'compiled_tiny_original_15b.mkv': [10, 11, 42], 'compiled_tiny_original_15c.mkv': [49, 60]},
        '0000003010000000': {'compiled_tiny_original_15b.mkv': [16], 'compiled_tiny_original_15c.mkv': [4]},
        '0000409090848682': {'compiled_tiny_original_15b.mkv': [17], 'compiled_tiny_original_15c.mkv': [5]},
        '0040c09090848686': {'compiled_tiny_original_15b.mkv': [18], 'compiled_tiny_original_15c.mkv': [6]},
        '4040c09094848686': {'compiled_tiny_original_15b.mkv': [19], 'compiled_tiny_original_15c.mkv': [7]},
        '4004c49094868686': {'compiled_tiny_original_15b.mkv': [20], 'compiled_tiny_original_15c.mkv': [8]},
        '8084c49494868686': {'compiled_tiny_original_15b.mkv': [21], 'compiled_tiny_original_15c.mkv': [9]},
        'c8d4c4d49486c686': {'compiled_tiny_original_15b.mkv': [22, 23], 'compiled_tiny_original_15c.mkv': [10, 11]},
        'd9d1c5d49486c696': {'compiled_tiny_original_15b.mkv': [24], 'compiled_tiny_original_15c.mkv': [12]},
        'd9d5c5d49486c696': {'compiled_tiny_original_15b.mkv': [25], 'compiled_tiny_original_15c.mkv': [13]},
        'd8d5c5d49486c696': {'compiled_tiny_original_15b.mkv': [26, 28, 29], 'compiled_tiny_original_15c.mkv': [14, 16, 17]},
        'd8d5cdd49486c696': {'compiled_tiny_original_15b.mkv': [27], 'compiled_tiny_original_15c.mkv': [15]},
        '1119999494849696': {'compiled_tiny_original_15b.mkv': [30], 'compiled_tiny_original_15c.mkv': [18]},
        '768925cd4dc3780c': {'compiled_tiny_original_15b.mkv': [46], 'compiled_tiny_original_15c.mkv': [24]}
    }
    
    max_gap = 1  ## Num of frames allowed between discovered matching frames, to be included in the same sequence
    merged, extras = find_possible_sequences(conflicting_frame_hashes, max_gap)
    rprint('conflicting_frame_hashes:')
    rprint(conflicting_frame_hashes)
    rprint('merged:')
    rprint(merged)
    rprint('extras:')
    rprint(extras)



'''

possible_sequences:
{
    'sequence 0': {'compiled_tiny_original_15b.mkv': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 'compiled_tiny_original_15c.mkv': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37], 'compiled_tiny_original_15a.mkv': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]},        
    'sequence 1': {
        'compiled_tiny_original_15b.mkv': [4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41, 42],
        'compiled_tiny_original_15c.mkv': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 42, 43, 44, 45, 46, 48, 49, 53, 54, 55, 56, 57, 59, 60],
        'compiled_tiny_original_15a.mkv': [23, 24, 25, 26, 27, 28, 29, 30, 34, 35, 36, 37, 38, 39, 40, 41]
    },
    'sequence 2': {'compiled_tiny_original_15b.mkv': [46], 'compiled_tiny_original_15c.mkv': [24], 'compiled_tiny_original_15a.mkv': []}
}


'''