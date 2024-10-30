import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
                                QLabel, QSlider, QHBoxLayout, QSizePolicy, QGroupBox)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
import cv2

class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.playPauseButton = QPushButton("Play")
        self.stopButton = QPushButton("Stop")
        self.stepForwardButton = QPushButton(">")
        self.stepBackwardButton = QPushButton("<")
        self.nextClipButton = QPushButton("Next Clip")
        self.prevClipButton = QPushButton("Prev Clip")
        self.timelineSlider = QSlider(Qt.Horizontal)

        self.set_tooltips()
        
        # Timestamp GroupBox
        self.timestampGroupBox = QGroupBox("Timestamp")
        self.timestampValueLabel = QLabel("00:00")
        timestampLayout = QVBoxLayout()
        timestampLayout.addWidget(self.timestampValueLabel)
        timestampLayout.setSpacing(5)  # Reduce spacing between widgets in the layout
        timestampLayout.setContentsMargins(10, 1, 10, 1)  # Adjust left, top, right, bottom margins
        self.timestampGroupBox.setLayout(timestampLayout)

        # Frame Number GroupBox
        self.frameNumberGroupBox = QGroupBox("Frame")
        self.frameNumberValueLabel = QLabel("0/0")
        frameNumberLayout = QVBoxLayout()
        frameNumberLayout.addWidget(self.frameNumberValueLabel)
        frameNumberLayout.setSpacing(5)  # Reduce spacing between widgets in the layout
        frameNumberLayout.setContentsMargins(10, 1, 10, 5)  # Adjust left, top, right, bottom margins
        self.frameNumberGroupBox.setLayout(frameNumberLayout)


        # Controls layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playPauseButton)
        buttonLayout.addWidget(self.stopButton)
        buttonLayout.addWidget(self.stepBackwardButton)
        buttonLayout.addWidget(self.stepForwardButton)
        buttonLayout.addWidget(self.prevClipButton)
        buttonLayout.addWidget(self.nextClipButton)
        buttonLayout.addWidget(self.timestampGroupBox)
        buttonLayout.addWidget(self.frameNumberGroupBox)

        layout = QVBoxLayout()
        layout.addWidget(self.timelineSlider)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

    def set_tooltips(self):
        self.setup_tooltip(self.playPauseButton, "(__ Spacebar)")
        self.setup_tooltip(self.stopButton, "(s)")
        self.setup_tooltip(self.stepForwardButton, "(f)")
        self.setup_tooltip(self.stepBackwardButton, "(d)")
        self.setup_tooltip(self.nextClipButton, "(R arrow)")
        self.setup_tooltip(self.prevClipButton, "(L arrow)")
        self.setup_tooltip(self.timelineSlider, "")

    def setup_tooltip(self, widget, text):
        widget.setToolTip(text)
        widget.setToolTipDuration(0)  # Tooltip shows immediately


class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.setWindowTitle("PySide6 Video Player")
        self.initialize_ui()
        self.setup_media_player()
        self.configure_buttons()

    def initialize_ui(self):
        # Initialize UI components
        self.videoWidget = QVideoWidget()
        self.controlPanel = ControlPanel(self)
        self.controlPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.videoWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.controlPanel)
        widget.setLayout(layout)

    def setup_media_player(self):
        self.mediaPlayer = QMediaPlayer(None)
        videoUrl = QUrl.fromLocalFile(self.video_path)
        self.mediaPlayer.setSource(videoUrl)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.durationChanged.connect(self.update_slider_max)
        self.mediaPlayer.positionChanged.connect(self.update_slider_position)
        self.mediaPlayer.positionChanged.connect(self.update_labels)

        cap = cv2.VideoCapture(self.video_path)
        self.frame_rate = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

    def configure_buttons(self):
        # Configure buttons and connect signals
        self.controlPanel.playPauseButton.clicked.connect(self.toggle_play_pause)
        self.controlPanel.stopButton.clicked.connect(self.stop_video)
        self.setup_auto_repeat(self.controlPanel.stepForwardButton, self.step_forward)
        self.setup_auto_repeat(self.controlPanel.stepBackwardButton, self.step_backward)
        self.controlPanel.prevClipButton.clicked.connect(self.prev_clip)
        self.controlPanel.nextClipButton.clicked.connect(self.next_clip)
        self.controlPanel.timelineSlider.sliderMoved.connect(self.seek_video)

    def setup_auto_repeat(self, button, slot_function):
        # Set up auto-repeat for step buttons
        button.setAutoRepeat(True)
        button.setAutoRepeatInterval(100)  # Interval in ms
        button.setAutoRepeatDelay(500)  # Initial delay in ms
        button.clicked.connect(slot_function)


    def update_labels(self, position):
        # Calculate time components
        milliseconds = (position % 1000)
        seconds = (position / 1000) % 60
        minutes = (position / (1000 * 60)) % 60
        hours = (position / (1000 * 60 * 60)) % 24
        timestamp = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{int(milliseconds):03}"
        self.controlPanel.timestampValueLabel.setText(timestamp)

        # Calculate frame number
        current_frame = int(position / (1000 / self.frame_rate))
        total_frames = int(self.mediaPlayer.duration() / (1000 / self.frame_rate))
        self.controlPanel.frameNumberValueLabel.setText(f"{current_frame}/{total_frames}")


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
        # self.ensure_media_ready()
        frame_duration = int(round(1000 / self.frame_rate))
        current_position = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(current_position + frame_duration)
        self.mediaPlayer.pause()

    def step_backward(self):
        # self.ensure_media_ready()
        frame_duration = int(round(1000 / self.frame_rate))
        current_position = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(current_position - frame_duration)
        self.mediaPlayer.pause()




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