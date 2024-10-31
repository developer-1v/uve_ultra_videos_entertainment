import os
import ffmpeg
from print_tricks import pt
from rich import print as rprint
def read_metadata(video_path):
    metadata = ffmpeg.probe(video_path)
    return metadata


if __name__ == "__main__":
    videos_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test'
    videos = os.listdir(videos_path)
    for video in videos:
        video_path = os.path.join(videos_path, video)
        metadata = read_metadata(video_path)
        rprint(video)
        rprint(metadata)
