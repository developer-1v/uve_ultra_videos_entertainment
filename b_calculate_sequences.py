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

def identify_continuous_sequences(conflicting_frame_hashes, video_names, max_gap=1):
    def can_extend_sequence(current_sequence, frames, max_gap):
        for video in video_names:
            if current_sequence[video]:
                last_frame = max(current_sequence[video])
                if frames[video] and min(frames[video]) > last_frame + max_gap:
                    return False
        return True

    def extend_sequence(current_sequence, frames):
        for video in video_names:
            if frames[video]:
                current_sequence[video].extend(frames[video])

    def finalize_sequence(current_sequence):
        for video in video_names:
            current_sequence[video] = sorted(set(current_sequence[video]))

    sequences = []
    current_sequence = {video: [] for video in video_names}

    for index, (key, value) in enumerate(conflicting_frame_hashes.items()):
        frames = {video: value.get(video, []) for video in video_names}

        if can_extend_sequence(current_sequence, frames, max_gap):
            extend_sequence(current_sequence, frames)
        else:
            if any(current_sequence[video] for video in video_names):
                finalize_sequence(current_sequence)
                sequences.append(current_sequence.copy())
            current_sequence = {video: [] for video in video_names}  # Reset current_sequence
            extend_sequence(current_sequence, frames)

    if any(current_sequence[video] for video in video_names):
        finalize_sequence(current_sequence)
        sequences.append(current_sequence)

    # Merge sequences that can be combined
    merged_sequences = []
    for seq in sequences:
        if not merged_sequences:
            merged_sequences.append(seq)
        else:
            last_seq = merged_sequences[-1]
            if can_extend_sequence(last_seq, seq, max_gap):
                extend_sequence(last_seq, seq)
                finalize_sequence(last_seq)
            else:
                merged_sequences.append(seq)

    # Ensure sequences are in the order of video_names
    ordered_sequences = []
    for seq in merged_sequences:
        ordered_seq = {video: seq[video] for video in video_names}
        ordered_sequences.append(ordered_seq)

    return ordered_sequences


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
    conflicting_frame_hashes = {
        '0000003010000000': {'tiny_compiled_15a_normal.mkv': [8], 'tiny_compiled_15b_reverse.mkv': [29]},
        '0000409090848682': {'tiny_compiled_15a_normal.mkv': [9], 'tiny_compiled_15b_reverse.mkv': [30]},
        '0040c09090848686': {'tiny_compiled_15a_normal.mkv': [10], 'tiny_compiled_15b_reverse.mkv': [31]},
        '4040c09094848686': {'tiny_compiled_15a_normal.mkv': [11], 'tiny_compiled_15b_reverse.mkv': [32]},
        '4004c49094868686': {'tiny_compiled_15a_normal.mkv': [12], 'tiny_compiled_15b_reverse.mkv': [33]},
        'c8d4c4d49486c686': {'tiny_compiled_15a_normal.mkv': [14, 15], 'tiny_compiled_15b_reverse.mkv': [35, 36]},
        'd9d1c5d49486c696': {'tiny_compiled_15a_normal.mkv': [16], 'tiny_compiled_15b_reverse.mkv': [37]},
        'd9d5c5d49486c696': {'tiny_compiled_15a_normal.mkv': [17], 'tiny_compiled_15b_reverse.mkv': [38]},
        'd8d5c5d49486c696': {'tiny_compiled_15a_normal.mkv': [18, 20, 21], 'tiny_compiled_15b_reverse.mkv': [39, 41, 42]},
        'd8d5cdd49486c696': {'tiny_compiled_15a_normal.mkv': [19], 'tiny_compiled_15b_reverse.mkv': [40]},
        '1119999494849696': {'tiny_compiled_15a_normal.mkv': [22], 'tiny_compiled_15b_reverse.mkv': [43]},
        '7619a4cc4dc3788c': {'tiny_compiled_15a_normal.mkv': [28], 'tiny_compiled_15b_reverse.mkv': [10]},
        '7691644c4dcb788c': {'tiny_compiled_15a_normal.mkv': [29, 30, 31], 'tiny_compiled_15b_reverse.mkv': [11, 12, 13]},
        '7691654c4dcb788c': {'tiny_compiled_15a_normal.mkv': [32, 33, 34, 35, 36, 37, 38], 'tiny_compiled_15b_reverse.mkv': [14, 15, 16, 17, 18, 19, 20, 21]},
        '7691654c4dcb780c': {'tiny_compiled_15a_normal.mkv': [39, 40], 'tiny_compiled_15b_reverse.mkv': [22]}
    }

    max_gap = 1  ## Num of frames allowed between discovered matching frames, to be included in the same sequence
    possible_sequences = find_possible_sequences(conflicting_frame_hashes, max_gap)
    rprint('conflicting_frame_hashes:')
    rprint(conflicting_frame_hashes)
    rprint('possible_sequences:')
    rprint(possible_sequences)
