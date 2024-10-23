
def merge_additional_sequences(result, updated_extras):
    keys = list(result.keys())
    merged = True  # Initialize a flag to check if any merge happened
    while merged:  # Continue looping until no more merges are possible
        merged = False  # Reset the flag for the current iteration
        new_result = {}  # Create a new result dictionary to avoid modifying during iteration
        keys = list(result.keys())  # Refresh the keys list in case it has changed

        for i in range(len(keys)):
            if keys[i] not in result:
                continue  # Skip if the key has been deleted in a previous merge
            for j in range(i + 1, len(keys)):
                if keys[j] not in result:
                    continue  # Skip if the key has been deleted in a previous merge
                for subkey in result[keys[i]]:
                    if subkey in result[keys[j]] and can_merge(result[keys[i]][subkey], result[keys[j]][subkey]):
                        result[keys[i]][subkey].extend(result[keys[j]][subkey])
                        del result[keys[j]]  # Remove the merged sequence
                        merged = True  # Set the flag to True as a merge happened
                        break  # Break to restart the process as the dictionary has changed
                if merged:
                    break  # Break to restart the outer loop as well

        # Attempt to merge extras into the result sequences
        for key, extras_list in list(updated_extras.items()):
            remaining_extras = []
            for extra in extras_list:
                inserted = False
                for seq_key in result:
                    if key in result[seq_key]:
                        if can_merge([result[seq_key][key][-1]], [extra]):  # Check if can append to end
                            result[seq_key][key].append(extra)
                            merged = True
                            inserted = True
                            break
                        elif can_merge([extra], [result[seq_key][key][0]]):  # Check if can prepend to start
                            result[seq_key][key].insert(0, extra)
                            merged = True
                            inserted = True
                            break
                if not inserted:
                    remaining_extras.append(extra)
            updated_extras[key] = remaining_extras

        if not merged:  # If no merge happened in the last full pass, finalize the new_result
            new_result = result.copy()

    return new_result, updated_extras

def merge_consecutive_sequences(input_dict, extras):
    # First, merge consecutive numbers within each original sequence
    merged_input = {}
    for seq_name, sequence in input_dict.items():
        merged_input[seq_name] = {}
        for key, value_list in sequence.items():
            merged_input[seq_name][key] = merge_consecutive(value_list)

    # Merge extras
    merged_extras = {key: merge_consecutive(value_list) for key, value_list in extras.items()}

    # Now, try to merge sequences across different original sequences
    result = {}
    new_extras = {key: [] for key in extras.keys()}

    for seq_name, sequence in merged_input.items():
        result[seq_name] = {}
        for key, value_list in sequence.items():
            # Flatten the list if it contains only one sublist
            if len(value_list) == 1:
                result[seq_name][key] = value_list[0]
            else:
                result[seq_name][key] = value_list

    for key, value_list in merged_extras.items():
        for seq in value_list:
            merged = False  # Initialize merged to False at the start of the loop
            # Here you should include any logic that attempts to merge 'seq' with existing sequences in 'result'
            # If a merge is successful, set merged = True

            if not merged:
                if len(seq) == 1:
                    new_extras[key].append(seq[0])
                else:
                    new_seq_name = f"sequence {len(result)}"
                    result[new_seq_name] = {k: [] for k in extras.keys()}
                    # Flatten the list if it contains only one sublist
                    if len(seq) == 1:
                        result[new_seq_name][key] = seq[0]
                    else:
                        result[new_seq_name][key] = seq

    # Remove any empty sequences
    result = {k: v for k, v in result.items() if any(v.values())}
    result, new_extras = merge_additional_sequences(result, new_extras)  # Add this line to merge additional sequences

    return result, new_extras

def merge_consecutive(numbers):
    numbers.sort()
    result = []
    current_seq = []
    for num in numbers:
        if not current_seq or num == current_seq[-1] + 1:
            current_seq.append(num)
        else:
            result.append(current_seq)
            current_seq = [num]
    if current_seq:
        result.append(current_seq)
    return result

def can_merge(seq1, seq2):
    return seq1[-1] + 1 == seq2[0]


# Test the function
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
for seq_name, seq_data in output.items():
    print(f"{seq_name}:")
    for key, value in seq_data.items():
        print(f"  {key}: {value}")
    print()

print("Updated Extras:")
print(new_extras)