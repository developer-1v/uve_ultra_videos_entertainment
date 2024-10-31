from print_tricks import pt

import os
import subprocess
import json
import ffmpeg

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

def print_video_chapters(chapters):
    if chapters:
        print("Existing chapters:")
        for chapter in chapters:
            print(f"Chapter {chapter['id']}: Start {chapter['start_time']}, End {chapter['end_time']}, Disabled: {chapter.get('disabled', 'no')}")
    else:
        print("No chapters found.")

def restructure_sequences(sequences):
    video_based_dict = {}
    for sequence_name, videos in sequences.items():
        for video_name, time_frame in videos.items():
            if video_name not in video_based_dict:
                video_based_dict[video_name] = {}
            video_based_dict[video_name][sequence_name] = time_frame
    pt(video_based_dict)
    return video_based_dict

def mark_videos(series_dict, video_based_sequences, output_to_new_file=True):
    for video_name, sequences in video_based_sequences.items():
        video_path = find_matching_video_path(series_dict, video_name)
        if video_path is None:
            print(f"Video file not found for name: {video_name}")
            continue
        existing_chapters = get_video_chapters(video_path)
        
        # Debugging: Print existing chapters
        print(f"Existing chapters for {video_name}: {existing_chapters}")
        
        # Process each sequence for the current video
        for sequence_name, time_frame in sequences.items():
            new_chapters = [{'id': f'cut_{len(existing_chapters) + i + 1}', 'start_time': str(time_frame[0]), 'end_time': str(time_frame[1]), 'disabled': 'yes'} for i in range(len(time_frame)//2)]
            existing_chapters = merge_chapters(existing_chapters, new_chapters)
        
        # Debugging: Print new chapters to be added
        print(f"New chapters to be added for {video_name}: {existing_chapters}")
        
        # After processing all sequences, determine the output path
        if output_to_new_file:
            output_path = os.path.join(os.path.dirname(video_path), f"marked_{os.path.basename(video_path)}")
        else:
            output_path = video_path  # Overwrite the original file

        # Ensure chapters are formatted correctly for ffmpeg
        chapter_metadata = ';'.join([f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(float(chap['start_time']) * 1000)}\nEND={int(float(chap['end_time']) * 1000)}\ntitle={chap['id']}\n" for chap in existing_chapters])

        # Debugging: Print final chapter metadata
        print(f"Final chapter metadata for {video_name}: {chapter_metadata}")

        # Process the video with ffmpeg, including chapters
        try:
            ffmpeg.input(video_path) \
                .output(output_path, map='0', map_metadata='0', 
                        codec='copy', format='matroska', loglevel='error',
                        **{'metadata:g': chapter_metadata}) \
                .run(overwrite_output=True)
        except ffmpeg.Error as e:
            print(f"Failed to process video {video_path}: {e}")
        
        print(f"Updated chapters written to {output_path} for video {video_name}")

        # Print the updated chapter metadata
        updated_chapters = get_video_chapters(output_path)
        print(f"Updated chapters for {video_name}: {updated_chapters}")
        print_video_chapters(updated_chapters)


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
{'3_complete_vids_to_test': {'3_complete_vids_to_test': ['C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\3_complete_vids_to_test\\_s01e01_40.mp4',
    C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\3_complete_vids_to_test\\_s01e02_40.mp4', 'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\3_complete_vids_to_test\\_s01e03_40.mp4',
    'C:\\.PythonProjects\\uve_ultra_videos_entertainment\\videos_for_testing\\tiny_vids\\3_complete_vids_to_test\\_s01e04_40.mp4']}}

'C:/.PythonProjects/uve_ultra_videos_entertainment/videos_for_testing/tiny_vids/3_complete_vids_to_test
'''