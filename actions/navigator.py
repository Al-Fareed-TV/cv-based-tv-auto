from dotenv import load_dotenv
import yaml
import os
import time
load_dotenv()
class NavigationNotFound(Exception):
    pass

class Navigator:
    def __init__(self, executor):
        nav_map_path = "config/navigation_map.yaml"

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

        dest_map = self.nav_map[current_focus]

        if destination not in dest_map:
            raise NavigationNotFound(
                f"No navigation path from {current_focus} to {destination}"
            )

        actions = dest_map[destination]["keys"]

        self._execute_actions(actions, delay)

        return actions  # optional, useful for logging/debug

    def _execute_actions(self, actions, delay):
        for action in actions:
                self.executor.send_key(action)
                time.sleep(delay)
