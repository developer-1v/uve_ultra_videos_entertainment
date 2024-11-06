# video_player.py
import sys
from PySide6.QtWidgets import QApplication
from vid_player_window import VideoPlayer

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())