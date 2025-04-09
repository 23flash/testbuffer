#!/usr/bin/env python3
import os
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QMessageBox,
                             QPushButton, QWidget)


class ButtonGridApp(QWidget):
    def __init__(self, use_framebuffer=True):
        super().__init__()
        self.use_framebuffer = use_framebuffer
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Button Grid")

        # Set framebuffer mode if requested
        if self.use_framebuffer:
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        else:
            # For development mode, set a reasonable window size
            self.resize(400, 300)

        # Create grid layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # Create 6 buttons arranged in a 3x2 grid
        button_titles = [
            "Button 1",
            "Button 2",
            "Button 3",
            "Button 4",
            "Button 5",
            "Button 6",
        ]

        positions = [(i, j) for i in range(2) for j in range(3)]

        for position, title in zip(positions, button_titles):
            button = QPushButton(title)
            button.setMinimumHeight(80)  # Make buttons larger for touch interfaces
            button.clicked.connect(lambda checked, t=title: self.buttonClicked(t))
            grid.addWidget(button, *position)

        self.setLayout(grid)

    def buttonClicked(self, title):
        print(f"{title} was clicked!")

        # Show a message box in development mode
        if not self.use_framebuffer:
            QMessageBox.information(self, "Button Clicked", f"{title} was clicked!")


def main():
    # Parse command line arguments
    use_framebuffer = "--dev" not in sys.argv

    app = QApplication(sys.argv)

    # Configure framebuffer if we're using it
    if use_framebuffer:
        try:
            # Set the QT_QPA_PLATFORM environment variable to 'linuxfb' for framebuffer
            os.environ["QT_QPA_PLATFORM"] = "linuxfb"

            # Uncomment and modify these lines as needed for your specific hardware
            # os.environ["QT_QPA_FB_DRM"] = "1"  # For DRM framebuffer
            # os.environ["QT_QPA_FB_DRM_DEVICE"] = "/dev/dri/card0"  # Specify DRM device
            # or for traditional framebuffer:
            # os.environ["QT_QPA_GENERIC_PLUGINS"] = "evdevkeyboard:/dev/input/event0,evdevmouse:/dev/input/event1"

            print("Running in framebuffer mode")
        except Exception as e:
            use_framebuffer = False
            print(f"Failed to set up framebuffer: {e}")
            print("Falling back to development mode")
    else:
        print("Running in development mode")

    window = ButtonGridApp(use_framebuffer)

    if use_framebuffer:
        window.showFullScreen()
    else:
        window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
