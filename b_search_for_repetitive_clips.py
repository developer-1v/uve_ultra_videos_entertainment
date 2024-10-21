import cv2
import os
import psutil
import shelve
from collections import defaultdict
from print_tricks import pt
from globals import SUPPORTED_VIDEO_TYPES
from tqdm import tqdm

def extract_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        # Check memory usage and yield if necessary
        if psutil.virtual_memory().percent > 80:  # Adjust threshold as needed
            yield frames
            frames = []
    if frames:
        yield frames
    cap.release()


def find_repetitive_sequences(videos_folder, sequence_length=5, save_interval=1000):
    matching_items_required = 2



if __name__ == "__main__":
    video_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_small_videos_for_testing', 'compiled')
    for video_file in os.listdir(video_path):
        video = cv2.VideoCapture(os.path.join(video_path, video_file))
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        pt(video_file, video, total_frames)
    pt(video_path)
    
    # main(video_path)