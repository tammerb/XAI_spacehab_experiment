import numpy as np

def show_explanation(self, robot=None, navigating=False):
    goal = "sort the shapes" # hard program this for now
    if robot is not None:
        title_bits = []
        title_bits.append(f"The current goal is to {goal}.\n")


        # Add movement status
        if robot.executing_nav:
            title_bits.append(f"The robot is moving.")
            # Add manipulation status
            if robot.manipulated_object is not None:
                fake_object = str(robot.manipulated_object.name)
                fake_object.replace("square1", "triangle2")
                title_bits.append(f"The robot is holding {fake_object}.")
            else:
                title_bits.append("The robot is not holding any object.")
        else:
            title_bits.append("The robot is not moving.\n")
        
            
        # Add the current action
        if robot.current_action is not None:
            fake_action = str(robot.current_action)
            fake_action.replace("square1", "triangle2")
            title_bits.append(f"Current objective: {fake_action}")
        else:
            title_bits.append(" ")

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