from print_tricks import pt

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush

class ChapterOverlay(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_scene()
        self.setup_view()
        self.setup_video_item()
        self.setup_overlay()
    
    def setup_scene(self):
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
    
    def setup_view(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setFrameStyle(0)
    
    def setup_video_item(self):
        self.videoItem = QGraphicsVideoItem()
        self.scene.addItem(self.videoItem)
    
    def setup_overlay(self):
        self.overlay = QGraphicsRectItem(self.videoItem.boundingRect())
        self.overlay.setBrush(QBrush(QColor(255, 0, 0, 128)))
        self.overlay.setPen(QPen(Qt.NoPen))
        self.scene.addItem(self.overlay)
        self.overlay.setZValue(1)
        self.overlay.hide()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setSceneRect(0, 0, self.width(), self.height())
        self.videoItem.setSize(self.size())
        self.overlay.setRect(self.videoItem.boundingRect())
    
    def show_overlay(self):
        self.overlay.show()
        self.overlay.setRect(self.videoItem.boundingRect())
    
    def hide_overlay(self):
        self.overlay.hide()

    @staticmethod
    def is_in_chapter(current_frame, chapters):
        """
        Check if the current frame is within any of the chapters.
        Each chapter is a dictionary with 'start_frame' and 'end_frame'.
        """
        pt(current_frame)
        for chapter in chapters:
            if chapter['start_frame'] <= current_frame <= chapter['end_frame']:
                pt('true')
                return True
        pt('false')
        return False