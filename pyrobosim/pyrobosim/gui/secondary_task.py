from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QPushButton, QGridLayout, QWidget, QApplication, QLabel
from PySide6.QtCore import Qt
import random
from time import sleep

class GridCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.grid_squares = []
        self.grid_size = (15, 25)  # Change the grid size as per your requirement
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
                grid_square.clicked.connect(self.check_button)  # Add callback here
                layout.addWidget(grid_square, i, j)
                self.grid_squares.append(grid_square)
        self.grid_squares[2].setChecked(True)
        self.grid_squares[2].setStyleSheet("background-color: green")
        self.checked_buttons.append(self.grid_squares[2])
        self.ax.axis('off')
        self.draw()

    def check_button(self):
        button = self.sender()
        if button.isChecked():
            button.setStyleSheet("background-color: green")  # Change to desired color
            self.checked_buttons.append(button)
        else:
            button.setStyleSheet("")  # Reset to default color
            self.checked_buttons.remove(button)
            self.randomly_check_buttons()

    def randomly_check_buttons(self):
        """Loops through all grid_squares and randomly checks 10% of the unchecked buttons."""
        for button in self.grid_squares:
            if not button.isChecked() and random.random() < 0.002:
                button.setChecked(True)
                button.setStyleSheet("background-color: green")
                self.checked_buttons.append(button)

        if len(self.checked_buttons) == 0:
            self.randomly_check_buttons()