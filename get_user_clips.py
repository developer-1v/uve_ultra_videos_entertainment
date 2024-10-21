import os
from globals import POSSIBLE_CLIP_FOLDER_NAMES, SUPPORTED_IMAGE_TYPES, SUPPORTED_VIDEO_TYPES
from print_tricks import pt

def find_paths_of_all_media(clips_path):
    clips = find_paths_of_clips(clips_path)
    images = find_paths_of_images(clips_path)
    return set(clips + images)

def find_paths_of_clips(clips_path):
    clips = []
    # Search for clips/cuts folders 
    for root, dirs, files in os.walk(clips_path):
        for dir_name in dirs:
            # pt(dir_name)
            if any(keyword in dir_name.lower() for keyword in POSSIBLE_CLIP_FOLDER_NAMES):
                folder_path = os.path.join(root, dir_name)
                
                for file_name in os.listdir(folder_path):
                    if file_name.lower().endswith(tuple(SUPPORTED_IMAGE_TYPES + SUPPORTED_VIDEO_TYPES)):
                        print(f"Found media file: {file_name}")
                        clips.append(folder_path)
                        break
    return clips

def find_paths_of_images(clips_path):
    images_to_cut = []
    # Search for clips/cuts folders 
    for root, dirs, files in os.walk(clips_path):
        for dir_name in dirs:
            # pt(dir_name)
            if any(keyword in dir_name.lower() for keyword in POSSIBLE_CLIP_FOLDER_NAMES):
                folder_path = os.path.join(root, dir_name)
                
                for file_name in os.listdir(folder_path):
                    if file_name.lower().endswith(tuple(SUPPORTED_IMAGE_TYPES)):
                        print(f"Found image file to cut: {file_name}")
                        images_to_cut.append(folder_path)
                        break
    return images_to_cut

def get_frame_images_for_cuts(folders_with_clips):
    frame_pairs = []
    pt(folders_with_clips)
    start_images = {}
    end_images = {}
    
    for folder in folders_with_clips:
        for filename in os.listdir(folder):
            if not any(filename.endswith(ext) for ext in SUPPORTED_IMAGE_TYPES):
                continue  # Skip unsupported file types
            
            full_path = os.path.join(folder, filename)
            
            if "start_frame_to_end" in filename:
                base_name = filename.replace("_start_frame_to_end.png", "")
                start_images[base_name] = full_path
                end_images[base_name] = None  # Set end frame to None
            elif "start" in filename:
                base_name = filename.replace("_start_frame.png", "")
                start_images[base_name] = full_path
            elif "end" in filename and "ending" not in filename:
                base_name = filename.replace("_end_frame.png", "")
                end_images[base_name] = full_path
            elif "end" in filename:
                base_name = filename.replace("_end_frame.png", "")
                end_images[base_name] = full_path
    
    for base_name in start_images:
        if base_name in end_images:
            frame_pairs.append((start_images[base_name], end_images[base_name]))
        else:
            raise ValueError(f"Missing end image for start image: {start_images[base_name]}")
    
    for base_name in end_images:
        if base_name not in start_images:
            raise ValueError(f"Missing start image for end image: {end_images[base_name]}")
    
    return frame_pairs

def get_movie_clips(folder):
    # Print the folder path to ensure it's correct
    print(f"Folder path in get_movie_clips: {folder}")
    
    # Check if the folder exists before listing
    if not os.path.exists(folder):
        raise FileNotFoundError(f"The path {folder} does not exist.")
    
    clips = []
    for filename in os.listdir(folder):
        # Ensure the file is a video file (you might want to add more checks here)
        if filename.endswith(('.mp4', '.mkv', '.avi')):
            clips.append(os.path.join(folder, filename))
    
    return clips

if __name__ == "__main__":
    clips_path = os.getcwd()
    paths_of_clips = find_paths_of_clips(clips_path)
    paths_of_images = find_paths_of_images(clips_path)
    frame_paired_images_to_cut = get_frame_images_for_cuts(paths_of_images)
    movie_clips = get_movie_clips(paths_of_clips)
    pt(paths_of_clips, paths_of_images, frame_paired_images_to_cut, movie_clips)