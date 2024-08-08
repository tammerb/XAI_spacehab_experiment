#!/usr/bin/env python3

"""
Example showing how to request task actions and plans.
"""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import time

from pyrobosim_msgs.action import ExecuteTaskAction, ExecuteTaskPlan
from pyrobosim_msgs.msg import TaskAction, TaskPlan
from pyrobosim_msgs.srv import RequestWorldState


class Commander(Node):
    def __init__(self):
        super().__init__("commander")

        self.declare_parameter("mode", value="action")

        # Action client for a single action
        self.action_client = ActionClient(self, ExecuteTaskAction, "execute_action")

        # Action client for a task plan
        self.plan_client = ActionClient(self, ExecuteTaskPlan, "execute_task_plan")

        # Call world state service to ensure node is running
        self.world_state_client = self.create_client(
            RequestWorldState, "request_world_state"
        )
        while rclpy.ok() and not self.world_state_client.wait_for_service(
            timeout_sec=1.0
        ):
            self.get_logger().info("Waiting for world state server...")
        future = self.world_state_client.call_async(RequestWorldState.Request())
        rclpy.spin_until_future_complete(self, future)

    def send_action_goal(self, goal):
        self.action_client.wait_for_server()
        return self.action_client.send_goal_async(goal)

    def send_plan_goal(self, goal):
        self.plan_client.wait_for_server()
        return self.plan_client.send_goal_async(goal)


def main():
    rclpy.init()
    cmd = Commander()

    # Choose between action or plan command, based on input parameter.
    mode = cmd.get_parameter("mode").value
    if mode == "action":
        cmd.get_logger().info("Executing task action...")
        goal = ExecuteTaskAction.Goal()
        goal.action = TaskAction(robot="robot", type="navigate", target_location="service_module")
        cmd.send_action_goal(goal)

    elif mode == "plan":
        cmd.get_logger().info("Executing task plan...")
        task_actions = [
            TaskAction(type="navigate", target_location="workspace"),
            TaskAction(type="pick", object="square"),
            TaskAction(type="navigate", target_location="bin"),
            TaskAction(type="place"),
            TaskAction(type="navigate", target_location="module"),
        ]
        goal = ExecuteTaskPlan.Goal()
        goal.plan = TaskPlan(robot="robot", actions=task_actions)
        cmd.send_plan_goal(goal)

    elif mode == "multirobot-plan":
        cmd.get_logger().info("Executing multirobot task plan...")
        task_actions = [
            TaskAction(type="navigate", target_location="desk"),
            TaskAction(type="pick", object="water"),
            TaskAction(type="navigate", target_location="counter"),
            TaskAction(type="place"),
            TaskAction(type="navigate", target_location="kitchen"),
        ]
        goal = ExecuteTaskPlan.Goal()
        goal.plan = TaskPlan(robot="robot0", actions=task_actions)
        cmd.send_plan_goal(goal)

        time.sleep(2.0)

        task_actions = [
            TaskAction(type="navigate", target_location="table"),
            TaskAction(type="pick", object="apple"),
            TaskAction(type="navigate", target_location="desk"),
            TaskAction(type="place"),
            TaskAction(type="navigate", target_location="bedroom"),
        ]
        goal = ExecuteTaskPlan.Goal()
        goal.plan = TaskPlan(robot="robot1", actions=task_actions)
        cmd.send_plan_goal(goal)

        time.sleep(2.0)

        task_actions = [
            TaskAction(type="navigate", target_location="table"),
            TaskAction(type="pick", object="banana"),
            TaskAction(type="navigate", target_location="counter0_left"),
            TaskAction(type="place"),
        ]
        goal = ExecuteTaskPlan.Goal()
        goal.plan = TaskPlan(robot="robot2", actions=task_actions)
        cmd.send_plan_goal(goal)

    else:
        cmd.get_logger().error(f"Invalid mode specified: {mode}")

    rclpy.spin(cmd)
    cmd.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
