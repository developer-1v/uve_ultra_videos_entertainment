import os
from print_tricks import pt
from globals import SUPPORTED_VIDEO_TYPES

def find_videos_in_folder(folder_path):
    video_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in SUPPORTED_VIDEO_TYPES):
                video_files.append(os.path.join(root, file))
    return video_files

def organize_videos_by_season(folder_path):
    seasons = {}
    for root, dirs, files in os.walk(folder_path):
        # Check if the current directory has video files
        video_files = find_videos_in_folder(root)
        if video_files:
            # Use the directory name as the season name
            season_name = os.path.basename(root)
            seasons[season_name] = sorted(video_files)
    return seasons

def organize_series(folder_path):
    series_name = os.path.basename(folder_path)
    seasons = organize_videos_by_season(folder_path)
    return {series_name: seasons}

def find_seasons(folder_path):
    series = organize_series(folder_path)
    # pt(series)

    return series

def print_series(series):
    for series_name, seasons in series.items():
        print(f"Series: {series_name}")
        for season, videos in sorted(seasons.items()):
            print(f"  Season: {season}")
            for video in videos:
                print(f"    Video: {video}")
                
if __name__ == "__main__":
    series_path = os.path.join(os.getcwd(), 'videos_for_testing', 'compiled_tiny_videos_for_testing', 'compiled')
    pt(series_path)
    seasons = find_seasons(series_path)
    print_series(seasons)