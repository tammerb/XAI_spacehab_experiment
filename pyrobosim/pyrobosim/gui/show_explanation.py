def show_explanation(self, robot=None, navigating=False):
    goal = "sort the shapes." # hard program this for now
    if robot is not None:
        title_bits = []
        title_bits.append(f"The current goal is to {goal}")
        if robot.current_action is not None:
            title_bits.append(f"Current action: {robot.current_action}")
        else:
            title_bits.append(" ")
        title_str = f"\n".join(title_bits)
        title_str = title_str.replace("_ ", " ")
        title_str = title_str.replace("_,", "")
        title_str = title_str.replace("[robot] ", "")
        title_str = title_str.replace("Cost: 0.000", "")
        self.axes.set_title(title_str)