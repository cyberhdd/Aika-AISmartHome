# condition
# is checks for reference equality (identity), == checks for value equality
def commandChoice(lightStat):
    if lightStat == 1:
        return {"commands": [{"code": "switch_led", "value": True}]}
    elif lightStat == 2:
        return {"commands": [{"code": "switch_led", "value": False}]}
    else:
        print("No such input. Try again.")
        return None
