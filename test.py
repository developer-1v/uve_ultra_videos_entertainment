import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor

class ChapterOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_frame = 25
        self.end_frame = 75
        self.current_frame = 0
        self.frame_rate = 30
        # Add this line to ensure the overlay can receive paint events
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def set_transparent_overlay(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

    def paintEvent(self, event):
        if self.start_frame <= self.current_frame <= self.end_frame:
            painter = QPainter(self)
            painter.setBrush(QColor(255, 0, 0, 222))  # Semi-transparent red
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())
            painter.fillRect(self.rect(), QColor(255, 0, 0, 128))

    def update_frame(self, position):
        self.current_frame = int(position / (1000 / self.frame_rate))
        self.update()  # Trigger a repaint

class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player with Overlay")
        self.videoWidget = QVideoWidget(self)
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        # Updated to use QUrl for local file paths
        from PySide6.QtCore import QUrl
        self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))

        self.chapterOverlay = ChapterOverlay(self.videoWidget)
        self.chapterOverlay.setGeometry(self.videoWidget.geometry())
        self.chapterOverlay.show()

        # Move overlay creation after setting up the central widget
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.chapterOverlay = ChapterOverlay(self)  # Change parent to self
        self.chapterOverlay.setGeometry(self.videoWidget.geometry())
        self.chapterOverlay.raise_()  # Ensure overlay is on top
        self.chapterOverlay.show()

        self.mediaPlayer.positionChanged.connect(self.chapterOverlay.update_frame)
        self.mediaPlayer.setLoops(QMediaPlayer.Infinite)  # Set the media player to loop infinitely
        self.mediaPlayer.play()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.chapterOverlay.setGeometry(self.videoWidget.geometry())

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)  # Change to your video path
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())