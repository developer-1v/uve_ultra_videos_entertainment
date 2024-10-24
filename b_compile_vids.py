import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

from print_tricks import pt
from rich import print as rprint

import os
from moviepy.editor import VideoFileClip

def extract_and_save_subclip(video_path, start_frame, end_frame, sequence_index, output_path):
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
                output_path = os.path.join(output_path, f"clip_{sequence_index}({start_frame}_{end_frame})_{video_name}")
                
                # Write the subclip to a file
                subclip.write_videofile(output_path, codec='libx264', audio_codec='aac')
                print(f"Subclip saved to {output_path}")
            else:
                print(f"Invalid time range for frames {start_frame}-{end_frame}.")
    except Exception as e:
        print(f"Error processing {video_path}: {e}")


def compile_videos_from_dict(video_dict, original_video_paths, output_path, per_sequence=False):
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
                    extract_and_save_subclip(video_path, start_frame, end_frame, sequence_index, output_path)


if __name__ == "__main__":
    
    original_video_paths = [
        r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\compiled_tiny_videos_for_testing\compiled\compiled_tiny_original_15a.mkv',
        r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\compiled_tiny_videos_for_testing\compiled\compiled_tiny_original_15b.mkv'
    ]

    video_dict = {
        'sequence_0': {
            'compiled_tiny_original_15b.mkv': [29, 30, 31, 32],
            'compiled_tiny_original_15a.mkv': [8, 9, 10, 11, 12]
        },
        'sequence_1': {
            'compiled_tiny_original_15a.mkv': [10, 11, 12, 13, 14,],
            'compiled_tiny_original_15b.mkv': [28, 29, 30, 31, 32,]
        }
    }
    
    pt.t()
    output_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\compiled_tiny_videos_for_testing'
    compile_videos_from_dict(video_dict, original_video_paths, output_path=output_path,per_sequence=False)
    pt.t()