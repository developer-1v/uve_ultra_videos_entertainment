from print_tricks import pt
from rich import print as rprint
from utility_read_metadata import print_metadata_for_videos_path

import os
import cv2

import subprocess
import json
import ffmpeg



def video_based_sequences_restructurer(sequences):
    video_based_dict = {}
    for sequence_name, videos in sequences.items():
        for video_name, time_frame in videos.items():
            if video_name not in video_based_dict:
                video_based_dict[video_name] = {}
            video_based_dict[video_name][sequence_name] = time_frame
    pt(video_based_dict)
    return video_based_dict

import subprocess
import json

def get_video_chapters(video_path, edition_name=None):
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'format', 
        '-print_format', 'json', 
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stderr:
        pt()
        print(f"Error reading chapters: {result.stderr.decode()}")
    
    metadata = json.loads(result.stdout)
    tags = metadata['format'].get('tags', {})
    edition_data = tags.get('[EDITION_ENTRY]\nEDITION_FLAG_DEFAULT', '')

    # Parse the edition data
    editions = edition_data.split(';')
    chapters = []

    for edition in editions:
        if edition_name and edition_name not in edition:
            continue
        
        chapter_lines = edition.split('\n')
        chapter_dict = {}
        for line in chapter_lines:
            if '=' in line:
                k, v = line.split('=', 1)
                chapter_dict[k.strip()] = v.strip()
        
        if chapter_dict:
            chapters.append(chapter_dict)
    
    pt(chapters)
    # if len(chapters) != 0:
    #     pt.ex()
    return chapters

def merge_chapters(existing_chapters, new_chapters):
    # pt()
    # if pt.r(loops=8):
    #     pt(existing_chapters, new_chapters)
    #     pt.ex()
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

def calculate_time_in_ms(frame_number, frame_rate):
    return int((frame_number / frame_rate) * 1000)

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
    # Initialize the dictionary to store play sequences
    play_sequences = {}
    # Sort sequences by their start frame
    sorted_sequences = sorted(sequences_to_cut.items(), key=lambda x: x[1][0])
    
    # Initialize the start of the first play sequence
    current_play_start = 1
    
    for i, (sequence_name, frames) in enumerate(sorted_sequences):
        start_frame, end_frame = frames
        # Create a play sequence before the current sequence if there is a gap
        if current_play_start < start_frame:
            play_sequences[f'play_{i}'] = [current_play_start, start_frame - 1]
        # Update the start for the next play sequence
        current_play_start = end_frame + 1
    
    # Check if there's a need for a final play sequence after the last sequence
    if current_play_start <= sorted_sequences[-1][1][1]:
        play_sequences[f'play_{len(sorted_sequences)}'] = [current_play_start, sorted_sequences[-1][1][1]]
    
    rprint('play sequences')
    rprint(play_sequences)
    return play_sequences

def convert_frames_to_timestamps(start_frame, end_frame, frame_rate):
    """Converts frame numbers to timestamps in milliseconds."""
    start_time = calculate_time_in_ms(start_frame, frame_rate)
    end_time = calculate_time_in_ms(end_frame, frame_rate)
    return start_time, end_time

def create_chapter_entries(sequences, prefix, start_index, enabled, skip_chapters):
    """Creates chapter entries with given prefix ('cut_' or 'play_')"""
    chapters = []
    current_index = start_index
    
    for sequence_name, time_frame in sequences.items():
        start_time, end_time = time_frame  # Assume sequences are already in timestamp format
        
        chapters.append({
            'id': f'{prefix}{current_index}',
            'start_time': str(start_time),
            'end_time': str(end_time),
            'enabled': enabled,
            'skip': skip_chapters
        })
        current_index += 1
    
    return sorted(chapters, key=lambda x: int(x['start_time']))

def determine_output_path(video_path, output_to_new_file):
    if output_to_new_file:
        return os.path.join(os.path.dirname(video_path), f"marked_{os.path.basename(video_path)}")
    else:
        return video_path  # Overwrite the original file

def apply_chapter_metadata(input_video_path, output_video_path, chapters_metadata):
    try:
        ffmpeg.input(input_video_path) \
            .output(output_video_path, map='0', map_metadata='0', 
                    codec='copy', format='matroska', loglevel='error',
                    **{'metadata:g': chapters_metadata}) \
            .run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"Failed to process video {input_video_path}: {e}")

def convert_sequences_of_frames_to_timestamps(video_based_frame_sequences, frame_rates):
    """Converts all sequences from frames to timestamps for each video."""
    video_based_timestamp_sequences = {}
    for video_name, sequences in video_based_frame_sequences.items():
        frame_rate = frame_rates.get(video_name)
        if frame_rate:
            timestamp_sequences = {}
            for sequence_name, frames in sequences.items():
                start_frame, end_frame = frames
                start_time, end_time = convert_frames_to_timestamps(start_frame, end_frame, frame_rate)
                timestamp_sequences[sequence_name] = (start_time, end_time)
            video_based_timestamp_sequences[video_name] = timestamp_sequences
        else:
            print(f"No frame rate available for {video_name}")
    # pt(video_based_timestamp_sequences)
    # pt.ex()
    return video_based_timestamp_sequences

def get_frame_rates_for_videos(video_paths):
    """Fetches the frame rate for each video in the provided dictionary of video paths."""
    frame_rates = {}
    for video_name, video_path in video_paths.items():
        frame_rate, _ = get_video_properties(video_path)
        if frame_rate is not None:
            frame_rates[video_name] = frame_rate
        else:
            print(f"Could not retrieve frame rate for video {video_path}")
    return frame_rates

def get_video_paths_from_series_dict(series_dict):
    video_paths = {}
    for series_name, nested_dict in series_dict.items():
        for sub_series_name, paths in nested_dict.items():
            for path in paths:
                video_name = os.path.basename(path)
                video_paths[video_name] = path
    return video_paths

def generate_chapter_metadata(existing_chapters):
    """
    Applies chapter metadata to a video file using ffmpeg.
    
    Args:
    video_path (str): Path to the video file.
    existing_chapters (list of dicts): List of chapter dictionaries with 'start_time', 'end_time', 'id', 'enabled', and 'skip' keys.
    output_to_new_file (bool): Flag to determine if the metadata should be applied to a new file or overwrite the existing one.
    """
    # Edition entry to set chapters as default and ordered
    edition_entry = (
        "[EDITION_ENTRY]\n"
        "EDITION_FLAG_DEFAULT=1\n"
        "EDITION_FLAG_ORDERED=1\n"
    )
    
    # Generate chapter metadata entries
    chapter_entries = []
    for chapter in existing_chapters:
        chapter_entry = (
            "[CHAPTER]\n"
            f"TIMEBASE=1/1000\n"
            f"START={int(float(chapter['start_time']))}\n"
            f"END={int(float(chapter['end_time']))}\n"
            f"title={chapter['id']}\n"
            f"enabled={int(chapter['enabled'])}\n"
            f"skip={int(chapter['skip'])}\n"
        )
        chapter_entries.append(chapter_entry)
    
    # Combine edition entry with all chapter entries
    chapter_metadata = edition_entry + ';'.join(chapter_entries)
    
    return chapter_metadata

def mark_videos(video_based_sequences, video_paths, prefix='_cut_', output_to_new_file=True, enabled=False):
    # list_of_initial_chapters = []
    results = []
    for video_name, sequences in video_based_sequences.items():
        video_path = video_paths.get(video_name)
        if video_path is None:
            print(f"Video file not found for name: {video_name}")
            continue

        frame_rate, total_duration_ms = get_video_properties(video_path)
        if frame_rate is None:
            print(f"Could not retrieve frame rate for video {video_path}")
            continue

        initial_chapters = get_video_chapters(video_path)
        pt(initial_chapters)
        # list_of_initial_chapters.append(initial_chapters)
        new_chapters = create_chapter_entries(sequences, prefix, len(initial_chapters) + 1, enabled, False)
        merged_chapters = merge_chapters(initial_chapters, new_chapters)
        pt(initial_chapters, new_chapters, merged_chapters)

        output_path = determine_output_path(video_path, output_to_new_file)
        chapter_metadata = generate_chapter_metadata(merged_chapters)
        apply_chapter_metadata(video_path, output_path, chapter_metadata)

        updated_chapters = get_video_chapters(output_path)
        
        results.append({
            "video_name": video_name,
            "output_path": output_path,
            "updated_chapters": updated_chapters
        })
    # pt(list_of_initial_chapters)
    return results



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
    
    video_based_frame_sequences = {
        '_s01e01_40.mp4': {'sequence 0': [2, 16], 'sequence 1': [34, 39], 'sequence 2': [25, 29], 'sequence 3': [43, 47], 'sequence 4': [52, 56], 'sequence 5': [65, 69], 'sequence 6': [74, 78], 'sequence 7': [80, 94]},
        '_s01e02_40.mp4': {'sequence 0': [2, 16], 'sequence 1': [21, 23], 'sequence 2': [35, 39], 'sequence 3': [26, 30], 'sequence 4': [43, 48], 'sequence 5': [53, 57], 'sequence 6': [66, 70], 'sequence 7': [74, 91]},
        '_s01e03_40.mp4': {'sequence 0': [3, 17], 'sequence 1': [22, 24], 'sequence 2': [36, 40], 'sequence 3': [27, 31], 'sequence 4': [44, 48], 'sequence 5': [53, 57], 'sequence 6': [66, 70], 'sequence 7': [90, 94], 'sequence 8': [73, 87]},
        '_s01e04_40.mp4': {'sequence 0': [4, 18], 'sequence 1': [23, 24], 'sequence 2': [37, 41], 'sequence 3': [28, 32], 'sequence 4': [45, 49], 'sequence 5': [54, 58], 'sequence 6': [67, 86], 'sequence 7': [90, 94]}
    }
    
    video_paths = get_video_paths_from_series_dict(series)
    
    frame_based_results = mark_videos(video_based_frame_sequences, video_paths, prefix='__cut_frames_')
    for frame_result in frame_based_results:
        print_metadata_for_videos_path(frame_result['output_path'], editions=True, all_metadata=False)
        break
    
    frame_rates = get_frame_rates_for_videos(video_paths)
    video_based_timestamp_sequences = convert_sequences_of_frames_to_timestamps(video_based_frame_sequences, frame_rates)
    timestamp_based_results = mark_videos(video_based_timestamp_sequences, video_paths, prefix='__cut_timestamps_')
    # pt.ex()
    
    for timestamp_result in timestamp_based_results:
        print_metadata_for_videos_path(timestamp_result['output_path'], editions=True, all_metadata=False)
        break
        
    pt(video_based_frame_sequences, video_based_timestamp_sequences)

    pt(1)
    print_metadata_for_videos_path(frame_based_results[0]['output_path'], editions=True, all_metadata=False)
    pt(2)
    print_metadata_for_videos_path(timestamp_based_results[0]['output_path'], editions=True, all_metadata=False)
if __name__ == "__main__":

    test_marking_of_videos()


'''



'''