import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QSizePolicy
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt


class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.playPauseButton = QPushButton("Play")
        self.stopButton = QPushButton("Stop")
        self.stepForwardButton = QPushButton("Step Forward")
        self.stepBackwardButton = QPushButton("Step Backward")
        self.timelineSlider = QSlider(Qt.Horizontal)
        self.timestampLabel = QLabel("Timestamp: 00:00")
        self.frameNumberLabel = QLabel("Frame: 0/0")

        ## slider
        layout = QVBoxLayout()  # Changed from QHBoxLayout to QVBoxLayout
        layout.addWidget(self.timelineSlider)  # This now comes first
        
        ## controls
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playPauseButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.stepForwardButton)
        buttonLayout.addWidget(self.stepBackwardButton)
        buttonLayout.addWidget(self.stepBackwardButton)
        # Add timestamp and frame number to the button layout
        buttonLayout.addWidget(self.timestampLabel)
        buttonLayout.addWidget(self.frameNumberLabel)
        layout.addLayout(buttonLayout)  # Add the button layout to the
        self.setLayout(layout)

# Modify the VideoPlayer class to use ControlPanel
class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.setWindowTitle("PySide6 Video Player")

        self.mediaPlayer = QMediaPlayer(None)
        videoWidget = QVideoWidget()
        
        videoUrl = QUrl.fromLocalFile(self.video_path)
        self.mediaPlayer.setSource(videoUrl)
        self.mediaPlayer.setVideoOutput(videoWidget)

        self.controlPanel = ControlPanel(self)
        self.controlPanel.playPauseButton.clicked.connect(self.toggle_play_pause)
        self.controlPanel.stopButton.clicked.connect(self.stop_video)
        self.controlPanel.stepForwardButton.clicked.connect(self.step_forward)
        self.controlPanel.stepBackwardButton.clicked.connect(self.step_backward)
        self.controlPanel.timelineSlider.sliderMoved.connect(self.seek_video)
        self.controlPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        videoWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(self.controlPanel)
        widget.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)

    def toggle_play_pause(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlayingState:
            self.controlPanel.playPauseButton.setText("Play")
            self.mediaPlayer.pause()
        else:
            self.controlPanel.playPauseButton.setText("Pause")
            self.mediaPlayer.play()

    def stop_video(self):
        self.mediaPlayer.stop()

    def step_forward(self):
        # This method will need additional implementation to move one frame forward
        pass

    def step_backward(self):
        # This method will need additional implementation to move one frame backward
        pass

    def seek_video(self, position):
        self.mediaPlayer.setPosition(position)
        # Update timestamp and frame number based on position

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\_s01e01_40.mp4'
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())