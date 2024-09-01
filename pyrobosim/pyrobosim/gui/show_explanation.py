import numpy as np

def show_explanation(self, robot=None, navigating=False):
    goal = "sort all of the shapes" # hard program this for now
    if robot is not None:
        title_bits = []
        title_bits.append(f"The current goal is to {goal}.\n")

        # Add the current action
        title_bits.append("Current action:")
        if robot.current_action is not None:
            action = str(robot.current_action)
            #action.replace("square1", "triangle2")
            title_bits.append(f"{action}\n")
        else:
            title_bits.append("\n")
        
        title_bits.append("Grasped object:")
        if robot.manipulated_object is not None:
            object = str(robot.manipulated_object.name)
            #object.replace("square1", "triangle2")
            title_bits.append(f"{object}\n")
        else:
            title_bits.append("none\n")

        # Add the current failure status
        if robot.failure is not None:
            title_bits.append(f"Action failed: {robot.failure}")
        else:
            title_bits.append(" ")
        
        title_str = f"\n".join(title_bits)
        title_str = title_str.replace("_ ", " ")
        title_str = title_str.replace("_,", "")
        title_str = title_str.replace("[robot] ", "")
        title_str = title_str.replace("Cost: 0.000", "")
        self.axes.set_title(title_str)