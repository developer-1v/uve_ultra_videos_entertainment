from copy import deepcopy

from rich import print as rprint


def merge_extras_into_sequences(sequences, extras, max_gap=1):
    sequences_copy = deepcopy(sequences)  # Create a deep copy of sequences to avoid modifying the original data
    extras_copy = deepcopy(extras)  # Create a deep copy of extras to avoid modifying the original data
    for key in extras_copy.keys():
        new_extras = extras_copy[key].copy()  # Copy the list to modify while iterating
        for num in extras_copy[key][:]:  # Iterate over a copy of the list
            for seq_name, seq_data in sequences_copy.items():
                if key in seq_data:  # Check if the key exists in the sequence
                    # Check if the number can be added to the beginning or end of the list within the max_gap
                    if abs(seq_data[key][0] - num) <= max_gap:
                        seq_data[key].insert(0, num)
                        new_extras.remove(num)
                    elif abs(seq_data[key][-1] - num) <= max_gap:
                        seq_data[key].append(num)
                        new_extras.remove(num)
        extras_copy[key] = new_extras  # Update the extras_copy with remaining numbers
        merged_with_extras = sequences_copy
    return merged_with_extras, extras_copy

if __name__ == '__main__':
    input = {
        'sequence 0': {'a': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'b': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 'c': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]},
        'sequence 1': {'a': [24, 25], 'b': [5, 6], 'c': [43, 44]},
        'sequence 2': {'a': [35, 36], 'b': [36, 37], 'c': [54, 55]},
        'sequence 3': {'a': [26, 27, 28, 29], 'b': [7, 8, 9], 'c': [45, 46]},
        'sequence 4': {'a': [37, 38, 39], 'b': [38, 39, 40, 41]}
    }
    Extras = {'a': [23, 34, 91, 95], 'b': [4, 35, 92, 96, 27, 30, 46], 'c': [42, 53, 48, 59, 93, 98, 15, 18, 24]}

    merged, extras = merge_extras_into_sequences(input, Extras)
    rprint('merged:')
    rprint(merged)
    rprint('extras:')
    rprint(extras)

