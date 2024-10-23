


def merge_consecutive_sequences(input_dict, extras):
    result = {}
    for sequence in input_dict.values():
        for key, value_list in sequence.items():
            if key not in result:
                result[key] = []
            result[key].extend(value_list)
    
    # Add Extras to the result
    for key, value_list in extras.items():
        if key not in result:
            result[key] = []
        result[key].extend(value_list)
    
    new_extras = {key: [] for key in extras}
    
    for key in result:
        result[key].sort()
        merged = []
        current_sequence = [result[key][0]]
        
        for num in result[key][1:]:
            if num == current_sequence[-1] + 1:
                current_sequence.append(num)
            else:
                if len(current_sequence) == 1:
                    new_extras[key].append(current_sequence[0])
                else:
                    merged.append(current_sequence)
                current_sequence = [num]
        
        if len(current_sequence) == 1:
            new_extras[key].append(current_sequence[0])
        else:
            merged.append(current_sequence)
        result[key] = merged
    
    return result, new_extras

input = {
    'sequence 0': {'a': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], 'b': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 'c': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]},
    'sequence 1': {'a': [24, 25], 'b': [5, 6], 'c': [43, 44]},
    'sequence 2': {'a': [35, 36], 'b': [36, 37], 'c': [54, 55]},
    'sequence 3': {'a': [26, 27, 28, 29], 'b': [7, 8, 9], 'c': [45, 46]},
    'sequence 4': {'a': [37, 38, 39], 'b': [38, 39, 40, 41]}
}
Extras = {'a': [23, 34, 91, 95], 'b': [4, 35, 92, 96, 27, 30, 46], 'c': [42, 53, 48, 59, 93, 98, 15, 18, 24]}

output, new_extras = merge_consecutive_sequences(input, Extras)
print("Merged sequences:")
print(output)
print("\nUpdated Extras:")
print(new_extras)