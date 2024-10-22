from rich import print as pprint



def reorganize_frames(input_data):
    output = {}
    extras = {}
    sequence_counter = 0
    
    # Initialize the first sequence
    output[f'sequence {sequence_counter}'] = {key: [] for key in next(iter(input_data.values()))}
    
    for clip, values in input_data.items():
        if clip == f'clip {len(input_data) - 1}':
            extras = values
            continue
        
        if all(not lst for lst in values.values()):
            sequence_counter += 1
            output[f'sequence {sequence_counter}'] = {key: [] for key in values}
        
        for key, lst in values.items():
            output[f'sequence {sequence_counter}'][key].extend(lst)
    
    # Remove empty sequences
    output = {k: v for k, v in output.items() if any(v.values())}
    
    # Renumber sequences
    output = {f'sequence {i}': v for i, v in enumerate(output.values())}
    
    return output, extras



if __name__ == '__main__':
    input = {
        'clip 1': {'a': [6], 'b': [47], 'c': [25]},
        'clip 2': {'a': [7, 8, 9], 'b': [48, 49, 50], 'c': [26, 27, 28]},
        'clip 3': {'a': [10, 11, 12, 13, 14, 15], 'b': [51, 52, 53, 54, 55, 56, 57, 58], 'c': [29, 30, 31, 32, 33, 34]},
        'clip 4': {'a': [16, 17, 18], 'b': [59], 'c': [35, 36, 37]},
        'clip 5': {'a': [23, 34], 'b': [4, 35], 'c': [42, 53]},
        'clip 6': {'a': [97, 98, 99], 'b': [88, 89, 90], 'c': [76, 77, 78]},
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
    
    output, extras = reorganize_frames(input)
    output = separate_into_sequences(output)
    print(output == desired_output)
    print(extras == desired_extras)
    pprint(output)
    pprint(extras)