from actions.navigator import NavigationNotFound,Navigator
from controller.tv_controller import SamsungRemote

NAV_MAP_PATH = "config/navigation_map.yaml"


def test_valid_navigation():
    remote = SamsungRemote();
    remote.connect();
    navigator = Navigator(NAV_MAP_PATH,remote)

    keys = navigator.goto("For You", "Search",0.5)
    print(keys)


# def test_invalid_current_focus():
#     navigator = Navigator(NAV_MAP_PATH)

#     try:
#         navigator.goto("Unknown Focus", "Search")
#     except NavigationNotFound as e:
#         print("✅ test_invalid_current_focus passed")
#         print(f"   Error: {e}")
#     else:
#         raise AssertionError("Expected NavigationNotFound not raised")


# def test_invalid_destination():
#     navigator = Navigator(NAV_MAP_PATH)

#     try:
#         navigator.goto("For You", "NonExistingDestination")
#     except NavigationNotFound as e:
#         print("✅ test_invalid_destination passed")
#         print(f"   Error: {e}")
#     else:
#         raise AssertionError("Expected NavigationNotFound not raised")


if __name__ == "__main__":
    test_valid_navigation()
