''' failed due to PyQt6 not working'''

from pyvidplayer2 import Video

def main(video_path):
    video = Video(video_path)
    video.show_controls()  # Show the video with GUI controls
    video.play()
    video.wait_for_finish()

if __name__ == "__main__":
    main(r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\_s01e01_40.mp4')