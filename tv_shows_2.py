from print_tricks import pt
from get_user_clips import (
    find_paths_of_all_media, 
    find_paths_of_images, 
    find_paths_of_clips, 
    get_movie_clips, 
    get_frame_paired_images_to_cut
)
from skimage.metrics import structural_similarity as ssim
from tqdm import tqdm
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def simple_hash(image, size=(8, 8)):
    resized = cv2.resize(image, size)
    return resized.mean(axis=0).mean(axis=0)

def find_simplified_frame_in_simplified_video(video_path, image_path, simplified_frames, size=(8, 8)):
    template = cv2.imread(image_path, 0)
    
    if template is None:
        print(f"Error: Could not read image {image_path}")
        return None

    template_hash = simple_hash(template, size)
    
    best_frame = None
    best_score = float('inf')

    for frame_number, frame_hash in simplified_frames.items():
        score = np.linalg.norm(template_hash - frame_hash)
        
        if score < best_score:
            best_score = score
            best_frame = frame_number

    return best_frame

def simplify_video_frames(video_path, size=(8, 8), fps=None):
    with VideoFileClip(video_path) as video:
        simplified_frames = {}
        
        total_frames = int(video.fps * video.duration)
        frame_rate = fps if fps is not None else video.fps
        
        for frame_number, frame in enumerate(tqdm(video.iter_frames(fps=frame_rate, dtype='uint8'), total=total_frames, desc="Creating simplified frames", unit="frame")):
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_hash = simple_hash(gray_frame, size)
            simplified_frames[frame_number] = frame_hash
        
        return simplified_frames

def find_full_image_frame_in_full_video_frame(video_path, image_path, frame_number, size=(32, 32)):
    with VideoFileClip(video_path) as video:
        template = cv2.imread(image_path, 0)
        
        if template is None:
            print(f"Error: Could not read image {image_path}")
            return None

        template_resized = cv2.resize(template, size)
        frame = video.get_frame(frame_number / video.fps)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, size)
        
        score, _ = ssim(resized_frame, template_resized, full=True)
        return frame_number if score > 0.8 else None

def process_videos(series_path, frames_to_cut):
    for root, dirs, files in os.walk(series_path):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv')):
                video_path = os.path.join(root, file)
                pt.t(f'processing video frames for {file}')
                simplified_frames = simplify_video_frames(video_path)
                pt.t(f'processing video frames for {file}')
                
                with VideoFileClip(video_path) as video:
                    cut_ranges = []
                    
                    for start_img, end_img in frames_to_cut:
                        simplified_start_frame = find_simplified_frame_in_simplified_video(video_path, start_img, simplified_frames)
                        if simplified_start_frame is not None:
                            start_frame = find_full_image_frame_in_full_video_frame(video_path, start_img, simplified_start_frame)
                        
                        if end_img is not None:
                            simplified_end_frame = find_simplified_frame_in_simplified_video(video_path, end_img, simplified_frames)
                            if simplified_end_frame is not None:
                                end_frame = find_full_image_frame_in_full_video_frame(video_path, end_img, simplified_end_frame)
                        else:
                            end_frame = None
                        
                        if start_frame is not None:
                            start_time = start_frame / video.fps
                            end_time = (end_frame / video.fps) if end_frame is not None else video.duration
                            cut_ranges.append((start_time, end_time))
                    
                    cut_video(video, cut_ranges, file)

def cut_video(video, cut_ranges, file):
    clips = []
    last_end = 0
    for start_time, end_time in cut_ranges:
        if last_end < start_time:
            clips.append(video.subclip(last_end, start_time))
        last_end = end_time
    if last_end < video.duration:
        clips.append(video.subclip(last_end, video.duration))
    
    if clips:
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile('output_' + file, codec='libx264')




if __name__ == "__main__":
    pt.t('entire app')
    series_path = r'C:\.PythonProjects\eva_editing_videos_automatically\videos_for_testing\mha_flattened'
    pt.t('folders with clips')
    folders_with_clips = find_paths_of_all_media(os.getcwd())
    pt.t('folders with clips')
    pt.t('get image frames for cuts')
    frames_to_cut = get_frame_paired_images_to_cut(folders_with_clips)
    pt.t('get image frames for cuts')
    pt.t('cut videos')
    process_videos(series_path, frames_to_cut)
    pt.t('cut videos')
    pt.t('entire app')