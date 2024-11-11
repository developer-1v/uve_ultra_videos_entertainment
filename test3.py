import subprocess
import json

def read_mkv_info(file_path):
    try:
        # Run ffprobe command to get all stream information including chapters and metadata
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_chapters',
            '-show_format',
            '-show_streams',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        # Try to find chapters
        chapters = data.get('chapters', [])
        if chapters:
            print("Found chapters:")
            for i, chapter in enumerate(chapters, 1):
                start_time = float(chapter.get('start_time', 0))
                end_time = float(chapter.get('end_time', 0))
                title = chapter.get('tags', {}).get('title', f'Chapter {i}')
                print(f"\nChapter {i}: {title}")
                print(f"Start: {format_time(start_time)}")
                print(f"End: {format_time(end_time)}")
        else:
            print("\nNo traditional chapters found.")
            
        # Try to find metadata that might contain chapter-like information
        print("\nChecking format metadata:")
        format_tags = data.get('format', {}).get('tags', {})
        for key, value in format_tags.items():
            print(f"{key}: {value}")
            
        # Check stream metadata
        print("\nChecking stream metadata:")
        streams = data.get('streams', [])
        for stream in streams:
            if 'tags' in stream:
                print(f"\nStream #{stream.get('index')} ({stream.get('codec_type', 'unknown')}):")
                for key, value in stream['tags'].items():
                    print(f"{key}: {value}")

    except Exception as e:
        print(f"Error: {str(e)}")

def dump_raw_metadata(file_path):
    try:
        # Run ffprobe command to get all information
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_chapters',
            '-show_format',
            '-show_streams',
            file_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        # Pretty print the entire JSON structure
        print(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {str(e)}")



def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

file_path = r'C:\Users\user\Downloads\_Tor\Chronicle.2012.Director.s.Cut.iTA.ENG.AC3.SUB.iTA.ENG.BluRay.1080p.x264.jeddak-MIRCrew.mkv'
read_mkv_info(file_path)

dump_raw_metadata(file_path)
