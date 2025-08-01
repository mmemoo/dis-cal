import json
from scripts.check_state import check_and_update_state

def add_cal_to_state(cals):
    check_and_update_state()
    
    with open("state.json","r") as f:
        state_json = json.load(f)

    state_json["total_cals"] += cals

    with open("state.json","w") as f:
        json.dump(state_json,f)