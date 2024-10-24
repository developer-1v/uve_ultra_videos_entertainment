from rich import print as rprint
from copy import deepcopy

def merge_all_sequences(sequences, max_gap=1):
    # Ensure sequences is a list of dictionaries
    sequences = deepcopy(list(sequences.values() if isinstance(sequences, dict) else sequences))

    # Convert all sequences' lists to sets for efficient merging
    for seq in sequences:
        seq.update((k, set(v)) for k, v in seq.items())

    sequences_changed = True
    while sequences_changed:
        sequences_changed = False
        keys = {k for seq in sequences for k in seq}
        
        for key in keys:
            for i in range(len(sequences)):
                if key in sequences[i]:
                    last_num_seq1 = max(sequences[i][key])
                    for j in range(len(sequences)):
                        if i != j and key in sequences[j]:
                            first_num_seq2 = min(sequences[j][key])
                            if last_num_seq1 + 1 <= first_num_seq2 <= last_num_seq1 + max_gap:
                                sequences[i][key].update(sequences[j][key])
                                sequences[j].pop(key, None)
                                sequences_changed = True
                                break

        # Remove empty dictionaries from the list
        sequences = [seq for seq in sequences if seq]

    # Convert sets back to sorted lists
    for seq in sequences:
        seq.update((k, sorted(v)) for k, v in seq.items())

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
