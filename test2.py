from rich import print as pprint


def merge_frames(input_dict):
    from itertools import chain

    # Initialize the output and extras dictionaries
    output = {'sequence 0': {'a': [], 'b': [], 'c': []}}
    extras = {'a': [], 'b': [], 'c': []}

    # Flatten the input dictionary values and sort them
    for key in ['a', 'b', 'c']:
        all_values = sorted(chain.from_iterable(d[key] for d in input_dict.values()))
        
        # Initialize the first sequence
        current_sequence = output['sequence 0'][key]
        
        # Iterate over sorted values to separate into sequences
        for i, value in enumerate(all_values):
            if i == 0 or value == all_values[i - 1] + 1:
                current_sequence.append(value)
            else:
                extras[key].append(value)

    # Add the second sequence for the remaining values
    output['sequence 1'] = {key: extras[key] for key in ['a', 'b', 'c']}
    extras = {key: [] for key in ['a', 'b', 'c']}

    return output, extras



if __name__ == '__main__':
    input = {
        'afa': {'a': [6], 'b': [47], 'c': [25]},
        'gafs': {'a': [7, 8, 9], 'b': [48, 49, 50], 'c': [26, 27, 28]},
        'hgs': {'a': [10, 11, 12, 13, 14, 15], 'b': [51, 52, 53, 54, 55, 56, 57, 58], 'c': [29, 30, 31, 32, 33, 34]},
        '3fsa': {'a': [16, 17, 18], 'b': [59], 'c': [35, 36, 37]},
        'gaf': {'a': [23, 34], 'b': [4, 35], 'c': [42, 53]},
        'hgd': {'a': [97, 98, 99], 'b': [88, 89, 90], 'c': [76, 77, 78]},
    }
    
    desired_output = {
        'sequence 0': {
            'a': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            'b': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
            'c': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37],
        },
        'sequence 1': {
            'a': [97, 98, 99],
            'b': [88, 89, 90],
            'c': [76, 77, 78],
        },
    }
    
    desired_extras = {
        'a': [23, 34],
        'b': [4, 35],
        'c': [42, 53],
    }
    
    output, extras = merge_frames(input)
    # output = separate_into_sequences(output)
    print(output == desired_output)
    print(extras == desired_extras)
    pprint(output)
    pprint(extras)