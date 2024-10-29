import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QHBoxLayout, QSizePolicy
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt, QTimer
import cv2

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.playPauseButton = QPushButton("Play")
        self.stopButton = QPushButton("Stop")
        self.stepForwardButton = QPushButton("Step Forward")
        self.stepBackwardButton = QPushButton("Step Backward")
        self.nextClipButton = QPushButton("Next Clip")
        self.prevClipButton = QPushButton("Prev Clip")
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
        buttonLayout.addWidget(self.stepBackwardButton)
        buttonLayout.addWidget(self.stepForwardButton)
        buttonLayout.addWidget(self.prevClipButton)
        buttonLayout.addWidget(self.nextClipButton)
        # Add timestamp and frame number to the button layout
        buttonLayout.addWidget(self.timestampLabel)
        buttonLayout.addWidget(self.frameNumberLabel)
        layout.addLayout(buttonLayout)  # Add the button layout to the
        self.setLayout(layout)


class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.setWindowTitle("PySide6 Video Player")

        # Initialize first_step attribute
        self.first_step = True

        # Use OpenCV to get the frame rate
        cap = cv2.VideoCapture(self.video_path)
        self.frame_rate = cap.get(cv2.CAP_PROP_FPS)
        cap.release()  # Release the video capture object

        self.mediaPlayer = QMediaPlayer(None)
        videoWidget = QVideoWidget()
        
        videoUrl = QUrl.fromLocalFile(self.video_path)
        self.mediaPlayer.setSource(videoUrl)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.durationChanged.connect(self.update_slider_max)
        self.mediaPlayer.positionChanged.connect(self.update_slider_position)

        self.controlPanel = ControlPanel(self)
        self.controlPanel.playPauseButton.clicked.connect(self.toggle_play_pause)
        self.controlPanel.stopButton.clicked.connect(self.stop_video)
        
        # Set up auto-repeat for step buttons
        self.controlPanel.stepForwardButton.setAutoRepeat(True)
        self.controlPanel.stepForwardButton.setAutoRepeatInterval(100)  # Interval in ms
        self.controlPanel.stepForwardButton.setAutoRepeatDelay(500)  # Initial delay in ms

        self.controlPanel.stepBackwardButton.setAutoRepeat(True)
        self.controlPanel.stepBackwardButton.setAutoRepeatInterval(100)
        self.controlPanel.stepBackwardButton.setAutoRepeatDelay(500)

        # Connect the buttons to the stepping functions
        self.controlPanel.stepForwardButton.clicked.connect(self.step_forward)
        self.controlPanel.stepBackwardButton.clicked.connect(self.step_backward)

        self.controlPanel.prevClipButton.clicked.connect(self.prev_clip)
        self.controlPanel.nextClipButton.clicked.connect(self.next_clip)
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

    def ensure_media_ready(self):
        # Check if the media player is ready, if not, perform a play-pause to ready it
        if self.mediaPlayer.mediaStatus() in [QMediaPlayer.NoMedia, QMediaPlayer.LoadedMedia]:
            self.mediaPlayer.play()
            self.mediaPlayer.pause()

    def step_forward(self):
        was_playing = self.mediaPlayer.playbackState() == QMediaPlayer.PlayingState
        self.ensure_media_ready()
        frame_duration = int(round(1000 / self.frame_rate))
        current_position = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(current_position + frame_duration)
        if was_playing:
            if self.first_step:
                self.mediaPlayer.pause()
                self.first_step = False
            else:
                self.mediaPlayer.play()

    def step_backward(self):
        was_playing = self.mediaPlayer.playbackState() == QMediaPlayer.PlayingState
        self.ensure_media_ready()
        frame_duration = int(round(1000 / self.frame_rate))
        current_position = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(current_position - frame_duration)
        if was_playing:
            if self.first_step:
                self.mediaPlayer.pause()
                self.first_step = False
            else:
                self.mediaPlayer.play()




    def next_clip(self):
        # Logic to jump to the next video clip
        pass

    def prev_clip(self):
        # Logic to jump to the previous video clip
        pass

    def update_slider_max(self, duration):
        self.controlPanel.timelineSlider.setMaximum(duration)

    def update_slider_position(self, position):
        self.controlPanel.timelineSlider.setValue(position)
    # Update the seek_video method to sync the slider with the video timeline

    def seek_video(self, position):
        self.mediaPlayer.setPosition(position)
        # Sync the slider position with the video's current position
        self.controlPanel.timelineSlider.setValue(position)

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\_s01e01_40.mp4'
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())