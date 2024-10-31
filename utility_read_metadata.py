import os, sys
import ffmpeg
from print_tricks import pt
from rich import print as rprint


def read_metadata(video_path):
    metadata = ffmpeg.probe(video_path)
    return metadata


def print_metadata(video_path, chapters_only=False):
    metadata = read_metadata(video_path)
    if chapters_only:
        # Attempt to extract chapter information from the 'tags' dictionary
        tags = metadata['format'].get('tags', {})
        chapter_data = next((value for key, value in tags.items() if 'CHAPTER' in key), 'No chapter information found')
        
        # Print the video path and the extracted chapter information
        rprint(video_path)
        rprint(chapter_data)
    else:
        # Print all metadata
        rprint(video_path)
        rprint(metadata)

def print_metadata_for_videos_path(path, chapters_only):
    if os.path.isdir(path):
        videos = os.listdir(path)
        for video in videos:
            video_path = os.path.join(path, video)
            print_metadata(video_path, chapters_only)
    elif os.path.isfile(path):
        print_metadata(path, chapters_only)
    else:
        print(f"Provided path is neither a file nor a directory: {path}")

if __name__ == "__main__":
    videos_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test'
    chapters_only = True
    print_metadata_for_videos_path(videos_path, chapters_only)
    
