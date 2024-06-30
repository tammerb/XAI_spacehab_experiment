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
from ..utils.knowledge import query_to_entity

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
        self.switch_task_button = QtWidgets.QPushButton("Switch task")
        self.switch_task_button.clicked.connect(self.switch_task_cb)
        self.buttons_layout.addWidget(self.switch_task_button)

        # Object Action Box
        self.object_layout = QtWidgets.QHBoxLayout()
        self.object_layout.addWidget(QtWidgets.QLabel("Object Selector:"))
        self.object_textbox = QtWidgets.QComboBox()
        object_names = [r.name for r in self.world.objects]
        self.object_textbox.addItems(object_names)
        self.object_textbox.setEditable(True)
        self.object_textbox.currentTextChanged.connect(self.update_manip_state)
        self.object_layout.addWidget(self.object_textbox)
        self.pick_button = QtWidgets.QPushButton("Pick")
        self.pick_button.clicked.connect(self.on_pick_click)
        self.object_layout.addWidget(self.pick_button)
        self.place_button = QtWidgets.QPushButton("Place")
        self.place_button.clicked.connect(self.on_place_click)
        self.object_layout.addWidget(self.place_button)

        # Object Action Box
        self.navigation_layout = QtWidgets.QHBoxLayout()
        self.navigation_layout.addWidget(QtWidgets.QLabel("Location Selector:"))
        self.location_textbox = QtWidgets.QComboBox()
        location_names = [r.name for r in self.world.locations]
        self.location_textbox.addItems(location_names)
        self.location_textbox.setEditable(True)
        self.location_textbox.currentTextChanged.connect(self.update_manip_state)
        self.navigation_layout.addWidget(self.location_textbox)
        self.nav_button = QtWidgets.QPushButton("Navigate")
        self.nav_button.clicked.connect(self.on_navigate_click)
        self.navigation_layout.addWidget(self.nav_button)

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
        self.main_layout.addLayout(self.object_layout)
        self.main_layout.addLayout(self.navigation_layout)
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
    
    def get_current_robot(self):
        return self.world.get_robot_by_name("robot")
    
    def on_navigate_click(self):
        """Callback to navigate to a goal location."""
        robot = self.get_current_robot()
        if robot and robot.executing_action:
            return

        query_list = [elem for elem in self.location_textbox.currentText().split(" ") if elem]
        loc = query_to_entity(
            self.world,
            query_list,
            mode="location",
            robot=robot,
            resolution_strategy="nearest",
        )
        if not loc:
            return
        
        print(f"[{robot.name}] Navigating to {loc}")
        self.canvas.navigate_in_thread(robot, loc)

    def on_pick_click(self):
        """Callback to pick an object."""
        robot = self.get_current_robot()
        if robot:
            loc = robot.location
            query_list = [elem for elem in self.object_textbox.currentText().split(" ") if elem]
            if loc:
                query_list.append(loc.name)
            obj = query_to_entity(
                self.world,
                query_list,
                mode="object",
                robot=robot,
                resolution_strategy="nearest",
            )
            if obj:
                print(f"[{robot.name}] Picking {obj.name}")
                self.canvas.pick_object(robot, obj)
                self.update_manip_state()

    def set_buttons_during_action(self, state):
        """
        Enables or disables buttons that should not be pressed while
        the robot is executing an action.

        :param state: Desired button state (True to enable, False to disable)
        :type state: bool
        """
        self.nav_button.setEnabled(state)
        self.pick_button.setEnabled(state)
        self.place_button.setEnabled(state)