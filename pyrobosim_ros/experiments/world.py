#!/usr/bin/env python3

"""
Example showing how to build a world and use it with pyrobosim,
additionally starting up a ROS interface.
"""
import os
import rclpy
import threading

from pyrobosim.core import Robot, World, WorldYamlLoader
from pyrobosim.gui.exp_main import start_gui
from pyrobosim.utils.general import get_data_folder
from pyrobosim_ros.ros_interface import WorldROSWrapper
from pyrobosim.navigation import ConstantVelocityExecutor, PathPlanner
from pyrobosim.navigation import OccupancyGrid
from pyrobosim.utils.pose import Pose

default_world_file = "world1_data.yaml"

def load_world():
    """Load a test world."""
    world_file = os.path.join(get_data_folder(), default_world_file)
    return WorldYamlLoader().from_yaml(world_file)

def create_world_from_yaml(world_file):
    return WorldYamlLoader().from_yaml(os.path.join(get_data_folder(), world_file))

def main():
    """Initializes ROS node"""
    rclpy.init()

    node = WorldROSWrapper(state_pub_rate=0.1, dynamics_rate=0.01)
    node.declare_parameter("world_file", value="")

    # Set the world
    world_file = node.get_parameter("world_file").get_parameter_value().string_value
    if world_file == "":
        node.get_logger().info(f"Using default world file {default_world_file}.")
        world = load_world()
    else:
        node.get_logger().info(f"Using world file {world_file}.")
        world = create_world_from_yaml(world_file)

    node.set_world(world)


    # Start ROS node in separate thread
    ros_thread = threading.Thread(target=lambda: node.start(wait_for_gui=True))
    ros_thread.start()

    # Start GUI in main thread
    start_gui(node.world)

    return


if __name__ == "__main__":
    node = main()
