from dotenv import load_dotenv
import websocket
import ssl
import json
import base64
import os
import threading
import time

load_dotenv()

TV_IP = os.getenv("TV_IP")
TV_PORT = int(os.getenv("TV_PORT"))
APP_NAME = "PythonRemote"
TOKEN_FILE = os.getenv("TOKEN_FILE")


class SamsungRemote:
    def __init__(self):
        self.token = self._load_token()
        self.ws = None
        self.authorized = threading.Event()  # ✅ NEW

    def _load_token(self):
        if os.path.exists(TOKEN_FILE):
            return open(TOKEN_FILE).read().strip()
        return ""

    def _save_token(self, token):
        with open(TOKEN_FILE, "w") as f:
            f.write(token)

    def connect(self):
        encoded_name = base64.b64encode(APP_NAME.encode()).decode()

        ws_url = (
            f"wss://{TV_IP}:{TV_PORT}/api/v2/channels/samsung.remote.control"
            f"?name={encoded_name}"
        )

        if self.token:
            ws_url += f"&token={self.token}"

        self.ws = websocket.WebSocketApp(
            ws_url,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error
        )

        thread = threading.Thread(
            target=self.ws.run_forever,
            kwargs={"sslopt": {"cert_reqs": ssl.CERT_NONE}},
            daemon=True
        )
        thread.start()

        print("⏳ Waiting for TV authorization...")
        if not self.authorized.wait(timeout=10):
            raise RuntimeError("TV authorization timeout")

        print("✅ TV authorized")

    def _on_open(self, ws):
        print("🔌 WebSocket connected")

    def _on_message(self, ws, message):
        msg = json.loads(message)
        print("📩 TV:", msg)

        if msg.get("data", {}).get("token"):
            self.token = msg["data"]["token"]
            self._save_token(self.token)
            print("🔐 Token saved")

        if msg.get("event") == "ms.channel.connect":
            self.authorized.set()  # ✅ AUTH CONFIRMED

    def _on_error(self, ws, error):
        print("❌ WebSocket error:", error)

    def send_key(self, key):
        if not self.authorized.is_set():
            print(f"⚠️ Ignoring key {key} — not authorized yet")
            return

        payload = {
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        }

        self.ws.send(json.dumps(payload))
        print("➡️ Sent:", key)
        time.sleep(0.3)

    def execute_actions(self, actions, delay=0.4):
        for key in actions:
            self.send_key(key)
            time.sleep(delay)
