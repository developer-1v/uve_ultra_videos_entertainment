from print_tricks import pt

import os
import cv2
import numpy as np
import hashlib

from get_user_clips import find_paths_of_clips, find_paths_of_images, get_frame_images_for_cuts

from moviepy.editor import VideoFileClip, concatenate_videoclips
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm

def find_frame_in_video(video_path, image_path, resized_frames, size=(32, 32)):
    pt.t('find frame in video')
    template = cv2.imread(image_path, 0)
    
    if template is None:
        print(f"Error: Could not read image {image_path}")
        return None

    template_resized = cv2.resize(template, size)
    
    best_frame = None
    best_score = -1

    for frame_number, resized_frame in resized_frames.items():
        score, _ = ssim(resized_frame, template_resized, full=True)
        # pt(score)
        
        if score > best_score:
            best_score = score
            best_frame = frame_number

        if best_score > 0.8:  # Threshold for matching
            break

    return best_frame if best_score > 0.8 else None

def process_video_frames(video_path, size=(32, 32), fps=None):
    pt.t('process video frames')
    video = VideoFileClip(video_path)
    resized_frames = {}
    
    total_frames = int(video.fps * video.duration)
    # Use the provided fps or default to the video's native frame rate for max speed
    frame_rate = fps if fps is not None else video.fps
    frame_rate = 100000
    
    for frame_number, frame in enumerate(tqdm(video.iter_frames(fps=frame_rate, dtype='uint8'), total=total_frames, desc="Processing frames")):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, size)
        resized_frames[frame_number] = resized_frame
    
    return resized_frames

def cut_videos(series_path, frames_to_cut):
    pt(frames_to_cut)
    # pt.ex()
    pt.t('cut videos')
    for root, dirs, files in os.walk(series_path):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                resized_frames = process_video_frames(video_path)
                video = VideoFileClip(video_path)
                cut_ranges = []
                
                for start_img, end_img in frames_to_cut:
                    start_frame = find_frame_in_video(video_path, start_img, resized_frames)
                    if end_img is not None:
                        end_frame = find_frame_in_video(video_path, end_img, resized_frames)
                    else:
                        end_frame = None
                    
                    if start_frame is not None:
                        start_time = start_frame / video.fps
                        end_time = (end_frame / video.fps) if end_frame is not None else video.duration
                        cut_ranges.append((start_time, end_time))
                
                clips = []
                last_end = 0
                for start_time, end_time in cut_ranges:
                    if last_end < start_time:
                        clips.append(video.subclip(last_end, start_time))
                    last_end = end_time
                if last_end < video.duration:
                    clips.append(video.subclip(last_end, video.duration))
                
                # Ensure all clips are concatenated correctly
                if clips:
                    final_clip = concatenate_videoclips(clips)
                    final_clip.write_videofile('output_' + file, codec='libx264')

if __name__ == "__main__":
    series_path = r'C:\.PythonProjects\eva_editing_videos_automatically\videos_for_testing\mha_flattened'
    folders_with_clips = find_paths_of_clips(os.getcwd())
    folders_with_images = find_paths_of_images(os.getcwd())
    folders_with_media_to_cut = set(folders_with_clips + folders_with_images)
    frames_to_cut = get_frame_images_for_cuts(folders_with_media_to_cut)
    cut_videos(series_path, frames_to_cut)