from rich.pretty import pprint
from rich import print as rprint
from print_tricks import pt

def get_frame_matches(conflicting_frame_hashes):
    frame_matches = {}
    for index, (key, value) in enumerate(conflicting_frame_hashes.items()):
        frame_matches[index] = value
    return frame_matches


def extract_video_names(conflicting_frame_hashes):
    video_names = set()
    for value in conflicting_frame_hashes.values():
        video_names.update(value.keys())
    return video_names

def collect_video_sequences(frame_matches, video_names):
    video_sequences = {video: [] for video in video_names}
    for video in video_sequences.keys():
        all_frames = []
        for index in frame_matches:
            frames = frame_matches[index].get(video, [])
            all_frames.extend(frames)
        all_frames = sorted(set(all_frames))
        video_sequences[video] = all_frames
    return video_sequences


def reorganize_sequences(sequences):
    possible_sequences = {}
    for i, seq in enumerate(sequences):
        sequence_key = f"sequence {i}"
        possible_sequences[sequence_key] = seq
    return possible_sequences

def remove_non_continuous_sequences(conflicting_frame_hashes, video_names, max_gap=1):
    for video in video_names:
        for key, frames in conflicting_frame_hashes.items():
            if video in frames:
                frame_list = frames[video]
                # Sort the frames to ensure they are in order
                frame_list.sort()
                # Check for gaps
                continuous_frames = []
                last_frame = frame_list[0]
                current_sequence = [last_frame]

                for frame in frame_list[1:]:
                    if frame - last_frame <= max_gap:
                        current_sequence.append(frame)
                    else:
                        if len(current_sequence) > 1:
                            continuous_frames.extend(current_sequence)
                        current_sequence = [frame]
                    last_frame = frame

                # Add the last sequence if it's valid
                if len(current_sequence) > 1:
                    continuous_frames.extend(current_sequence)

                # Update the frames for the video
                frames[video] = continuous_frames

    # Remove entries with no frames
    keys_to_remove = [key for key, frames in conflicting_frame_hashes.items() if not any(frames.values())]
    for key in keys_to_remove:
        del conflicting_frame_hashes[key]
        
    return conflicting_frame_hashes
    
def identify_continuous_sequences(conflicting_frame_hashes, video_names, max_gap=1):
    sequences = []
    possible_frames = []

    # Extract frames for the first video
    first_video = list(video_names)[0]
    all_frames_first_video = []

    for frames in conflicting_frame_hashes.values():
        if first_video in frames:
            all_frames_first_video.append(frames[first_video])

    # Flatten the list of frames and sort them
    all_frames_first_video = sorted([frame for sublist in all_frames_first_video for frame in sublist])

    current_sequence = [all_frames_first_video[0]]

    for frame in all_frames_first_video[1:]:
        if frame - current_sequence[-1] <= max_gap:
            current_sequence.append(frame)
        else:
            sequences.append(current_sequence)
            current_sequence = [frame]

    # Add the last sequence if it exists
    if current_sequence:
        sequences.append(current_sequence)

    # Identify possible frames that could be added to sequences later
    for seq in sequences:
        if len(seq) == 1:
            possible_frames.append(seq[0])

    pprint('Sequences:')
    pprint(sequences)
    pprint('Possible frames:')
    pprint(possible_frames)

    return sequences


def find_possible_sequences(conflicting_frame_hashes, max_gap=1):
    frame_matches = get_frame_matches(conflicting_frame_hashes)
    pprint('frame_matches:')
    pprint(frame_matches)

    video_names = extract_video_names(conflicting_frame_hashes)
    sequences = identify_continuous_sequences(conflicting_frame_hashes, video_names, max_gap)
    possible_sequences = reorganize_sequences(sequences)

    # pprint('possible_sequences:')
    # pprint(possible_sequences)
    pt()
    return possible_sequences


if __name__ == "__main__":
    # conflicting_frame_hashes = {
    #     '0000003010000000': {'tiny_compiled_15a_normal.mkv': [8], 'tiny_compiled_15b_reverse.mkv': [29]},
    #     '0000409090848682': {'tiny_compiled_15a_normal.mkv': [9], 'tiny_compiled_15b_reverse.mkv': [30]},
    #     '0040c09090848686': {'tiny_compiled_15a_normal.mkv': [10], 'tiny_compiled_15b_reverse.mkv': [31]},
    #     '4040c09094848686': {'tiny_compiled_15a_normal.mkv': [11], 'tiny_compiled_15b_reverse.mkv': [32]},
    #     '4004c49094868686': {'tiny_compiled_15a_normal.mkv': [12], 'tiny_compiled_15b_reverse.mkv': [33]},
    #     'c8d4c4d49486c686': {'tiny_compiled_15a_normal.mkv': [14, 15], 'tiny_compiled_15b_reverse.mkv': [35, 36]},
    #     'd9d1c5d49486c696': {'tiny_compiled_15a_normal.mkv': [16], 'tiny_compiled_15b_reverse.mkv': [37]},
    #     'd9d5c5d49486c696': {'tiny_compiled_15a_normal.mkv': [17], 'tiny_compiled_15b_reverse.mkv': [38]},
    #     'd8d5c5d49486c696': {'tiny_compiled_15a_normal.mkv': [18, 20, 21], 'tiny_compiled_15b_reverse.mkv': [39, 41, 42]},
    #     'd8d5cdd49486c696': {'tiny_compiled_15a_normal.mkv': [19], 'tiny_compiled_15b_reverse.mkv': [40]},
    #     '1119999494849696': {'tiny_compiled_15a_normal.mkv': [22], 'tiny_compiled_15b_reverse.mkv': [43]},
    #     '7619a4cc4dc3788c': {'tiny_compiled_15a_normal.mkv': [28], 'tiny_compiled_15b_reverse.mkv': [10]},
    #     '7691644c4dcb788c': {'tiny_compiled_15a_normal.mkv': [29, 30, 31], 'tiny_compiled_15b_reverse.mkv': [11, 12, 13]},
    #     '7691654c4dcb788c': {'tiny_compiled_15a_normal.mkv': [32, 33, 34, 35, 36, 37, 38], 'tiny_compiled_15b_reverse.mkv': [14, 15, 16, 17, 18, 19, 20, 21]},
    #     '7691654c4dcb780c': {'tiny_compiled_15a_normal.mkv': [39, 40], 'tiny_compiled_15b_reverse.mkv': [22]}
    # }




    conflicting_frame_hashes = {
    '7619a4cc4dc3788c': {'compiled_tiny_original_15a.mkv': [6], 'compiled_tiny_original_15b.mkv': [47], 'compiled_tiny_original_15c.mkv': [25]},
    '7691644c4dcb788c': {'compiled_tiny_original_15a.mkv': [7, 8, 9], 'compiled_tiny_original_15b.mkv': [48, 49, 50], 'compiled_tiny_original_15c.mkv': [26, 27, 28]},
    '7691654c4dcb788c': {'compiled_tiny_original_15a.mkv': [10, 11, 12, 13, 14, 15], 'compiled_tiny_original_15b.mkv': [51, 52, 53, 54, 55, 56, 57, 58], 'compiled_tiny_original_15c.mkv': [29, 30, 31, 32, 33, 34]},
    '7691654c4dcb780c': {'compiled_tiny_original_15a.mkv': [16, 17, 18], 'compiled_tiny_original_15b.mkv': [59], 'compiled_tiny_original_15c.mkv': [35, 36, 37]},
    '24010080808582cb': {'compiled_tiny_original_15a.mkv': [23, 34], 'compiled_tiny_original_15b.mkv': [4, 35], 'compiled_tiny_original_15c.mkv': [42, 53]},
    '24010000808582cb': {'compiled_tiny_original_15a.mkv': [24, 25, 35, 36], 'compiled_tiny_original_15b.mkv': [5, 6, 36, 37], 'compiled_tiny_original_15c.mkv': [43, 44, 54, 55]},
    '24000000808582cb': {'compiled_tiny_original_15a.mkv': [26, 27, 28, 29, 37, 38, 39], 'compiled_tiny_original_15b.mkv': [7, 8, 9, 38, 39, 40, 41], 'compiled_tiny_original_15c.mkv': [45, 46, 48, 56, 57, 59]},
    '24000000808582ca': {'compiled_tiny_original_15a.mkv': [30, 40, 41], 'compiled_tiny_original_15b.mkv': [10, 11, 42], 'compiled_tiny_original_15c.mkv': [49, 60]},
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
    
    max_gap = 1  ## Num of frames allowed between discovered matching frames, to be included in the same sequence
    possible_sequences = find_possible_sequences(conflicting_frame_hashes, max_gap)
    rprint('conflicting_frame_hashes:')
    rprint(conflicting_frame_hashes)
    rprint('possible_sequences:')
    rprint(possible_sequences)



'''

possible_sequences:
{
    'sequence 0': {'compiled_tiny_original_15b.mkv': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 'compiled_tiny_original_15c.mkv': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37], 'compiled_tiny_original_15a.mkv': [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]},        
    'sequence 1': {
        'compiled_tiny_original_15b.mkv': [4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 36, 37, 38, 39, 40, 41, 42],
        'compiled_tiny_original_15c.mkv': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 42, 43, 44, 45, 46, 48, 49, 53, 54, 55, 56, 57, 59, 60],
        'compiled_tiny_original_15a.mkv': [23, 24, 25, 26, 27, 28, 29, 30, 34, 35, 36, 37, 38, 39, 40, 41]
    },
    'sequence 2': {'compiled_tiny_original_15b.mkv': [46], 'compiled_tiny_original_15c.mkv': [24], 'compiled_tiny_original_15a.mkv': []}
}


'''