from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
from PySide6.QtWidgets import QCheckBox, QVBoxLayout, QWidget, QApplication
import matplotlib.pyplot as plt

class GridCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.checkboxes = []
        self.grid_size = (5, 5)  # Change the grid size as per your requirement

        self.setup_grid()

    def setup_grid(self):
        layout = QVBoxLayout(self)
        widget = QWidget(self)
        widget.setLayout(layout)

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                checkbox = QCheckBox()
                layout.addWidget(checkbox)
                self.checkboxes.append(checkbox)

        self.ax.axis('off')
        self.draw()

# Example usage
if __name__ == '__main__':

    app = QApplication(sys.argv)
    grid_canvas = GridCanvas()
    grid_canvas.show()
    sys.exit(app.exec_())