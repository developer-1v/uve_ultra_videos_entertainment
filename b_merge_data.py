from rich import print as rprint





def get_merged_data(data):
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
            else:
                # Move single-frame data to extras
                extras[key].extend(current_sequence[key])

        # Check if the sequence has more than one key before incrementing sequence_count
        if len(merged.get(f"sequence {sequence_count}", {})) > 1:
            sequence_count += 1
        else:
            # Remove the sequence if it does not span multiple keys
            merged.pop(f"sequence {sequence_count}", None)

    return merged, extras




input = {

    'a': [[6], [7, 8, 9], [10, 11, 12, 13, 14, 15], [16, 17, 18], [23], [34], [24, 25], [35, 36], [26, 27, 28, 29], [37, 38, 39], [91], [95]],
    'b': [[47], [48, 49, 50], [51, 52, 53, 54, 55, 56, 57, 58], [59], [4], [35], [5, 6], [36, 37], [7, 8, 9], [38, 39, 40, 41], [92], [96], [16], [17], [18], [19], [20], [21], [22, 23], [24], [25], [26], [28, 29], [27], [30], [46]],
    'c': [[25], [26, 27, 28], [29, 30, 31, 32, 33, 34], [35, 36, 37], [42], [53], [43, 44], [54, 55], [45, 46], [48], [56, 57], [59], [93], [98], [4], [5], [6], [7], [8], [9], [10, 11], [12], [13], [14], [16, 17], [15], [18], [24]] 
}

merged, extras = get_merged_data(input)
rprint("Merged:", merged)
rprint("Extras:", extras)
