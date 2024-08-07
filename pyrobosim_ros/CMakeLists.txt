cmake_minimum_required(VERSION 3.22)
project(pyrobosim_ros)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Enforce dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

# Install pyrobosim Python package
ament_python_install_package(
  pyrobosim
  PACKAGE_DIR ../pyrobosim/pyrobosim)
install(PROGRAMS
  examples/demo.py
  examples/demo_commands.py
  examples/demo_pddl_world.py
  examples/demo_pddl_planner.py
  examples/demo_pddl_goal_publisher.py
  examples/demo_velocity_publisher.py
  ../pyrobosim/examples/demo_prm.py
  ../pyrobosim/examples/demo_rrt.py
  ../pyrobosim/examples/demo_pddl.py
  ../pyrobosim/examples/demo_world_save.py
  experiments/exp_demo.py
  experiments/world1.py
  experiments/world_mx.py
  experiments/world_fam.py
  experiments/world_eva.py
  experiments/planner.py
  experiments/planner_2.py
  experiments/commander.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install pyrobosim_ros Python package
ament_python_install_package(
  pyrobosim_ros
  PACKAGE_DIR pyrobosim_ros)

# Install data files
install(DIRECTORY
  ../pyrobosim/pyrobosim/data
  DESTINATION share/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

# Build tests if enabled
if(BUILD_TESTING)
  add_subdirectory(test)
endif()

ament_package()
