from rich import print as rprint
from print_tricks import pt
import copy




def flatten_data(data):
    """ Flatten nested lists in the dictionary values. """
    flattened_data = {}
    for key in data:
        if all(isinstance(sublist, list) for sublist in data[key]):
            flat_list = []
            for sublist in data[key]:
                flat_list.extend(sublist)
            flattened_data[key] = flat_list
        else:
            flattened_data[key] = data[key]
    return flattened_data

def initialize_structures(data):
    """ Initialize pointers and data structures for sequence building. """
    pointers = {key: 0 for key in data}
    max_length = max(len(data[key]) for key in data)
    return pointers, max_length

def build_sequences(data, pointers):
    """ Build sequences from the data based on the pointers. """
    current_sequence = {key: [] for key in data}
    min_start = None
    for key in data:
        if pointers[key] < len(data[key]):
            if min_start is None or data[key][pointers[key]] < min_start:
                min_start = data[key][pointers[key]]
    for key in data:
        while pointers[key] < len(data[key]) and (not current_sequence[key] or data[key][pointers[key]] == current_sequence[key][-1] + 1):
            current_sequence[key].append(data[key][pointers[key]])
            pointers[key] += 1
    return current_sequence

def store_sequences(merged, extras, current_sequence, sequence_count):
    """ Store sequences or move to extras if only one frame, working on a copy of extras. """
    extras_copy = copy.deepcopy(extras)  # Create a deep copy of extras
    for key in current_sequence:
        if len(current_sequence[key]) > 1:
            if f"sequence {sequence_count}" not in merged:
                merged[f"sequence {sequence_count}"] = {}
            merged[f"sequence {sequence_count}"][key] = current_sequence[key]
        else:
            extras_copy[key].extend(current_sequence[key])
    return merged, extras_copy



def get_merged_data(data):
    data = flatten_data(data)
    pointers, max_length = initialize_structures(data)
    merged = {}
    extras = {key: [] for key in data}
    sequence_count = 0

    while any(pointers[key] < len(data[key]) for key in data):
        current_sequence = build_sequences(data, pointers)
        merged, extras = store_sequences(merged, extras, current_sequence, sequence_count)
        if len(merged.get(f"sequence {sequence_count}", {})) > 1:
            sequence_count += 1
        else:
            merged.pop(f"sequence {sequence_count}", None)
    return merged, extras



if __name__ == '__main__':

    # input = {

    #     'a': [[6], [7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18], [23], [34], [24, 25], [35, 36], [26, 27, 28, 29], [37, 38, 39], [91], [95]],
    #     'b': [[47], [48, 49, 50], [51, 52, 53, 54, 55, 56, 57, 58], [59], [4], [35], [5, 6], [36, 37], [7, 8, 9], [38, 39, 40, 41], [92], [96], [16], [17], [18], [19], [20], [21], [22, 23], [24], [25], [26], [28, 29], [27], [30], [46]],
    #     'c': [[25], [26, 27, 28], [29, 30, 31, 32, 33, 34], [35, 36, 37], [42], [53], [43, 44], [54, 55], [45, 46], [48], [56, 57], [59], [93], [98], [4], [5], [6], [7], [8], [9], [10, 11], [12], [13], [14], [16, 17], [15], [18], [24]] 
    # }
    input = {
    'compiled_tiny_original_15a.mkv': [[6], [7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18], [23], [34], [24, 25], [35, 36], [26, 27, 28, 29], [37, 38, 39], [30], [40, 41]],
    'compiled_tiny_original_15b.mkv': [[47], [48, 49, 50], [51, 52, 53, 54, 55, 56, 57, 58], [59], [4], [35], [5, 6], [36, 37], [7, 8, 9], [38, 39, 40, 41], [10, 11], [42], [16], [17], [18], [19], [20], [21], [22, 23], [24], [25], [26], [28, 29], [27], [30], [46]],
    'compiled_tiny_original_15c.mkv': [[25], [26, 27, 28], [29, 30, 31, 32, 33, 34], [35, 36, 37], [42], [53], [43, 44], [54, 55], [45, 46], [48], [56, 57], [59], [49], [60], [4], [5], [6], [7], [8], [9], [10, 11], [12], [13], [14], [16, 17], [15], [18], [24]]
    }
    ## flatten out the lists in each dict and get their lengths
    for key in input:
        input[key] = [item for sublist in input[key] for item in sublist]
        print(f"{key}: {len(input[key])}")


    merged, extras = get_merged_data(input)
    rprint("Merged:", merged)
    rprint("Extras:", extras)



'''

{
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

'''