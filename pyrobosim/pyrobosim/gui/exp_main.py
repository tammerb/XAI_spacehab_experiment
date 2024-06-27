import signal
import sys

from pyrobosim.gui import PyRoboSimMainWindow
from pyrobosim.gui import PyRoboSimGUI

from PySide6 import QtWidgets
from PySide6.QtCore import QTimer

from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT

from .exp_world_canvas import SpaceWorldCanvas
from .secondary_task import GridCanvas

def start_gui(world):
    """
    Helper function to start a pyrobosim GUI for a world model.

    :param world: World object to attach to the GUI.
    :type world: :class:`pyrobosim.core.world.World`

    app  = custom SpaceHabSimGUI object
    """
    app = SpaceHabSimGUI(world, sys.argv)

    signal.signal(signal.SIGINT, lambda *args: app.quit())

    timer = QTimer(parent=app)
    timer.timeout.connect(lambda: None)
    timer.start(1000)

    sys.exit(app.exec_())

class SpaceHabSimGUI(PyRoboSimGUI):
    """Inherits from PyRoboSimGUI but calls the custom main_window."""
    def __init__(self, world, args, show=True):
        super(PyRoboSimGUI, self).__init__(args, show=show)
        self.world = world
        self.main_window = SpaceHabSimMainWindow(world, show)
        self.main_window.show()

class SpaceHabSimMainWindow(PyRoboSimMainWindow):
    """Main window for the Space Habitat Simulator"""

    def __init__(self, world, show=True, *args, **kwargs):
        super(PyRoboSimMainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("pyrobosim")
        self.set_window_dims()

        # Connect the GUI to the world
        self.world = world
        self.world.gui = self
        self.world.has_gui = True

        self.layout_created = False
        self.canvas = SpaceWorldCanvas(self, world, show)
        #self.secondary_canvas = GridCanvas(self)
        self.secondary_canvas = GridCanvas(self)
        self.create_layout()
        self.canvas.show()



    def create_layout(self):
        """Creates the main GUI layout."""
        self.main_widget = QtWidgets.QWidget()

        # Push buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.rand_pose_button = QtWidgets.QPushButton("Randomize robot pose")
        self.rand_pose_button.clicked.connect(self.rand_pose_cb)
        self.buttons_layout.addWidget(self.rand_pose_button)
        self.rand_goal_button = QtWidgets.QPushButton("Randomize nav goal")
        self.rand_goal_button.clicked.connect(self.rand_goal_cb)
        self.buttons_layout.addWidget(self.rand_goal_button)
        self.switch_task_button = QtWidgets.QPushButton("Switch task")
        self.switch_task_button.clicked.connect(self.switch_task_cb)
        self.buttons_layout.addWidget(self.switch_task_button)

        # Robot edit box
        self.robot_layout = QtWidgets.QGridLayout()
        self.robot_layout.addWidget(QtWidgets.QLabel("Robot name:"), 0, 1)
        self.robot_textbox = QtWidgets.QComboBox()
        robot_names = [r.name for r in self.world.robots]
        self.robot_textbox.addItems(robot_names)
        self.robot_textbox.setEditable(True)
        self.robot_textbox.currentTextChanged.connect(self.update_manip_state)
        self.robot_layout.addWidget(self.robot_textbox, 0, 2, 0, 8)

        # Goal query edit box
        self.goal_layout = QtWidgets.QGridLayout()
        self.goal_layout.addWidget(QtWidgets.QLabel("Goal query:"), 0, 1)
        self.goal_textbox = QtWidgets.QLineEdit()
        self.goal_layout.addWidget(self.goal_textbox, 0, 2, 0, 8)

        # Action buttons
        self.action_layout = QtWidgets.QHBoxLayout()
        self.nav_button = QtWidgets.QPushButton("Navigate")
        self.nav_button.clicked.connect(self.on_navigate_click)
        self.action_layout.addWidget(self.nav_button)
        self.pick_button = QtWidgets.QPushButton("Pick")
        self.pick_button.clicked.connect(self.on_pick_click)
        self.action_layout.addWidget(self.pick_button)
        self.place_button = QtWidgets.QPushButton("Place")
        self.place_button.clicked.connect(self.on_place_click)
        self.action_layout.addWidget(self.place_button)

        # World layout (Matplotlib affordances)
        self.world_layout = QtWidgets.QVBoxLayout()
        self.nav_toolbar = NavigationToolbar2QT(self.canvas, self)
        self.addToolBar(QtCore.Qt.BottomToolBarArea, self.nav_toolbar)  # remove this for experimental setup.

        # Stacked Widget layout
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.canvas)
        self.stacked_widget.addWidget(self.secondary_canvas)
        self.world_layout.addWidget(self.stacked_widget)
        self.canvas_index=0 

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.addLayout(self.robot_layout)
        self.main_layout.addLayout(self.goal_layout)
        self.main_layout.addLayout(self.action_layout)
        self.main_layout.addLayout(self.world_layout)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
        self.layout_created = True

    def closeEvent(self, _):
        """Cleans up running threads on closing the window."""
        self.canvas.nav_animator.stop()
        self.canvas.nav_animator.wait()

    def switch_task_cb(self):
        if self.canvas_index == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.canvas_index = 1
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.canvas_index = 0
        self.canvas.show_world_state(navigating=True)
        self.canvas.draw()