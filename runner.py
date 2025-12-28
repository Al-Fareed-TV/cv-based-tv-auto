from controller.tv_controller import TVController

RTSP_URL = "rtsp://192.168.1.99:1945/"

FLOW_PROMPT = """
Navigate from Home screen to Apps tab and open it.
"""

controller = TVController(
    camera_source=RTSP_URL,
    flow_prompt=FLOW_PROMPT
)

controller.start()
