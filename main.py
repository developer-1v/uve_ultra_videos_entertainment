from print_tricks import pt

import os
import sys

from get_user_clips import find_paths_of_clips, find_paths_of_images, get_frame_images_for_cuts
from gui import GUI
from process_clips import process_clips
from tv_shows import cut_videos

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--gui':
            print("Started with GUI")
            # Add your GUI initialization code here
            series_path = GUI.get_series_path_from_gui()
            clips_path = GUI.get_clips_path_from_gui()
        else:
            print("Started from another script")
            series_path = sys.argv[1]
            clips_path = sys.argv[2]
    else:
        print("Started from terminal or double-click")
        cwd = os.getcwd()
        series_path = os.path.join(cwd, 'mha_flattened')
        clips_path = cwd
    
    folders_with_clips = find_paths_of_clips(clips_path)
    folders_with_images = find_paths_of_images(clips_path)
    folders_with_media_to_cut = set(folders_with_clips + folders_with_images)
    
    # for folder in folders_with_clips:
    #     process_clips(folder)
    
    frames_to_cut = get_frame_images_for_cuts(folders_with_media_to_cut)
    
    cut_videos(series_path, frames_to_cut)
    pt(frames_to_cut)

if __name__ == "__main__":
    main()