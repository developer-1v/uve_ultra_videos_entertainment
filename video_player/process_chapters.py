from print_tricks import pt
pt.easy_import()

import bisect

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen, QBrush

from utility_read_metadata import get_chapters_by_prefix, read_metadata

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




class FrameProcessor:
    def __init__(self, video_path, prefix):
        self.video_path = video_path
        self.metadata = read_metadata(video_path)
        
        # Get chapters and convert START/END to integers
        chapters = get_chapters_by_prefix(self.metadata, prefix)
        for chapter in chapters:
            chapter['START'] = int(chapter['START'])
            chapter['END'] = int(chapter['END'])
        
        # Sort chapters by START time
        self.chapters = sorted(chapters, key=lambda x: x['START'])
        
        # Create start_frames list after sorting
        self.start_frames = [chapter['START'] for chapter in self.chapters]
        self.current_chapter = None


    def update_overlay(self, current_frame, overlay):
        """
        Update the overlay visibility based on the current frame using binary search.
        """
        # Now both current_frame and self.start_frames contain integers
        idx = bisect.bisect_right(self.start_frames, current_frame) - 1
        if idx >= 0 and self.chapters[idx]['START'] <= current_frame <= self.chapters[idx]['END']:
            if self.current_chapter != self.chapters[idx]:
                self.current_chapter = self.chapters[idx]
                overlay.show()
        else:
            if self.current_chapter is not None:
                self.current_chapter = None
                overlay.hide()

# if __name__ == "__main__":
#     video_path = r'C:\.PythonProjects\uve_ultra_videos_entertainment\videos_for_testing\tiny_vids\3_complete_vids_to_test\marked__s01e01_40.mp4'
#     frame_processor = FrameProcessor(video_path)
#     frame_processor.update_overlay(100, overlay)
