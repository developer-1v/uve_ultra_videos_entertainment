import os
import ffmpeg
from rich import print as rprint

def read_metadata(video_path):
    try:
        metadata = ffmpeg.probe(video_path)
        return metadata
    except ffmpeg.Error as e:
        rprint(f"Error reading metadata for {video_path}: {e}")
        return None

def print_metadata(metadata, video_path, editions_only=False):
    if metadata is None:
        rprint(f"No metadata found for {video_path}")
        return

    if editions_only:
        editions = extract_editions(metadata)
        print_chapters(editions)
    else:
        rprint(video_path)
        rprint(metadata)

def print_metadata_for_videos_path(path, editions_only):
    if not os.path.exists(path):
        rprint(f"Provided path does not exist: {path}")
        return

    if os.path.isdir(path):
        videos = os.listdir(path)
        for video in videos:
            video_path = os.path.join(path, video)
            metadata = read_metadata(video_path)
            print_metadata(metadata, video_path, editions_only)
    else:
        metadata = read_metadata(path)
        print_metadata(metadata, path, editions_only)

def extract_editions(metadata):
    tags = metadata['format'].get('tags', {})
    formatted_chapters = []
    for key, value in tags.items():
        if 'EDITION' in key:
            chapters = value.split('[CHAPTER]')
            for chapter in chapters:
                if chapter.strip():
                    chapter_lines = chapter.split('\n')
                    chapter_dict = {}
                    for line in chapter_lines:
                        if '=' in line:
                            k, v = line.split('=', 1)
                            k = k.strip()
                            v = v.strip()
                            chapter_dict[k] = v
                    formatted_chapters.append(format_chapter(chapter_dict))
    return formatted_chapters

def print_chapters(formatted_chapters):
    # Adjust printing to handle dictionary format
    if formatted_chapters:
        for chapter in formatted_chapters:
            rprint('chapter ---------------')
            title = chapter['title']
            timebase = chapter['TIMEBASE']
            other_details = "\n".join(f"  {k}={v}" for k, v in chapter['details'].items())
            rprint(f"title={title}\n{other_details}\n  TIMEBASE={timebase}")
    else:
        rprint('No chapter information found')

def format_chapter(chapter_dict):
    # Ensure START and END are included and correctly named
    return {
        'title': chapter_dict.get('title', 'Untitled'),
        'TIMEBASE': chapter_dict.get('TIMEBASE', ''),
        'start_frame': chapter_dict.get('START', 'Unknown'),  # Adjusted key name to 'START'
        'end_frame': chapter_dict.get('END', 'Unknown'),      # Adjusted key name to 'END'
        'details': {k: v for k, v in chapter_dict.items() if k not in ['title', 'TIMEBASE', 'START', 'END']}
    }

def get_chapters_by_prefix(metadata, prefix):
    chapters = extract_editions(metadata)
    filtered_chapters = []
    for chapter in chapters:
        title = chapter.get('title', '')
        if title.startswith(prefix):
            start_frame = chapter.get('start_frame', 'Unknown')
            end_frame = chapter.get('end_frame', 'Unknown')
            filtered_chapters.append({'title': title, 'START': start_frame, 'END': end_frame})
    return filtered_chapters


if __name__ == "__main__":
    videos_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test'
    editions_only = True
    print_metadata_for_videos_path(videos_path, editions_only)
    
    
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
    metadata = read_metadata(video_path)
    prefix = "__cut_frames_"
    chapters_with_prefix = get_chapters_by_prefix(metadata, prefix)
    for chapter in chapters_with_prefix:
        rprint(chapter)