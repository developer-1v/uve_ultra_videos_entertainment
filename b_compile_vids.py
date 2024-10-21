import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

from print_tricks import pt
from rich import print as rprint

import os
from moviepy.editor import VideoFileClip

def extract_and_save_subclip(video_path, start_frame, end_frame, sequence_index):
    try:
        with VideoFileClip(video_path) as clip:
            # Calculate start and end times in seconds
            start_time = start_frame / clip.fps
            end_time = end_frame / clip.fps
            
            # Ensure the times are within the clip's duration
            if start_time < clip.duration and end_time <= clip.duration:
                # Extract the subclip
                subclip = clip.subclip(start_time, end_time)
                
                # Define the output path using a valid file name
                video_name = os.path.basename(video_path)
                output_path = f"clip_{sequence_index + 1:02d}({start_frame}_{end_frame})_{video_name}"
                
                # Write the subclip to a file
                subclip.write_videofile(output_path, codec='libx264', audio_codec='aac')
                print(f"Subclip saved to {output_path}")
            else:
                print(f"Invalid time range for frames {start_frame}-{end_frame}.")
    except Exception as e:
        print(f"Error processing {video_path}: {e}")

def convert_dict_to_frame_ranges(video_dict):
    frame_ranges = []
    for sequence, videos in video_dict.items():
        for video_name, frames in videos.items():
            # Verify that frames are sequential
            if all(frames[i] + 1 == frames[i + 1] for i in range(len(frames) - 1)):
                # Add the min and max as the start and end frames
                frame_ranges.append((video_name, frames[0], frames[-1]))
            else:
                print(f"Error: Frames for {video_name} in {sequence} are not sequential.")
    return frame_ranges

def compile_videos_from_dict(video_dict, original_video_paths, output_path='test_compiled_video.mp4', per_sequence=False):
    for sequence_index, (sequence_name, videos) in enumerate(video_dict.items()):
        for video_name, frames in videos.items():
            # Check if frames list is not empty
            if not frames:
                print(f"Warning: No frames found for {video_name} in {sequence_name}. Skipping.")
                continue

            for video_path in original_video_paths:
                if os.path.basename(video_path) == video_name:
                    start_frame = frames[0]
                    end_frame = frames[-1]
                    extract_and_save_subclip(video_path, start_frame, end_frame, sequence_index)


if __name__ == "__main__":
    
    original_video_paths = [
        'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15a_normal.mkv',
        'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15b_reverse.mkv'
    ]

    video_dict = {
        'sequence_0': {
            'tiny_compiled_15b_reverse.mkv': [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
            'tiny_compiled_15a_normal.mkv': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        },
        'sequence_1': {
            'tiny_compiled_15b_reverse.mkv': [10, 11, 12, 13, 14, 15, 16, 17, 18],
            'tiny_compiled_15a_normal.mkv': [28, 29, 30, 31, 32, 33, 34, 35, 36]
        }
    }
    
    compile_videos_from_dict(video_dict, original_video_paths, output_path='test_compiled_video.mp4', per_sequence=False)

# if __name__ == "__main__":
    # video_dict = {
    #     'sequence_0': {
    #         'tiny_compiled_15b_reverse.mkv': [29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    #         'tiny_compiled_15a_normal.mkv': [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    #     },
    #     'sequence_1': {
    #         'tiny_compiled_15b_reverse.mkv': [10, 11, 12, 13, 14, 15, 16, 17, 18],
    #         'tiny_compiled_15a_normal.mkv': [28, 29, 30, 31, 32, 33, 34, 35, 36]
    #     }
    # }

#     original_video_paths = [
#         'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15a_normal.mkv',
#         'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15b_reverse.mkv'
#     ]

#     compile_videos_from_dict(video_dict, original_video_paths, output_path='test_compiled_video.mp4', per_sequence=False)
