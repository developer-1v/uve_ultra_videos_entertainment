

import cv2
import os
from print_tricks import pt
from get_user_clips import find_paths_of_clips, get_movie_clips
from tqdm import tqdm
import random

def count_frames(video_path):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.release()
    return total_frames

def print_video_details(video_path, video_type, original_width=None, original_height=None):
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Failed to open {video_type} {video_path}")
        return
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"{video_type} '{video_path}': {width}x{height}, {fps} FPS, {total_frames} frames")
    
    # Print the difference in resolution if original dimensions are provided
    if original_width is not None and original_height is not None:
        if (width, height) != (original_width, original_height):
            print(f"Resolution difference: Original {original_width}x{original_height}, Clip {width}x{height}")
    
    video.release()

def determine_clip_order(clips, order="normal"):
    if order == "reverse":
        return list(reversed(clips))
    elif order == "random":
        return random.sample(clips, len(clips))
    else:
        return clips

def assign_order_and_compile_video(original_video_path, clips, interval_frames, output_video_name, order="normal"):
    ordered_clips = determine_clip_order(clips, order)
    compile_video_with_clips(original_video_path, ordered_clips, interval_frames, output_video_name)

def compile_video_with_clips(original_video_path, clips, interval_frames, output_video_name):
    # Print details of the original video
    original_video = cv2.VideoCapture(original_video_path)
    width = int(original_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(original_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = original_video.get(cv2.CAP_PROP_FPS)
    print_video_details(original_video_path, "Original Video")

    # Prepare a VideoWriter to save the new video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_name, fourcc, fps, (width, height))

    current_frame = 0
    clip_index = 0

    total_frames = int(original_video.get(cv2.CAP_PROP_FRAME_COUNT))
    with tqdm(total=total_frames, desc="Processing Video") as pbar:
        while True:
            # Read and write frames from the original video until the next interval
            for _ in range(interval_frames):
                ret, frame = original_video.read()
                if not ret:
                    break
                out.write(frame)
                current_frame += 1
                pbar.update(1)

            # Insert the entire clip if available
            if clip_index < len(clips):
                clip_path = clips[clip_index]
                clip_index += 1

                # Open the video clip
                clip_video = cv2.VideoCapture(clip_path)
                if not clip_video.isOpened():
                    print(f"Failed to open clip {clip_path}")
                    continue

                clip_width = int(clip_video.get(cv2.CAP_PROP_FRAME_WIDTH))
                clip_height = int(clip_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
                clip_fps = clip_video.get(cv2.CAP_PROP_FPS)

                # Check compatibility for a few frames
                needs_resizing = (clip_width, clip_height) != (width, height)
                fps_mismatch = clip_fps != fps

                if needs_resizing or fps_mismatch:
                    print(f"Clip {clip_path} is not compatible:")
                    if needs_resizing:
                        print(f" - Resolution mismatch: Clip {clip_width}x{clip_height}, Original {width}x{height}")
                    if fps_mismatch:
                        print(f" - FPS mismatch: Clip {clip_fps}, Original {fps}")
                    clip_video.release()
                    continue

                # Assume compatibility and insert the entire clip
                while True:
                    ret_clip, clip_frame = clip_video.read()
                    if not ret_clip:
                        break
                    out.write(clip_frame)
                    pbar.update(1)

                # Print a message after the entire clip is inserted
                print(f"Inserted clip {clip_path} at frame {current_frame}")

                clip_video.release()

            # Check if the end of the original video is reached
            if not ret:
                break

    # Ensure resources are released
    original_video.release()
    out.release()

if __name__ == "__main__":
    cwd = os.getcwd()
    
    # Define the paths
    input_videos_folder = os.path.join(cwd, 'videos_for_testing', 'compiled_tiny_videos_for_testing')
    paths_of_clips = os.path.join(input_videos_folder, 'small_clips')
    
    # Create the compiled subfolder if it doesn't exist
    compiled_folder = os.path.join(input_videos_folder, 'compiled')
    if not os.path.exists(compiled_folder):
        os.makedirs(compiled_folder)
    
    # Check if the path exists
    if not os.path.exists(paths_of_clips):
        print(f"Error: The path {paths_of_clips} does not exist.")
    else:
        clips = get_movie_clips(paths_of_clips)
    
    num_clips = len(clips)
    
    # Process each video in the input folder
    for video_file in os.listdir(input_videos_folder):
        if video_file.endswith('.mkv'):  # Adjust the extension as needed
            original_video_path = os.path.join(input_videos_folder, video_file)
            output_video_name = os.path.join(compiled_folder, f'compiled_{video_file}')
            
            total_frames = count_frames(original_video_path)
            pt(total_frames)
            
            # Calculate the interval
            interval_frames_between_clips = total_frames // num_clips
            
            pt(clips, num_clips, interval_frames_between_clips)
            
            # Compile the video with clips in random order
            order = "random"
            assign_order_and_compile_video(original_video_path, clips, interval_frames_between_clips, output_video_name, order)
            print(f"Processed {video_file} into {output_video_name}")

    print("All videos processed.")