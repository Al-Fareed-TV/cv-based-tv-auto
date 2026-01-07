class KeyboardLayout:
    KEYS = {
        "a": (0, 0),
        "b": (0, 1),
        "c": (0, 2),
        "d": (0, 3),
        "e": (0, 4),
        "f": (0, 5),
        "g": (0, 6),
        "clear": (0, 7),
        "h": (1, 0),
        "i": (1, 1),
        "j": (1, 2),
        "k": (1, 3),
        "l": (1, 4),
        "m": (1, 5),
        "n": (1, 6),
        "sym": (1, 7),
        "o": (2, 0),
        "p": (2, 1),
        "q": (2, 2),
        "r": (2, 3),
        "s": (2, 4),
        "t": (2, 5),
        "u": (2, 6),
        "v": (3, 0),
        "w": (3, 1),
        "x": (3, 2),
        "y": (3, 3),
        "z": (3, 4),
        ",": (3, 5),
        ".": (3, 6),
        "caps": (3, 7),
        "key_settings": (4, 0),
        "key_space": (4, 2),
        "key_search": (4, 4),
        "key_left": (4, 6),
        "key_right": (4, 7),
    }


class KeyboardNavigator:
    def __init__(self, start_char="a"):
        start_char = start_char.lower()
        if start_char not in KeyboardLayout.KEYS:
            raise ValueError(f"Invalid start character: {start_char}")

        self.row, self.col = KeyboardLayout.KEYS[start_char]

    def move_to(self, key):
        key = key.lower()
        if key not in KeyboardLayout.KEYS:
            raise ValueError(f"Key not found on keyboard: {key}")

        target_row, target_col = KeyboardLayout.KEYS[key]
        actions = []

        # Vertical moves
        while self.row < target_row:
            actions.append("KEY_DOWN")
            self.row += 1
        while self.row > target_row:
            actions.append("KEY_UP")
            self.row -= 1

        # Horizontal moves
        while self.col < target_col:
            actions.append("KEY_RIGHT")
            self.col += 1
        while self.col > target_col:
            actions.append("KEY_LEFT")
            self.col -= 1

        actions.append("KEY_ENTER")
        return actions


def generate_actions_for_input(text, start_char="a"):
    navigator = KeyboardNavigator(start_char)
    actions = []

    if isinstance(text, str) and text.startswith("key_"):
        actions.extend(navigator.move_to(text))
        return actions

    for ch in text:
        actions.extend(navigator.move_to(ch))

    return actions
