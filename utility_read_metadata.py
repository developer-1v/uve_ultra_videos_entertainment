import os, sys
import ffmpeg
from print_tricks import pt
from rich import print as rprint


def read_metadata(video_path):
    metadata = ffmpeg.probe(video_path)
    return metadata


def print_metadata(video_path, editions_only=False):
    metadata = read_metadata(video_path)
    if editions_only:
        # Extract and print only edition information
        editions = extract_editions(metadata)
        rprint(video_path)
        rprint(editions)
    else:
        # Print all metadata without restrictions
        rprint(video_path)
        rprint(metadata)


def extract_editions(metadata):
    tags = metadata['format'].get('tags', {})
    formatted_editions = []
    for key, value in tags.items():
        if 'EDITION' in key:
            # Split the chapters by '[CHAPTER]' to ensure all chapters are captured
            chapters = value.split('[CHAPTER]')
            for chapter in chapters:
                if chapter.strip():  # Ensure the chapter contains data
                    # Split each chapter by '\n' and format it
                    chapter_lines = chapter.split('\n')
                    chapter_dict = {}
                    for line in chapter_lines:
                        if '=' in line:  # Check if the line contains '='
                            k, v = line.split('=', 1)
                            chapter_dict[k.strip()] = v.strip()
                    
                    # Rearrange the order: title first, timebase last
                    if 'title' in chapter_dict:
                        formatted_chapter = f"title={chapter_dict['title']}\n"
                        formatted_chapter += "\n".join(f"  {k}={v}" for k, v in chapter_dict.items() if k != 'title' and k != 'TIMEBASE')
                        formatted_chapter += f"\n  TIMEBASE={chapter_dict.get('TIMEBASE', '')}"
                        formatted_editions.append(formatted_chapter)
    
    # Print each formatted edition separately
    if formatted_editions:
        for edition in formatted_editions:
            rprint(edition)
    else:
        rprint('No edition information found')

def print_metadata_for_videos_path(path, editions_only):
    if os.path.isdir(path):
        videos = os.listdir(path)
        for video in videos:
            video_path = os.path.join(path, video)
            print_metadata(video_path, editions_only)
            # pt.ex()
    elif os.path.isfile(path):
        print_metadata(path, editions_only)
    else:
        print(f"Provided path is neither a file nor a directory: {path}")

if __name__ == "__main__":
    videos_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test'
    editions_only = True
    print_metadata_for_videos_path(videos_path, editions_only)


'''




'''



