import yaml
import os

class NavigationNotFound(Exception):
    pass
class Navigator:
    def __init__(self, nav_map_path):
        if not os.path.exists(nav_map_path):
            raise FileNotFoundError(nav_map_path)

        with open(nav_map_path, "r") as f:
            self.nav_map = yaml.safe_load(f)

    def goto(self, current_focus, destination):
        if current_focus not in self.nav_map:
            raise NavigationNotFound(
                f"No navigation defined for focus: {current_focus}"
            )

        dest_map = self.nav_map[current_focus]

        if destination not in dest_map:
            raise NavigationNotFound(
                f"No navigation path from {current_focus} to {destination}"
            )

        return dest_map[destination]["keys"]
