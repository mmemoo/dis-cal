import json
from datetime import datetime

def check_and_update_state():
    with open("state.json","r") as f:
        state_json = json.load(f)

    current_date = datetime.now().strftime(format="%d-%m-%Y")
    state_date = state_json["date"]

    if current_date != state_date:
        state_json["total_cals"] = 0
        state_json["date"] = current_date

    with open("state.json","w") as f:
        json.dump(state_json,f)

    return state_json["total_cals"],state_json["date"]