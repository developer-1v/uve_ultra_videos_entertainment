import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

from print_tricks import pt
from rich import print as rprint

def extract_and_save_subclip(video_path, start_time, end_time, output_path):
    """Extracts and saves a subclip from a given video."""
    try:
        with VideoFileClip(video_path) as clip:
            subclip = clip.subclip(start_time, end_time)
            subclip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            print(f"Subclip saved to {output_path}")
    except Exception as e:
        print(f"Error processing {video_path}: {e}")

def extract_subclips(video_dict, original_video_paths, output_path):
    """Extracts specified subclips from videos."""
    for sequence_index, (sequence_name, videos) in enumerate(video_dict.items()):
        for video_name, (start_frame, end_frame) in videos.items():
            if start_frame is None or end_frame is None:
                print(f"Warning: No valid frame range found for {video_name} in {sequence_name}. Skipping.")
                continue

            for video_path in original_video_paths:
                if os.path.basename(video_path) == video_name:
                    with VideoFileClip(video_path) as clip:
                        start_time = start_frame / clip.fps
                        end_time = end_frame / clip.fps
                        subclip_output_path = os.path.join(output_path, f"clip_{sequence_index}({start_frame}_{end_frame})_{video_name}")
                        extract_and_save_subclip(video_path, start_time, end_time, subclip_output_path)

def compile_originals_without_subclips(video_dict, original_video_paths, output_path):
    """Compiles the original videos excluding the subclip frames."""
    for video_path in original_video_paths:
        video_name = os.path.basename(video_path)
        clips_to_concatenate = []
        with VideoFileClip(video_path) as clip:
            last_end = 0
            for sequence in video_dict.values():
                if video_name in sequence:
                    frames = sequence[video_name]
                    start_time = frames[0] / clip.fps
                    end_time = frames[-1] / clip.fps
                    if start_time > last_end:
                        clips_to_concatenate.append(clip.subclip(last_end, start_time))
                    last_end = end_time
            if last_end < clip.duration:
                clips_to_concatenate.append(clip.subclip(last_end, clip.duration))
            if clips_to_concatenate:
                final_clip = concatenate_videoclips(clips_to_concatenate)
                final_output_path = os.path.join(output_path, f"original_no_subclips_{video_name}")
                final_clip.write_videofile(final_output_path, codec='libx264', audio_codec='aac')
                print(f"Original video without subclips compiled to {final_output_path}")

if __name__ == "__main__":
    original_video_paths = [
        r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\compiled_tiny_videos_for_testing\compiled\compiled_tiny_original_15a.mkv',
        r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\compiled_tiny_videos_for_testing\compiled\compiled_tiny_original_15b.mkv'
    ]

    video_dict = {
        'sequence_0': {
            'compiled_tiny_original_15b.mkv': [29, 32],
            'compiled_tiny_original_15a.mkv': [8, 12]
        },
        'sequence_1': {
            'compiled_tiny_original_15a.mkv': [10, 14],
            'compiled_tiny_original_15b.mkv': [28, 32]
        }
    }

    pt.t()
    output_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\compiled_tiny_videos_for_testing'
    
    # Extract subclips
    extract_subclips(video_dict, original_video_paths, output_path)
    
    # Compile original videos without subclips
    compile_originals_without_subclips(video_dict, original_video_paths, output_path)
    
    pt.t()