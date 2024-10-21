import cv2
import re
import os
from print_tricks import pt
from globals import SUPPORTED_VIDEO_TYPES

def is_black_frame(frame, threshold=10):
    return cv2.mean(frame)[0] < threshold

def find_non_black_frame(cap, total_frames, reverse=False):
    frame_index = total_frames - 1 if reverse else 0
    step = -1 if reverse else 1
    black_frame_count = 0
    black_frame_indices = []

    while 0 <= frame_index < total_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame at index {frame_index}")
            frame_index += step
            continue
        if not is_black_frame(frame):
            # print(f"Total black frames: {black_frame_count}")
            # print(f"Black frame indices: {black_frame_indices}")
            return frame, frame_index
        black_frame_count += 1
        black_frame_indices.append(frame_index)
        frame_index += step

    # print(f"No non-black frames found in the {'end' if reverse else 'beginning'} of the video.")
    # print(f"Total black frames: {black_frame_count}")
    # print(f"Black frame indices: {black_frame_indices}")
    return None, frame_index

def process_clips(folder_path):
    print(f"Processing videos in {folder_path}")
    
    def extract_number(file_name):
        match = re.search(r'\d+', file_name)
        return int(match.group()) if match else float('inf')
    
    files = sorted(os.listdir(folder_path), key=extract_number)
    for file_name in files:
        pt()
        pt(file_name)
        if file_name.lower().endswith(tuple(SUPPORTED_VIDEO_TYPES)):
            process_video_file(folder_path, file_name)

def process_video_file(folder_path, file_name):
    video_path = os.path.join(folder_path, file_name)
    start_frame_path = os.path.join(folder_path, f"{file_name}_start_frame.png")
    end_frame_path = os.path.join(folder_path, f"{file_name}_end_frame.png")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(f"Total frames in {video_path}: {total_frames}")
    
    process_start_frame(cap, total_frames, start_frame_path, video_path)
    process_end_frame(cap, total_frames, end_frame_path, video_path)
    
    cap.release()

def process_start_frame(cap, total_frames, start_frame_path, video_path):
    if os.path.exists(start_frame_path):
        print(f"Start frame image already exists for {video_path}. Skipping processing for start frame.")
        return
    
    start_frame, start_frame_index = find_non_black_frame(cap, total_frames, reverse=False)
    if start_frame is None:
        print(f"No non-black frames found in the beginning of {video_path}")
    else:
        # print(f"First non-black frame found at index {start_frame_index}")
        # print(f"Start frame shape: {start_frame.shape}")
        save_frame(start_frame, start_frame_path, start_frame_index, "first")

def process_end_frame(cap, total_frames, end_frame_path, video_path):
    if os.path.exists(end_frame_path):
        print(f"End frame image already exists for {video_path}. Skipping processing for end frame.")
        return
    
    end_frame, end_frame_index = find_non_black_frame(cap, total_frames, reverse=True)
    if end_frame is None:
        print(f"No non-black frames found at the end of {video_path}")
    else:
        # print(f"Last non-black frame found at index {end_frame_index}")
        # print(f"End frame shape: {end_frame.shape}")
        save_frame(end_frame, end_frame_path, end_frame_index, "last")

def save_frame(frame, frame_path, frame_index, frame_position):
    # print(f"Attempting to save {frame_position} non-black frame to {frame_path}")
    if cv2.imwrite(frame_path, frame):
        print(f"Saved {frame_position} non-black frame to {frame_path} at index {frame_index}")
    else:
        print(f"Failed to save {frame_position} non-black frame to {frame_path}")
