from rich.pretty import pprint
from rich import print as rprint
from print_tricks import pt









if __name__ == "__main__":


    conflicting_frame_hashes = {
        '7619a4cc4dc3788c': {'compiled_tiny_original_15a.mkv': [6], 'compiled_tiny_original_15b.mkv': [47], 'compiled_tiny_original_15c.mkv': [25]},
        '7691644c4dcb788c': {'compiled_tiny_original_15a.mkv': [7, 8, 9], 'compiled_tiny_original_15b.mkv': [48, 49, 50], 'compiled_tiny_original_15c.mkv': [26, 27, 28]},
        '7691654c4dcb788c': {'compiled_tiny_original_15a.mkv': [10, 11, 12, 13, 14, 15], 'compiled_tiny_original_15b.mkv': [51, 52, 53, 54, 55, 56, 57, 58], 'compiled_tiny_original_15c.mkv': [29, 30, 31, 32, 33, 34]},
        '7691654c4dcb780c': {'compiled_tiny_original_15a.mkv': [16, 17, 18], 'compiled_tiny_original_15b.mkv': [59], 'compiled_tiny_original_15c.mkv': [35, 36, 37]},
        '24010080808582cb': {'compiled_tiny_original_15a.mkv': [23, 34], 'compiled_tiny_original_15b.mkv': [4, 35], 'compiled_tiny_original_15c.mkv': [42, 53]},
        '24010000808582cb': {'compiled_tiny_original_15a.mkv': [24, 25, 35, 36], 'compiled_tiny_original_15b.mkv': [5, 6, 36, 37], 'compiled_tiny_original_15c.mkv': [43, 44, 54, 55]},
        '24000000808582cb': {'compiled_tiny_original_15a.mkv': [26, 27, 28, 29, 37, 38, 39], 'compiled_tiny_original_15b.mkv': [7, 8, 9, 38, 39, 40, 41], 'compiled_tiny_original_15c.mkv': [45, 46, 48, 56, 57, 59]},
        '24000000808582ca': {'compiled_tiny_original_15a.mkv': [30, 40, 41], 'compiled_tiny_original_15b.mkv': [10, 11, 42], 'compiled_tiny_original_15c.mkv': [49, 60]},
        '24000000808582ca': {'compiled_tiny_original_15a.mkv': [51, 62], 'compiled_tiny_original_15b.mkv': [54, 65], 'compiled_tiny_original_15c.mkv': [57, 68]},
        '0000003010000000': {'compiled_tiny_original_15b.mkv': [16], 'compiled_tiny_original_15c.mkv': [4]},
        '0000409090848682': {'compiled_tiny_original_15b.mkv': [17], 'compiled_tiny_original_15c.mkv': [5]},
        '0040c09090848686': {'compiled_tiny_original_15b.mkv': [18], 'compiled_tiny_original_15c.mkv': [6]},
        '4040c09094848686': {'compiled_tiny_original_15b.mkv': [19], 'compiled_tiny_original_15c.mkv': [7]},
        '4004c49094868686': {'compiled_tiny_original_15b.mkv': [20], 'compiled_tiny_original_15c.mkv': [8]},
        '8084c49494868686': {'compiled_tiny_original_15b.mkv': [21], 'compiled_tiny_original_15c.mkv': [9]},
        'c8d4c4d49486c686': {'compiled_tiny_original_15b.mkv': [22, 23], 'compiled_tiny_original_15c.mkv': [10, 11]},
        'd9d1c5d49486c696': {'compiled_tiny_original_15b.mkv': [24], 'compiled_tiny_original_15c.mkv': [12]},
        'd9d5c5d49486c696': {'compiled_tiny_original_15b.mkv': [25], 'compiled_tiny_original_15c.mkv': [13]},
        'd8d5c5d49486c696': {'compiled_tiny_original_15b.mkv': [26, 28, 29], 'compiled_tiny_original_15c.mkv': [14, 16, 17]},
        'd8d5cdd49486c696': {'compiled_tiny_original_15b.mkv': [27], 'compiled_tiny_original_15c.mkv': [15]},
        '1119999494849696': {'compiled_tiny_original_15b.mkv': [30], 'compiled_tiny_original_15c.mkv': [18]},
        '768925cd4dc3780c': {'compiled_tiny_original_15b.mkv': [46], 'compiled_tiny_original_15c.mkv': [24]}
    }
    


    ## fix this below:
    Desired_output_1 = {
        'sequence 0': {
            'compiled_tiny_original_15a.mkv': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            'compiled_tiny_original_15b.mkv': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
            'compiled_tiny_original_15c.mkv': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
        },
        'sequence 1': {
            'compiled_tiny_original_15a.mkv': [23, 24, 25, 26, 27, 28, 29, 30],
            'compiled_tiny_original_15b.mkv': [5, 6, 7, 8, 9, 10, 11, 12],
            'compiled_tiny_original_15c.mkv': [43, 44, 45, 46, 47, 48, 49, 50]
        },
        'sequence 2': {
            'compiled_tiny_original_15a.mkv': [35, 36, 37, 38, 39, 40, 41],
            'compiled_tiny_original_15b.mkv': [38, 39, 40, 41, 42],
            'compiled_tiny_original_15c.mkv': [45, 46, 48, 56, 57, 59]
        }
    }

    Desired_output_2 = {
        'compiled_tiny_original_15a.mkv': [51, 62],
        'compiled_tiny_original_15b.mkv': [54, 65],
        'compiled_tiny_original_15c.mkv': [57, 68],
    }

    max_gap = 1  ## Num of frames allowed between discovered matching frames, to be included in the same sequence
    merged, extras = find_possible_sequences(conflicting_frame_hashes, max_gap)
    rprint('conflicting_frame_hashes:')
    rprint(conflicting_frame_hashes)
    rprint('merged:')
    rprint(merged)
    rprint('extras:')
    rprint(extras)

    print(Desired_output_1 == merged)
    print(Desired_output_2 == extras)