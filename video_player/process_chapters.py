import cv2
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget
from print_tricks import pt

class ChapterOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chapters = [
            {'start_frame': 3, 'end_frame': 33},
            {'start_frame': 55, 'end_frame': 88}
        ]
        self.current_frame = 0
        self.set_transparent_overlay()
        self.show()  # Ensure the widget is shown

    def showEvent(self, event):
        super().showEvent(event)
        print("Overlay shown")

    def hideEvent(self, event):
        super().hideEvent(event)
        print("Overlay hidden")

    def set_transparent_overlay(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)  # Ensure background is not filled

    def paintEvent(self, event):
        print(f"Overlay size: {self.size()}, position: {self.pos()}")
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setBrush(QColor(255, 0, 0, 128))
        painter.drawRect(self.rect())
        painter.fillRect(self.rect(), QColor(255, 0, 0, 128))
        
        for chapter in self.chapters:
            print(f"Checking chapter: {chapter}")  # Debugging statement
            if chapter['start_frame'] <= self.current_frame <= chapter['end_frame']:
                print("Drawing rectangle")  # Debugging statement
                painter.drawRect(self.rect())  # Draw overlay
                break
        else:
            print("Not in any chapter")  # Debugging statement
            painter.fillRect(self.rect(), QColor(0, 0, 0, 0))  # Clear the overlay if not in chapter

    def update_frame(self, frame_number):
        self.current_frame = frame_number
        self.update()  # Trigger a repaint

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