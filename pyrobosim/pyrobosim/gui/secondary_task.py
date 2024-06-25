from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget, QApplication, QLabel
from PySide6.QtCore import Qt
import random

class GridCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.grid_squares = []
        self.grid_size = (15, 15)  # Change the grid size as per your requirement
        self.checked_buttons = []
        self.setup_grid()

    def setup_grid(self):
        layout = QGridLayout(self)
        widget = QWidget(self)
        widget.setLayout(layout)

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                grid_square = QPushButton()
                grid_square.setCheckable(True)
                grid_square.clicked.connect(self.change_button_color)  # Add callback here
                layout.addWidget(grid_square, i, j)
                self.grid_squares.append(grid_square)

        self.ax.axis('off')
        self.draw()

    def change_button_color(self):
        button = self.sender()
        if button.isChecked():
            button.setStyleSheet("background-color: green")  # Change to desired color
            self.checked_buttons.append(button)
        else:
            button.setStyleSheet("")  # Reset to default color
            self.checked_buttons.remove(button)
        self.reset_checked_buttons()

    def uncheck_button(self, button):
        button.setChecked(False)
        button.setStyleSheet("")  # Reset to default color

    def reset_checked_buttons(self):
        if len(self.checked_buttons) > 4:
                random_button = random.choice(self.checked_buttons)
                random_button.setChecked(False)
                random_button.setStyleSheet("")  # Reset to default color
