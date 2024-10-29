# gui.py
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QSize

class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Processing GUI")
        self.setMinimumSize(QSize(800, 600))
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # Top grid section
        top_label = QLabel("Top Section")
        top_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        layout.addWidget(top_label, 0, 0, 1, 3)  # Row, Column, RowSpan, ColumnSpan

        # Middle grid section
        left_label = QLabel("Left Cell")
        left_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        center_label = QLabel("Center Cell")
        center_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        right_label = QLabel("Right Cell")
        right_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        layout.addWidget(left_label, 1, 0)
        layout.addWidget(center_label, 1, 1)
        layout.addWidget(right_label, 1, 2)
        layout.setColumnStretch(1, 3)  # Making the center cell larger

        # Bottom grid section
        bottom_label = QLabel("Bottom Section")
        bottom_label.setFrameStyle(QFrame.Box | QFrame.Plain)
        layout.addWidget(bottom_label, 2, 0, 1, 3)

        # Split in center cell
        center_frame = QFrame()
        center_layout = QGridLayout(center_frame)
        top_center_label = QLabel("Top Split")
        bottom_center_label = QLabel("Bottom Split")
        center_layout.addWidget(top_center_label, 0, 0)
        center_layout.addWidget(bottom_center_label, 1, 0)
        center_layout.setRowStretch(0, 95)
        center_layout.setRowStretch(1, 5)
        layout.addWidget(center_frame, 1, 1)

def run():
    app = QApplication([])
    window = MainGUI()
    window.show()
    app.exec()

if __name__ == "__main__":
    run()