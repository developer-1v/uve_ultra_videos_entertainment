from rich import print as pprint
from print_tricks import pt

def sort_data(input_data):
    # Initialize sorted_data with keys from input_data
    sorted_data = {key: [] for key in input_data[next(iter(input_data))]}
    used_numbers = {key: set() for key in input_data[next(iter(input_data))]}  # Track numbers already added
    
    # Collect all frames correctly ensuring keys match
    frames = []
    for key in input_data:
        frame = []
        for sub_key in sorted_data.keys():  # Ensure we only collect for keys in sorted_data
            if sub_key in input_data[key]:
                frame.append(tuple(input_data[key][sub_key]))
            else:
                frame.append(tuple())  # Append empty tuple if key not present
        frames.append(frame)
    
    # Debugging output to check frames
    print("Collected frames:", frames)

    # Sort frames by the first element of the first key to maintain order
    frames.sort(key=lambda x: x[0][0] if x[0] else float('inf'))
    
    # Debugging output to check sorted frames
    print("Sorted frames:", frames)
    
    # Find sorted data
    for frame in frames:
        for sub_key, seq in zip(sorted_data.keys(), frame):
            sequence = []
            last_num = None
            
            for num in seq:
                if num in used_numbers[sub_key]:  # Skip number if already used
                    continue
                if last_num is not None and num != last_num + 1:
                    sorted_data[sub_key].append(sequence)
                    sequence = []
                sequence.append(num)
                last_num = num
                used_numbers[sub_key].add(num)  # Mark number as used
            
            # Append the last sequence
            if sequence:
                sorted_data[sub_key].append(sequence)

    # Debugging output to check final sorted data
    print("Final sorted data:", sorted_data)
    
    return sorted_data


if __name__ == '__main__':
    # input = {
    #     'hgd': {'a': [97, 98, 99], 'b': [88, 89, 90], 'c': [76, 77, 78]},
    #     'afa': {'a': [6], 'b': [47], 'c': [25]},
    #     'gafs': {'a': [7, 8, 9], 'b': [48, 49, 50], 'c': [26, 27, 28]},
    #     'hgs': {'a': [10, 11, 12, 13, 14, 15], 'b': [51, 52, 53, 54, 55, 56, 57, 58], 'c': [29, 30, 31, 32, 33, 34]},
    #     '3fsa': {'a': [16, 17, 18], 'b': [59], 'c': [35, 36, 37]},
    #     'gaf': {'a': [23, 34], 'b': [4, 35], 'c': [42, 53]},
    # }

    input = {
        '7619a4cc4dc3788c': {'a': [6], 'b': [47], 'c': [25]},
        '7691644c4dcb788c': {'a': [7, 8, 9], 'b': [48, 49, 50], 'c': [26, 27, 28]},
        '7691654c4dcb788c': {'a': [10, 11, 12, 13, 14, 15], 'b': [51, 52, 53, 54, 55, 56, 57, 58], 'c': [29, 30, 31, 32, 33, 34]},
        '7691654c4dcb780c': {'a': [16, 17, 18], 'b': [59], 'c': [35, 36, 37]},
        '24010080808582cb': {'a': [23, 34], 'b': [4, 35], 'c': [42, 53]},
        '24010000808582cb': {'a': [24, 25, 35, 36], 'b': [5, 6, 36, 37], 'c': [43, 44, 54, 55]},
        '24000000808582cb': {'a': [26, 27, 28, 29, 37, 38, 39], 'b': [7, 8, 9, 38, 39, 40, 41], 'c': [45, 46, 48, 56, 57, 59]},
        '24000000808582ca': {'a': [30, 40, 41], 'b': [10, 11, 42], 'c': [49, 60]},
        '24000000808582ca': {'a': [91, 95], 'b': [92, 96], 'c': [93, 98]},
        '0000003010000000': {'b': [16], 'c': [4]},
        '0000409090848682': {'b': [17], 'c': [5]},
        '0040c09090848686': {'b': [18], 'c': [6]},
        '4040c09094848686': {'b': [19], 'c': [7]},
        '4004c49094868686': {'b': [20], 'c': [8]},
        '8084c49494868686': {'b': [21], 'c': [9]},
        'c8d4c4d49486c686': {'b': [22, 23], 'c': [10, 11]},
        'd9d1c5d49486c696': {'b': [24], 'c': [12]},
        'd9d5c5d49486c696': {'b': [25], 'c': [13]},
        'd8d5c5d49486c696': {'b': [26, 28, 29], 'c': [14, 16, 17]},
        'd8d5cdd49486c696': {'b': [27], 'c': [15]},
        '1119999494849696': {'b': [30], 'c': [18]},
        '768925cd4dc3780c': {'b': [46], 'c': [24]}
    }
    total_a = sum(len(input[key].get('a', [])) for key in input)
    total_b = sum(len(input[key].get('b', [])) for key in input)
    total_c = sum(len(input[key].get('c', [])) for key in input)

    print(f"Total numbers under 'a': {total_a}")
    print(f"Total numbers under 'b': {total_b}")
    print(f"Total numbers under 'c': {total_c}")
    
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
    
    sorted_data = sort_data(input)
    # merged = separate_into_sequences(merged)
    print(sorted_data == desired_output)
    # print(extras == desired_extras)
    pprint(sorted_data)
    # pprint(extras)
    
    
'''
{'a': [[6], [7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18], [23], [34], [97, 98, 99]], 'b': [[47], [48, 49, 50], [51, 52, 53, 54, 55, 56, 57, 58], [59], [4], [35], [88, 89, 90]], 'c': [[25], [26, 27, 28], [29, 30, 31, 32, 33, 34], [35, 36, 37], [42], [53], [76, 77, 78]]}

Make me a function that will return two dictionaries. 
The first dictionary will merge as many of these lists as it can, per key with the following rules:
it can only merge lists that are consecutive in numbers. If there is a gap of more than 1, it will not merge them. 
The second dictionary will contain the remaining lists that did not get merged, but each of these numbers in the merged list
will actually be flattened into a single list

'''