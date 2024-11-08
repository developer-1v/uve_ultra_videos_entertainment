import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                              QGraphicsScene, QGraphicsView, QGraphicsRectItem)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QPen, QBrush



class VideoPlayer(QMainWindow):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player with Overlay")
        
        # Create graphics scene and view
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setViewportMargins(0, 0, 0, 0)
        self.view.setFrameStyle(0)
        
        
        # Create video item for graphics scene
        self.videoItem = QGraphicsVideoItem()
        self.scene.addItem(self.videoItem)
        
        # Create media player
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoItem)
        from PySide6.QtCore import QUrl
        self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))
        
        # Create overlay rectangle
        self.overlay = QGraphicsRectItem(self.videoItem.boundingRect())
        self.overlay.setBrush(QBrush(QColor(255, 0, 0, 128)))
        self.overlay.setPen(QPen(Qt.NoPen))
        self.scene.addItem(self.overlay)
        self.overlay.setZValue(1)  # Ensure overlay is above video
        
        # Set up the main window
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Connect position updates
        self.mediaPlayer.positionChanged.connect(self.update_overlay)
        self.mediaPlayer.setLoops(QMediaPlayer.Infinite)
        self.mediaPlayer.play()
        
    def update_overlay(self, position):
        duration = self.mediaPlayer.duration()
        if duration > 0:
            # Calculate normalized position (0 to duration)
            normalized_position = position % duration
            
            # Convert to frames (assuming 30 fps)
            frame = int((normalized_position / duration) * (30 * (duration/1000)))
            
            # Show overlay between frames 25-75 for each loop
            normalized_frame = frame % (30 * (duration/1000))  # Normalize frame count to one loop
            if 25 <= normalized_frame <= 75:
                self.overlay.show()
                self.overlay.setRect(self.videoItem.boundingRect())
            else:
                self.overlay.hide()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Fit scene to view without margins
        self.view.setSceneRect(0, 0, self.view.width(), self.view.height())
        self.videoItem.setSize(self.view.size())
        self.overlay.setRect(self.videoItem.boundingRect())

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)  # Change to your video path
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())