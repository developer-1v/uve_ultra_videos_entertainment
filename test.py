import os
from print_tricks import pt
video_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_tiny_videos_for_testing', 'compiled', 'tiny_compiled_15a_normal.mkv')


''' Movie py minimal clip example '''

from moviepy.editor import VideoFileClip

# Define the paths to the video files
video_paths = [
    'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15a_normal.mkv',
    'C:\\.PythonProjects\\eva_editing_videos_automatically\\videos_for_testing\\compiled_tiny_videos_for_testing\\compiled\\tiny_compiled_15b_reverse.mkv'
]

# Define the frame range
start_frame = 5
end_frame = 15

# Process each video
for video_path in video_paths:
    with VideoFileClip(video_path) as clip:
        # Calculate start and end times in seconds
        start_time = start_frame / clip.fps
        end_time = end_frame / clip.fps
        
        # Extract the subclip
        subclip = clip.subclip(start_time, end_time)
        
        # Define the output path using a valid file name
        video_name = os.path.basename(video_path)  # Get the video file name
        output_path = f"subclip_{start_frame}_{end_frame}_{video_name}"
        
        # Write the subclip to a file
        subclip.write_videofile(output_path, codec='libx264', audio_codec='aac')

pt.ex()

''' 125-140 it/s'''
import av
import hashlib
import numpy as np
import time
from tqdm import tqdm

def hash_frame(frame):
    # Convert frame to a string and hash it
    return hashlib.md5(frame.to_ndarray().tobytes()).hexdigest()

frame_hash_map = {}

# Start timing
start_time = time.time()

# Open the video file
container = av.open(video_path)

# Get the total number of frames
total_frames = container.streams.video[0].frames

# Process frames with a progress bar
for frame_number, frame in tqdm(enumerate(container.decode(video=0)), total=total_frames, desc="Processing Video"):
    frame_hash = hash_frame(frame)
    if frame_hash in frame_hash_map:
        frame_hash_map[frame_hash].append(frame_number)
    else:
        frame_hash_map[frame_hash] = [frame_number]


# End timing
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Time taken to process the video: {elapsed_time:.2f} seconds")

# frame_hash_map now contains unique frame hashes as keys and lists of frame numbers as values



''' open 3d - 125-140 it/s'''
import av
import hashlib
import numpy as np
import open3d as o3d
import time
from tqdm import tqdm

def hash_frame(frame):
    return hashlib.md5(frame.to_ndarray().tobytes()).hexdigest()

container = av.open(video_path)
frame_hash_map = {}  # Use a regular Python dictionary

# Start timing
start_time = time.time()

# Get the total number of frames
total_frames = container.streams.video[0].frames

# Process frames with a progress bar
for frame_number, frame in tqdm(enumerate(container.decode(video=0)), total=total_frames, desc="Processing Video"):
    frame_hash = hash_frame(frame)
    if frame_hash in frame_hash_map:
        frame_hash_map[frame_hash].append(frame_number)
    else:
        frame_hash_map[frame_hash] = [frame_number]

# End timing
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Time taken to process the video: {elapsed_time:.2f} seconds")


# frame_hash_map now contains unique frame hashes as keys and lists of frame numbers as values
# 


'''Simple cv2 read video, frame by frame. 40 minute, 31,000 frames video, processed in 2:26. 200+ it/s '''

import cv2
import time
import os
from tqdm import tqdm  # Import tqdm

# Path to the video file
video_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_large_videos_for_testing', 'compiled_video_1.avi')

# Start timing
start_time = time.time()

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get the total number of frames
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Read frames from the video with a progress bar
with tqdm(total=total_frames, desc="Processing Video") as pbar:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Process the frame (if needed)
        # For example, display the frame
        # cv2.imshow('Frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        pbar.update(1)  # Update the progress bar

# Release the video capture object
cap.release()

# End timing
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Time taken to read the video: {elapsed_time:.2f} seconds")




'''Simple pyav read video, frame by frame. 2:18, 470 it/s'''

import av
import time
import os
from tqdm import tqdm  # Import tqdm

# Path to the video file
video_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_large_videos_for_testing', 'compiled_video_1.avi')

# Start timing
start_time = time.time()

# Open the video file
container = av.open(video_path)

# Get the total number of frames
total_frames = container.streams.video[0].frames

# Read frames from the video with a progress bar
with tqdm(total=total_frames, desc="Processing Video") as pbar:
    for frame in container.decode(video=0):
        # Process the frame (if needed)
        # For example, convert frame to an image array
        # image = frame.to_ndarray(format='bgr24')
        pbar.update(1)  # Update the progress bar

# End timing
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Time taken to read the video: {elapsed_time:.2f} seconds")
