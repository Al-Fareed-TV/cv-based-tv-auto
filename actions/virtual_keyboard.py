class KeyboardLayout:
    KEYBOARD = [
        ["a", "b", "c", "d", "e", "f", "g", "clear"],
        ["h", "i", "j", "k", "l", "m", "n", "sym"],
        ["o", "p", "q", "r", "s", "t", "u"],
        ["v", "w", "x", "y", "z", ",", ".", "caps"],
        ["key_settings", "key_space", "key_space", "key_space", "key_search", "key_search", "key_left", "key_right"],
    ]

    POSITION_MAP = {
        key: {"row": r, "col": c}
        for r, row in enumerate(KEYBOARD)
        for c, key in enumerate(row)
    }

class KeyboardNavigator:
    def __init__(self, start_char="a"):
        start_char = start_char.lower()
        if start_char not in KeyboardLayout.POSITION_MAP:
            raise ValueError(f"Invalid start character: {start_char}")

        pos = KeyboardLayout.POSITION_MAP[start_char]
        self.current_row = pos["row"]
        self.current_col = pos["col"]

    def move_to(self, key):
        key = key.lower()
        if key not in KeyboardLayout.POSITION_MAP:
            raise ValueError(f"Key not found on keyboard: {key}")

        target = KeyboardLayout.POSITION_MAP[key]
        actions = []

        while self.current_row < target["row"]:
            actions.append("KEY_DOWN")
            self.current_row += 1
        while self.current_row > target["row"]:
            actions.append("KEY_UP")
            self.current_row -= 1

        while self.current_col < target["col"]:
            actions.append("KEY_RIGHT")
            self.current_col += 1
        while self.current_col > target["col"]:
            actions.append("KEY_LEFT")
            self.current_col -= 1

        actions.append("KEY_ENTER")
        return actions


def generate_actions_for_input(value, start_char="a"):
    """
    Handles BOTH:
    - normal text: "sony"
    - special keys: "key_space", "key_search"
    """
    navigator = KeyboardNavigator(start_char)
    actions = []

    value = value.lower()

    # ✅ Special keyboard key
    if value.startswith("key_"):
        actions.extend(navigator.move_to(value))
        return actions

    # ✅ Normal word typing
    for ch in value:
        actions.extend(navigator.move_to(ch))

    return actions
