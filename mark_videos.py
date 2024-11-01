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

def create_new_chapters(sequences, frame_rate, total_duration_ms, existing_chapters, add_cuts=False, add_plays=True, enabled=True, skip_chapters=False):
    new_chapters = []
    cut_index = len(existing_chapters)  # Start indexing cuts from the end of existing chapters

    if add_cuts:
        for sequence_name, time_frame in sequences.items():
            for i in range(len(time_frame)//2):
                start_ms = calculate_time_in_ms(time_frame[2*i], frame_rate)
                end_ms = calculate_time_in_ms(time_frame[2*i + 1], frame_rate)
                new_chapters.append({
                    'id': f'cut_{cut_index + 1}',
                    'start_time': str(start_ms),
                    'end_time': str(end_ms),
                    'enabled': enabled,
                    'skip': skip_chapters
                })
                cut_index += 1  # Increment cut index for each new cut

    # Sort all chapters (existing and new) by start time
    all_chapters = sorted(existing_chapters + new_chapters, key=lambda x: int(x['start_time']))

    if add_plays:
        last_end_time = 0
        play_index = 1
        for chapter in all_chapters:
            start_time = int(chapter['start_time'])
            if last_end_time < start_time:
                # Add a play chapter in the gap
                new_chapters.append({
                    'id': f'play_{play_index}',
                    'start_time': str(last_end_time),
                    'end_time': str(start_time),
                    'enabled': enabled,
                    'skip': skip_chapters
                })
                play_index += 1
            last_end_time = max(last_end_time, int(chapter['end_time']))

        # Check if there's remaining time after the last chapter
        if last_end_time < total_duration_ms:
            new_chapters.append({
                'id': f'play_{play_index}',
                'start_time': str(last_end_time),
                'end_time': str(total_duration_ms),
                'enabled': enabled,
                'skip': skip_chapters
            })

    return new_chapters

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

def mark_videos(series_dict, video_based_sequences, output_to_new_file=True, enabled=False, skip_chapters=False):
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
        print_metadata_for_videos_path(output_path, chapters=False, editions=True, all_metadata=False)
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
    
    simplified_possible_conflicting_sequences = {
        'sequence 0': {'_s01e01_40.mp4': [2, 16], '_s01e02_40.mp4': [2, 16], '_s01e03_40.mp4': [3, 17], '_s01e04_40.mp4': [4, 18]},
        'sequence 1': {'_s01e01_40.mp4': [34, 39], '_s01e02_40.mp4': [21, 23], '_s01e03_40.mp4': [22, 24], '_s01e04_40.mp4': [23, 24]},
        'sequence 2': {'_s01e01_40.mp4': [25, 29], '_s01e02_40.mp4': [35, 39], '_s01e03_40.mp4': [36, 40], '_s01e04_40.mp4': [37, 41]},
        'sequence 3': {'_s01e01_40.mp4': [43, 47], '_s01e02_40.mp4': [26, 30], '_s01e03_40.mp4': [27, 31], '_s01e04_40.mp4': [28, 32]},
        'sequence 4': {'_s01e01_40.mp4': [52, 56], '_s01e02_40.mp4': [43, 48], '_s01e03_40.mp4': [44, 48], '_s01e04_40.mp4': [45, 49]},
        'sequence 5': {'_s01e01_40.mp4': [65, 69], '_s01e02_40.mp4': [53, 57], '_s01e03_40.mp4': [53, 57], '_s01e04_40.mp4': [54, 58]},
        'sequence 6': {'_s01e01_40.mp4': [74, 78], '_s01e02_40.mp4': [66, 70], '_s01e03_40.mp4': [66, 70], '_s01e04_40.mp4': [67, 86]},
        'sequence 7': {'_s01e01_40.mp4': [80, 94], '_s01e02_40.mp4': [74, 91], '_s01e03_40.mp4': [90, 94], '_s01e04_40.mp4': [90, 94]},
    }
    
    video_based_sequences = restructure_sequences(simplified_possible_conflicting_sequences)
    mark_videos(series, video_based_sequences)

if __name__ == "__main__":

    test_marking_of_videos()


'''



'''