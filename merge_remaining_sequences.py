from rich import print as rprint
from copy import deepcopy

def merge_all_sequences(sequences, max_gap=1):
    if isinstance(sequences, dict):
        sequences = deepcopy(list(sequences.values()))  # Create a deep copy of the sequences
    else:
        sequences = deepcopy(sequences)  # Ensure a deep copy is used if not initially a dictionary

    # Convert all sequences' lists to sets for efficient merging
    for seq in sequences:
        for key in seq:
            seq[key] = set(seq[key])

    keys = set(k for seq in sequences for k in seq.keys())
    for key in keys:
        sequences_copy = [seq.copy() for seq in sequences]  # Use deep copy to avoid modifying original during iteration

        # Collect all merge operations
        i = 0
        while i < len(sequences_copy):
            if key in sequences_copy[i]:
                last_num_seq1 = max(sequences_copy[i][key])  # Use max since we're now dealing with sets
                j = 0
                while j < len(sequences_copy):
                    if i != j and key in sequences_copy[j]:
                        first_num_seq2 = min(sequences_copy[j][key])  # Use min for the same reason
                        if last_num_seq1 + 1 <= first_num_seq2 <= last_num_seq1 + max_gap:
                            # Merge sets directly
                            sequences[i][key].update(sequences[j][key])
                            del sequences[j][key]
                            sequences_copy[i][key].update(sequences_copy[j][key])
                            del sequences_copy[j][key]
                            break
                    j += 1
            i += 1

        # Clean up sequences with no remaining keys under 'key'
        sequences = [seq for seq in sequences if seq.keys()]

    # Convert sets back to lists if order is important, otherwise can leave as sets
    for seq in sequences:
        for key in seq:
            seq[key] = sorted(seq[key])  # Convert back to sorted list to maintain order

    # Re-label sequences
    labeled_sequences = {f'sequence {index}': seq for index, seq in enumerate(sequences)}
    return labeled_sequences

if __name__ == '__main__':
    sequences = {
        "sequence 0": {
            "a": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "b": [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
            "c": [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
        },
        "sequence 1": {
            "a": [23, 24, 25],
            "b": [4, 5, 6],
            "c": [42, 43, 44]
        },
        "sequence 2": {
            "a": [34, 35, 36],
            "b": [35, 36, 37],
            "c": [53, 54, 55]
        },
        "sequence 3": {
            "a": [26, 27, 28, 29],
            "b": [7, 8, 9],
            "c": [45, 46, 48]
        },
        "sequence 4": {
            "a": [37, 38, 39],
            "b": [38, 39, 40, 41]
        }
    }

    updated_extras = {
        "a": [91, 95],
        "b": [92, 96, 27, 30],
        "c": [59, 93, 98, 15, 18]
    }


    extras = {'a': [91, 95], 'b': [92, 96, 27, 30], 'c': [59, 93, 98, 15, 18]}

    # Example usage:
    merged_sequences = merge_all_sequences(sequences)
    print('merged sequences:')
    rprint(merged_sequences)
