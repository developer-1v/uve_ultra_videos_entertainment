from rich import print as rprint
from print_tricks import pt

def debug_print(
    video_hashes, 
    conflicting_frame_hashes, 
    sorted_data, 
    merged, 
    extras, 
    merged_w_extras, 
    new_extras, 
    possible_conflicting_sequences,
    test_full_vids=False,
    print_data=False,  # Controls printing of data structures
    print_key_totals=False,  # Controls printing of total items per key
    print_totals=False,  # Controls printing of total items
):
    data_labels = [
        ("video hashes", video_hashes),
        ("conflicting frame hashes", conflicting_frame_hashes),
        ("sorted data", sorted_data),
        ("merged", merged),
        ("extras", extras),
        ("merged with extras", merged_w_extras),
        ("new extras", new_extras),
        ("possible conflicting sequences", possible_conflicting_sequences),
    ]
    
    if test_full_vids:
        with open('log.txt', 'w') as log_file:
            def log_print(message):
                print(message, file=log_file)
            print_func = log_print
    else:
        print_func = rprint

    def print_dict_details(data, label, print_func):
        total_items = 0
        subkey_totals = {}

        for key, subdict in data.items():
            if isinstance(subdict, dict):
                sub_total = 0
                for subkey, items in subdict.items():
                    item_count = len(items)
                    sub_total += item_count
                    if print_data:
                        print_func(f'  {subkey}: {items} ({item_count} items)')
                    if print_key_totals:
                        subkey_totals[subkey] = subkey_totals.get(subkey, 0) + item_count
                if print_key_totals:
                    print_func(f'  Total in {key}: {sub_total} items')
                total_items += sub_total
            else:
                item_count = len(subdict)
                if print_data:
                    print_func(f'  {key}: {subdict} ({item_count} items)')
                total_items += item_count

        if print_totals:
            print_func(f'Total items in {label}: {total_items}')
        if print_key_totals:
            for subkey, total in subkey_totals.items():
                print_func(f'Total items in {label} {subkey}: {total} items')

    # Moved outside the `if print_data` block
    for label, data in data_labels:
        print_func(f'\n{label}:\n')
        print_func(data)
        print_dict_details(data, label, print_func)

