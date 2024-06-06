from pyrobosim.gui.world_canvas import WorldCanvas, NavAnimator

#class SpaceNavAnimator(NavAnimator):
#    pass

class SpaceWorldCanvas(WorldCanvas):
    print("Using SpaceWorldCanvas")
    #pass
    def show_world_state(self, robot=None, navigating=False):
        print("Calling MY show_world_state")

        if robot is not None:
            title_bits = []
            if navigating:
                robot_loc = self.world.get_location_from_pose(robot.get_pose())
                if robot_loc is not None:
                    title_bits.append(f"My Location: {robot_loc.name}")
            elif robot.location is not None:
                if isinstance(robot.location, str):
                    robot_loc = robot.location
                else:
                    robot_loc = robot.location.name
                title_bits.append(f"My Location: {robot_loc}")
            if robot.manipulated_object is not None:
                title_bits.append(f"Holding: {robot.manipulated_object.name}")
            title_str = f"[{robot.name}] " + ", ".join(title_bits)
            self.axes.set_title(title_str)

        
