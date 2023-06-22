# import helpers
from Helper import colourHelper


# condition
# "is" checks for reference equality (identity), "==" checks for value equality
def commandChoice(lightStat):
    if lightStat == 1:
        return {"commands": [{"code": "switch_led", "value": True}]}
    elif lightStat == 2:
        return {"commands": [{"code": "switch_led", "value": False}]}
    else:
        print("No such input. Try again.")
        return None


def checkStatus():
    return None


def colorChoice():
    print(
        "Choose your color:\n1. White\n2. Yellow\n3. Red\n4. Green\n5. Blue\n6. Orange\n7. Purple\n"
    )
    selection = int(input("Color choice: "))
    if selection == 1:
        command = colourHelper.get_colour_command("white")

    elif selection == 2:
        command = colourHelper.get_colour_command("yellow")

    elif selection == 3:
        command = colourHelper.get_colour_command("red")

    elif selection == 4:
        command = colourHelper.get_colour_command("green")

    elif selection == 5:
        command = colourHelper.get_colour_command("blue")

    elif selection == 6:
        command = colourHelper.get_colour_command("orange")

    elif selection == 7:
        command = colourHelper.get_colour_command("purple")

    else:
        return {
            "commands": [
                {"code": "work_mode", "value": "colour"},
                {"code": "temp_value_v2", "value": 700},
                {"code": "bright_value_v2", "value": 800},
                {"code": "colour_data_v2", "value": {"h": 50, "s": 1000, "v": 900}},
            ]
        }

    return command


def colorTemp():
    return {
        "commands": [
            {"code": "colour_data_v2", "value": {"h": 200, "s": 100, "v": 100}}
        ]
    }
