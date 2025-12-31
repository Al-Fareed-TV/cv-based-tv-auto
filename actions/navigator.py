import yaml
import os
import time


class NavigationNotFound(Exception):
    pass


class Navigator:
    def __init__(self, executor, nav_map_path="config/navigation_map.yaml"):
        if not executor:
            raise ValueError("Navigator requires an executor")

        if not os.path.exists(nav_map_path):
            raise FileNotFoundError(nav_map_path)

        with open(nav_map_path, "r") as f:
            self.nav_map = yaml.safe_load(f)

        self.executor = executor

    def goto(self, current_focus, destination, delay=0.4):
        if current_focus not in self.nav_map:
            raise NavigationNotFound(
                f"No navigation defined for focus: {current_focus}"
            )

        if destination not in self.nav_map[current_focus]:
            raise NavigationNotFound(
                f"No navigation path from {current_focus} to {destination}"
            )

        keys = self.nav_map[current_focus][destination]["keys"]

        for key in keys:
            self.executor.send_key(key)
            time.sleep(delay)