import json

def check_setup_state():
    with open("setup_state.json") as f:
        setup_state_json = json.load(f)

    return setup_state_json["chromadb"] and setup_state_json["usda_data"]