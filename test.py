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
        frame = int(position / (1000 / 30))  # Assuming 30 fps
        if 25 <= frame <= 75:
            self.overlay.show()
        else:
            self.overlay.hide()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view.setSceneRect(QRectF(self.view.rect()))
        self.videoItem.setSize(self.view.size())
        self.overlay.setRect(self.videoItem.boundingRect())

if __name__ == "__main__":
    video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
    app = QApplication(sys.argv)
    player = VideoPlayer(video_path)  # Change to your video path
    player.resize(800, 600)
    player.show()
    sys.exit(app.exec())