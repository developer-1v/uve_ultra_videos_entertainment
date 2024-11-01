from print_tricks import pt
from utility_read_metadata import print_metadata_for_videos_path

import os
import subprocess
import json
pt.t()
import ffmpeg
pt.t()


def get_video_chapters(video_path):
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'chapter', 
        '-print_format', 'json', 
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        pt()
        print(f"Error reading chapters: {result.stderr.decode()}")
    chapters = json.loads(result.stdout)
    return chapters.get('chapters', [])



def merge_chapters(existing_chapters, new_chapters):
    # Combine existing and new chapters
    combined_chapters = existing_chapters + new_chapters
    
    # Sort chapters by start time to maintain order
    combined_chapters.sort(key=lambda x: float(x['start_time']))
    
    # Here you could add additional logic to handle overlapping chapters if necessary
    return combined_chapters 

def find_matching_video_path(series_dict, video_name):
    for series_name, nested_dict in series_dict.items():
        for sub_series_name, video_paths in nested_dict.items():
            for path in video_paths:
                if os.path.basename(path) == video_name:
                    return path
    return None


def restructure_sequences(sequences):
    video_based_dict = {}
    for sequence_name, videos in sequences.items():
        for video_name, time_frame in videos.items():
            if video_name not in video_based_dict:
                video_based_dict[video_name] = {}
            video_based_dict[video_name][sequence_name] = time_frame
    pt(video_based_dict)
    return video_based_dict


def calculate_time_in_ms(frame_number, frame_rate):
    return int((frame_number / frame_rate) * 1000)



import cv2

def get_video_properties(video_path):
    """
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Error: Could not open video.")
        return None, None

    frame_rate = video.get(cv2.CAP_PROP_FPS)
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    duration_ms = int((frames / frame_rate) * 1000) if frame_rate > 0 else None

    video.release()
    return frame_rate, duration_ms

def create_clips_to_play(sequences_to_cut):
    '''
    Take a list of sequences to cut, and get the frames surrounding it to 
    obtain the list of frames that should play. 
    
    '''
    chapters_to_play = {}
    
    for video_name, sequences in sequences_to_cut.items():
        # Get all sequence ranges and sort them by start frame
        seq_ranges = []
        for seq in sequences.values():
            seq_ranges.append(seq)
        seq_ranges.sort(key=lambda x: x[0])
        
        # Find the gaps
        gaps = []
        
        # Add gap before first sequence if needed
        if seq_ranges[0][0] > 1:
            gaps.append([1, seq_ranges[0][0] - 1])
        
        # Find gaps between sequences
        for i in range(len(seq_ranges) - 1):
            current_end = seq_ranges[i][1]
            next_start = seq_ranges[i + 1][0]
            if current_end + 1 < next_start:
                gaps.append([current_end + 1, next_start - 1])
        
        chapters_to_play[video_name] = gaps
    
    return chapters_to_play

def create_chapter_entries(sequences, prefix, start_index, enabled, skip_chapters, frame_rate=None):
    """Creates chapter entries with given prefix ('cut_' or 'play_')"""
    chapters = []
    current_index = start_index
    
    for sequence_name, time_frame in sequences.items():
        # Convert frames to ms if frame_rate is provided
        if frame_rate:
            start_time = calculate_time_in_ms(time_frame[0], frame_rate)
            end_time = calculate_time_in_ms(time_frame[1], frame_rate)
        else:
            # If no frame_rate, assume time_frame is already in ms
            start_time = time_frame[0]
            end_time = time_frame[1]
            
        chapters.append({
            'id': f'{prefix}{current_index}',
            'start_time': str(start_time),
            'end_time': str(end_time),
            'enabled': enabled,
            'skip': skip_chapters
        })
        current_index += 1
    
    return sorted(chapters, key=lambda x: int(x['start_time']))

def create_new_chapters(sequences, frame_rate, total_duration_ms, existing_chapters, add_cuts=True, add_plays=True, enabled=True, skip_chapters=False):
    new_chapters = []
    start_index = len(existing_chapters) + 1

    # Handle cut chapters
    if add_cuts:
        cut_chapters = create_chapter_entries(
            sequences, 
            'cut_', 
            start_index, 
            enabled, 
            skip_chapters,
            frame_rate
        )
        new_chapters.extend(cut_chapters)

    # Handle play chapters
    if add_plays:
        # Convert sequences to play sequences
        play_sequences = create_clips_to_play({f"video": sequences})["video"]
        # Convert to dictionary with sequence names
        play_dict = {f"play_{i}": gap for i, gap in enumerate(play_sequences, 1)}
        
        play_chapters = create_chapter_entries(
            play_dict,
            'play_',
            1,  # Always start play index from 1
            enabled,
            skip_chapters,
            frame_rate
        )
        new_chapters.extend(play_chapters)

    return sorted(new_chapters, key=lambda x: int(x['start_time']))


def apply_chapter_metadata(video_path, existing_chapters, output_to_new_file):
    edition_entry = f"[EDITION_ENTRY]\nEDITION_FLAG_DEFAULT=1\nEDITION_FLAG_ORDERED=1\n"
    chapter_metadata = edition_entry + ';'.join([
        f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(float(chap['start_time']))}\nEND={int(float(chap['end_time']))}\n"
        f"title={chap['id']}\nenabled={chap['enabled']}\nskip={chap['skip']}"
        for chap in existing_chapters
    ])

    if output_to_new_file:
        output_path = os.path.join(os.path.dirname(video_path), f"marked_{os.path.basename(video_path)}")
    else:
        output_path = video_path  # Overwrite the original file

    try:
        ffmpeg.input(video_path) \
            .output(output_path, map='0', map_metadata='0', 
                    codec='copy', format='matroska', loglevel='error',
                    **{'metadata:g': chapter_metadata}) \
            .run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"Failed to process video {video_path}: {e}")
    
    return output_path

def mark_videos(series_dict, video_based_sequences, output_to_new_file=True, enabled=False):
    for video_name, sequences in video_based_sequences.items():
        video_path = find_matching_video_path(series_dict, video_name)
        if video_path is None:
            print(f"Video file not found for name: {video_name}")
            continue

        frame_rate, total_duration_ms = get_video_properties(video_path)
        if frame_rate is None:
            print(f"Could not retrieve frame rate for video {video_path}")
            continue

        existing_chapters = get_video_chapters(video_path)
        print(f"Initial chapters for {video_name}: {existing_chapters}")

        new_chapters = create_new_chapters(sequences, frame_rate, total_duration_ms, existing_chapters)
        existing_chapters = merge_chapters(existing_chapters, new_chapters)
        print(f"Combined chapters for {video_name}: {existing_chapters}")

        output_path = apply_chapter_metadata(video_path, existing_chapters, output_to_new_file)
        print(f"Updated chapters written to {output_path} for video {video_name}")

        updated_chapters = get_video_chapters(output_path)
        print(f"Updated chapters for {video_name}: {updated_chapters}")
        print_metadata_for_videos_path(output_path, editions=True, all_metadata=False)
        pt.ex()

def test_marking_of_videos():
    from b_main import find_seasons
    
    test_full_vids = False
    if test_full_vids:
        series_path = fr'C:\Users\user\Downloads\_Tor\[Sokudo] Boku no Hero Academia [1080p BD][AV1][dual audio]\_vids_for_python_automatic_editing'
    else:
        main_folder = 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\'
        # series_path = os.path.join(main_folder, 'compiled_tiny_videos_for_testing', 'compiled')
        series_path = os.path.join(main_folder, 'tiny_vids','3_complete_vids_to_test')

        
    series = find_seasons(series_path)
    pt(series)
    # pt.ex()
    
    video_based_sequences = {
        '_s01e01_40.mp4': {'sequence 0': [2, 16], 'sequence 1': [34, 39], 'sequence 2': [25, 29], 'sequence 3': [43, 47], 'sequence 4': [52, 56], 'sequence 5': [65, 69], 'sequence 6': [74, 78], 'sequence 7': [80, 94]},
        '_s01e02_40.mp4': {'sequence 0': [2, 16], 'sequence 1': [21, 23], 'sequence 2': [35, 39], 'sequence 3': [26, 30], 'sequence 4': [43, 48], 'sequence 5': [53, 57], 'sequence 6': [66, 70], 'sequence 7': [74, 91]},
        '_s01e03_40.mp4': {'sequence 0': [3, 17], 'sequence 1': [22, 24], 'sequence 2': [36, 40], 'sequence 3': [27, 31], 'sequence 4': [44, 48], 'sequence 5': [53, 57], 'sequence 6': [66, 70], 'sequence 7': [90, 94], 'sequence 8': [73, 87]},
        '_s01e04_40.mp4': {'sequence 0': [4, 18], 'sequence 1': [23, 24], 'sequence 2': [37, 41], 'sequence 3': [28, 32], 'sequence 4': [45, 49], 'sequence 5': [54, 58], 'sequence 6': [67, 86], 'sequence 7': [90, 94]}
    }
    
    mark_videos(series, video_based_sequences)

if __name__ == "__main__":

    test_marking_of_videos()


'''



'''