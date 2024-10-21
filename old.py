import os
import moviepy.editor as mp
import cv2
import numpy as np

def find_videos(folder):
    video_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))
    return video_files

def find_image_in_video(video_path, image_path):
    cap = cv2.VideoCapture(video_path)
    template = cv2.imread(image_path, 0)
    w, h = template.shape[::-1]
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= 0.8)
        if len(loc[0]) > 0:
            return cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Return time in seconds
    return None

def cut_video(video_path, cuts):
    video = mp.VideoFileClip(video_path)
    final_clips = []
    start = 0
    
    for cut in cuts:
        end = cut['start']
        final_clips.append(video.subclip(start, end))
        start = cut['end']
    
    final_clips.append(video.subclip(start, video.duration))
    final_video = mp.concatenate_videoclips(final_clips)
    final_video.write_videofile(f"edited_{os.path.basename(video_path)}")

def main():
    folder = "path_to_your_folder"
    videos = find_videos(folder)
    
    cuts = [
        {'start': find_image_in_video("path_to_video", "path_to_start_image"), 'end': find_image_in_video("path_to_video", "path_to_end_image")}
        # Add more cuts as needed
    ]
    
    for video in videos:
        cut_video(video, cuts)

if __name__ == "__main__":
    main()