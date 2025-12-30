from actions.navigator import NavigationNotFound,Navigator


NAV_MAP_PATH = "config/navigation_map.yaml"


def test_valid_navigation():
    navigator = Navigator(NAV_MAP_PATH)

    keys = navigator.goto("For You", "Search")

    assert keys == ["KEY_LEFT", "KEY_UP", "KEY_ENTER"]
    print("✅ test_valid_navigation passed")


def test_invalid_current_focus():
    navigator = Navigator(NAV_MAP_PATH)

    try:
        navigator.goto("Unknown Focus", "Search")
    except NavigationNotFound as e:
        print("✅ test_invalid_current_focus passed")
        print(f"   Error: {e}")
    else:
        raise AssertionError("Expected NavigationNotFound not raised")


def test_invalid_destination():
    navigator = Navigator(NAV_MAP_PATH)

    try:
        navigator.goto("For You", "NonExistingDestination")
    except NavigationNotFound as e:
        print("✅ test_invalid_destination passed")
        print(f"   Error: {e}")
    else:
        raise AssertionError("Expected NavigationNotFound not raised")


if __name__ == "__main__":
    print("🚀 Running Navigator tests...\n")

    test_valid_navigation()
    test_invalid_current_focus()
    test_invalid_destination()

    print("\n🎉 All Navigator tests passed")
