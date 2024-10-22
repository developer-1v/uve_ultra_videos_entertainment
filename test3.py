def merge_and_extract_extras(data):
    merged = {}
    extras = {key: [] for key in data}
    sequence_count = 0

    # Initialize pointers for each key
    pointers = {key: 0 for key in data}
    max_length = max(len(data[key]) for key in data)

    while any(pointers[key] < len(data[key]) for key in data):
        current_sequence = {key: [] for key in data}
        min_start = None

        # Determine the minimum start value for the next sequence
        for key in data:
            if pointers[key] < len(data[key]):
                if min_start is None or data[key][pointers[key]][0] < min_start:
                    min_start = data[key][pointers[key]][0]

        # Build sequences starting from the minimum start value
        for key in data:
            while pointers[key] < len(data[key]) and (not current_sequence[key] or data[key][pointers[key]][0] == current_sequence[key][-1] + 1):
                current_sequence[key].extend(data[key][pointers[key]])
                pointers[key] += 1

        # Store the sequences or move to extras if only one frame
        for key in current_sequence:
            if len(current_sequence[key]) > 1:
                if f"sequence {sequence_count}" not in merged:
                    merged[f"sequence {sequence_count}"] = {}
                merged[f"sequence {sequence_count}"][key] = current_sequence[key]
            elif current_sequence[key]:
                extras[key].extend(current_sequence[key])

        if any(len(current_sequence[key]) > 1 for key in current_sequence):
            sequence_count += 1

    return merged, extras

# Example usage
data = {
    'a': [[6], [7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18], [23], [34], [97, 98, 99]],
    'b': [[47], [48, 49, 50], [51, 52, 53, 54, 55, 56, 57, 58], [59], [4], [35], [88, 89, 90]],
    'c': [[25], [26, 27, 28], [29, 30, 31, 32, 33, 34], [35, 36, 37], [42], [53], [76, 77, 78]]
}

merged, extras = merge_and_extract_extras(data)
print("Merged:", merged)
print("Extras:", extras)