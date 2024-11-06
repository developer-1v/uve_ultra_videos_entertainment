import cv2
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget

class ChapterOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chapters = [
            {'start_frame': 100, 'end_frame': 200},
            {'start_frame': 400, 'end_frame': 500}
        ]
        self.current_frame = 0
        self.set_transparent_overlay()

    def set_transparent_overlay(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(255, 0, 0, 128))  # Red with 50% opacity
        painter.setPen(Qt.NoPen)
        for chapter in self.chapters:
            if chapter['start_frame'] <= self.current_frame <= chapter['end_frame']:
                painter.drawRect(self.rect())  # Draw overlay
                break

    def update_frame(self, frame_number):
        self.current_frame = frame_number
        self.update()  # Trigger a repaint

    def is_in_chapter(current_frame, chapters):
        """
        Check if the current frame is within any of the chapters.
        Each chapter is a tuple (start_frame, end_frame).
        """
        for start, end in chapters:
            if start <= current_frame <= end:
                return True
        return False
# This class needs to be integrated with the video player's frame update mechanism.