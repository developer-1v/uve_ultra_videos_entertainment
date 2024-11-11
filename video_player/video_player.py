from print_tricks import pt
pt.easy_import('b_main.py')
import sys
from PySide6.QtWidgets import QApplication
from video_player.vid_player_window import VideoPlayer

def run_vid_player(video_path, prefix="__cut_frames_"):
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path, prefix)
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
    run_vid_player(video_path, prefix="__cut_frames_")