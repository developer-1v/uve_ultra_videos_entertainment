import os, sys
import ffmpeg
from print_tricks import pt
from rich import print as rprint


def read_metadata(video_path):
    metadata = ffmpeg.probe(video_path)
    return metadata


def print_metadata(video_path, chapters=False, editions=False, all_metadata=False):
    metadata = read_metadata(video_path)
    if chapters:
        # Extract and print only chapter information
        chapters = extract_chapters(metadata)
        rprint(video_path)
        rprint(chapters)
    if editions:
        # Extract and print only edition information
        editions = extract_editions(metadata)
        rprint(video_path)
        rprint(editions)
    if all_metadata:
        # Print all metadata without restrictions
        rprint(video_path)
        rprint(metadata)




def extract_chapters(metadata):
    tags = metadata['format'].get('tags', {})
    chapter_data = next((value for key, value in tags.items() if 'CHAPTER' in key), 'No chapter information found')
    return chapter_data

def extract_editions(metadata):
    tags = metadata['format'].get('tags', {})
    edition_data = next((value for key, value in tags.items() if 'EDITION' in key), 'No edition information found')
    return edition_data

def print_metadata_for_videos_path(path, chapters, editions, all_metadata):
    if os.path.isdir(path):
        videos = os.listdir(path)
        for video in videos:
            video_path = os.path.join(path, video)
            print_metadata(video_path, chapters, editions, all_metadata)
            pt.ex()
    elif os.path.isfile(path):
        print_metadata(path, chapters, editions, all_metadata)
    else:
        print(f"Provided path is neither a file nor a directory: {path}")

if __name__ == "__main__":
    videos_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test'
    chapters = True
    editions = True
    all_metadata = False
    print_metadata_for_videos_path(videos_path, chapters, editions, all_metadata)



'''



'''