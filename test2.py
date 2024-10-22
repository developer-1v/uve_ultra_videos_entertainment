from rich import print as pprint
from print_tricks import pt

def merge_frames(input_data):
    extras = {'a': [], 'b': [], 'c': []}
    
    # Collect all sequences
    sequences = []
    for key in input_data:
        sequences.append((input_data[key]['a'], input_data[key]['b'], input_data[key]['c']))
    
    # Sort sequences by the first element of 'a' to maintain order
    sequences.sort(key=lambda x: x[0][0] if x[0] else float('inf'))
    
    # Find extras
    for a_seq, b_seq, c_seq in sequences:
        for sub_key, seq in zip(['a', 'b', 'c'], [a_seq, b_seq, c_seq]):
            last_num = None
            sequence = []
            
            for num in seq:
                if last_num is None or num == last_num + 1:
                    sequence.append(num)
                else:
                    extras[sub_key].extend(sequence)
                    sequence = [num]
                last_num = num
            
            # Add remaining sequence to extras if not consecutive
            if sequence:
                extras[sub_key].extend(sequence)
    
    return extras


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
    
    merged = merge_frames(input)
    # merged = separate_into_sequences(merged)
    print(merged == desired_output)
    # print(extras == desired_extras)
    pprint(merged)
    # pprint(extras)