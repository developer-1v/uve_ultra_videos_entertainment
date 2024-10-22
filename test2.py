from rich import print as pprint
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


if __name__ == '__main__':
    input = {
        'hgd': {'a': [97, 98, 99], 'b': [88, 89, 90], 'c': [76, 77, 78]},
        'afa': {'a': [6], 'b': [47], 'c': [25]},
        'gafs': {'a': [7, 8, 9], 'b': [48, 49, 50], 'c': [26, 27, 28]},
        'hgs': {'a': [10, 11, 12, 13, 14, 15], 'b': [51, 52, 53, 54, 55, 56, 57, 58], 'c': [29, 30, 31, 32, 33, 34]},
        '3fsa': {'a': [16, 17, 18], 'b': [59], 'c': [35, 36, 37]},
        'gaf': {'a': [23, 34], 'b': [4, 35], 'c': [42, 53]},
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
    
    merged = sort_data(input)
    # merged = separate_into_sequences(merged)
    print(merged == desired_output)
    # print(extras == desired_extras)
    pprint(merged)
    # pprint(extras)
    
    
'''
{'a': [[6], [7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18], [23], [34], [97, 98, 99]], 'b': [[47], [48, 49, 50], [51, 52, 53, 54, 55, 56, 57, 58], [59], [4], [35], [88, 89, 90]], 'c': [[25], [26, 27, 28], [29, 30, 31, 32, 33, 34], [35, 36, 37], [42], [53], [76, 77, 78]]}

Make me a function that will return two dictionaries. 
The first dictionary will merge as many of these lists as it can, per key with the following rules:
it can only merge lists that are consecutive in numbers. If there is a gap of more than 1, it will not merge them. 
The second dictionary will contain the remaining lists that did not get merged, but each of these numbers in the merged list
will actually be flattened into a single list

'''