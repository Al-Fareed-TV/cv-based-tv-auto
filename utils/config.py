import json

file_path = "prompts/sys_prompt.json"
def load_json():
    with open(file_path, 'r') as f:
        return json.load(f)
