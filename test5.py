from rich import print as rprint


def merge_all_sequences(sequences):
    keys = set(k for seq in sequences for k in seq.keys())  # Collect all unique keys from all sequences
    for key in keys:
        merged = True
        while merged:
            merged = False
            for i in range(len(sequences)):
                if key in sequences[i]:
                    last_num_seq1 = sequences[i][key][-1]
                    for j in range(len(sequences)):
                        if i != j and key in sequences[j]:
                            first_num_seq2 = sequences[j][key][0]
                            if last_num_seq1 + 1 == first_num_seq2:
                                # Perform the merge
                                sequences[i][key].extend(sequences[j][key])
                                del sequences[j][key]
                                merged = True
                                break
                    if merged:
                        break
        # Clean up sequences with no remaining keys under 'key' after all merges are done
        sequences = [seq for seq in sequences if key in seq or len(seq.keys()) > 1]

    # Create a dictionary with sequence labels
    labeled_sequences = {}
    for index, sequence in enumerate(sequences):
        label = f'sequence {index}'
        labeled_sequences[label] = sequence

    return labeled_sequences


sequences = {
    'sequence 0': {'a': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'b': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 'c': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]},
    'sequence 1': {'a': [24, 25], 'b': [5, 6], 'c': [43, 44]},
}

sequences = [
    {
        'a': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        'b': [46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        'c': [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
    },
    {
        'a': [23, 24, 25],
        'b': [4, 5, 6],
        'c': [42, 43, 44]
    },
    {
        'a': [34, 35, 36],
        'b': [35, 36, 37],
        'c': [53, 54, 55]
    },
    {
        'a': [26, 27, 28, 29],
        'b': [7, 8, 9],
        'c': [45, 46, 48]
    },
    {
        'a': [37, 38, 39],
        'b': [38, 39, 40, 41]
    }
]

extras = {'a': [91, 95], 'b': [92, 96, 27, 30], 'c': [59, 93, 98, 15, 18]}

# Example usage:
merged_sequences = merge_all_sequences(sequences)
print('merged sequences:')
rprint(merged_sequences)
