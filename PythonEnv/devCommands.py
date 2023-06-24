# import helpers
from Helper import colourHelper
import requests
import json

# import credentials
devices = json.load(open("config/devices.json"))
LIGHT_SONOFF_DEVICE_ID = devices["light_sonoff_bathroom_id"]

##################################################
################# Tuya ###########################
##################################################


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


def commandLightSwitch(switchMode):
    return {"commands": [{"code": "switch_led", "value": switchMode}]}


# plug on/off
def commandPlugSwitch(switchMode):
    return {"commands": [{"code": "switch_1", "value": switchMode}]}


def commandStatus(result):
    switch_led_value = None
    work_mode_value = None
    bright_value = None
    temp_value = None
    colour_led_value = None
    for item in result["result"]:
        if item["code"] == "switch_led":
            switch_led_value = item["value"]
            # print("Switch LED:", switch_led_value)
            continue
        if item["code"] == "bright_value_v2":
            bright_value = item["value"]
            continue
        if item["code"] == "temp_value_v2":
            temp_value = item["value"]
            continue
        if item["code"] == "work_mode":
            work_mode_value = item["value"]
            # print("Work Mode:", work_mode_value)
        # if colour mode
        if work_mode_value == "colour":
            if item["code"] == "colour_data_v2":
                colour_led_value = item["value"]
                colour = colourHelper.get_matching_colour(colour_led_value)
                if colour is not None:
                    colour_led_value = colour
                # print("LED Colour:", colour_led_value)
                break
    return switch_led_value, work_mode_value, bright_value, temp_value, colour_led_value
    """ # if white mode
    if work_mode_value == "white":
        print("Bright Value:", bright_value)
        print("Temp Value:", temp_value) """


def commandStatusPlug(result):
    switch_plug_value = None
    power_value = None
    current_value = None
    voltage_value = None
    for item in result["result"]:
        if item["code"] == "switch_1":
            switch_plug_value = item["value"]
            # print("Switch Plug:", switch_plug_value)
            continue
        if item["code"] == "cur_power":
            power_value = item["value"]
            power_value = float(power_value / 10)
            # print("Current power (W):", power_value)
            continue
        if item["code"] == "cur_current":
            current_value = item["value"]
            # print("Current current (mA):", current_value)
            continue
        if item["code"] == "cur_voltage":
            voltage_value = item["value"]
            voltage_value = float(voltage_value / 10)
            # print("Current voltage (V):", voltage_value)
            continue
    return switch_plug_value, power_value, current_value, voltage_value


def commandStatusPlugPower(result):
    power_value = None
    for item in result["result"]:
        if item["code"] == "cur_power":
            power_value = item["value"]
            return power_value


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


def commandBrightness(bright_value):
    print("1. Increase\n2. Decrease\n3. Set")
    selection = int(input("Enter your choice: "))

    if selection == 1:
        brightness = bright_value + 100
        # max brightness at 1000
        if brightness > 1000:
            brightness = 1000
            print("Brightness already at maximum.")
    elif selection == 2:
        brightness = bright_value - 100
        # min brightness at 10
        if brightness < 10:
            brightness = 10
            print("Brightness already at minimum.")
    elif selection == 3:
        brightness = int(input("Enter the brightness value (10-1000): "))
        if brightness > 1000 or brightness < 10:
            print("Invalid value. Please enter a valid brightness value.\n")
            return None
    else:
        return None

    return {"commands": [{"code": "bright_value_v2", "value": brightness}]}


def commandBrightnessIncrease(bright_value):
    brightness = bright_value + 100
    # max brightness at 1000
    if brightness > 1000:
        brightness = 1000
        print("Brightness already at maximum.")
    return {"commands": [{"code": "bright_value_v2", "value": brightness}]}


def commandBrightnessDecrease(bright_value):
    brightness = bright_value - 100
    # min brightness at 10
    if brightness < 10:
        brightness = 10
        print("Brightness already at minimum.")
    return {"commands": [{"code": "bright_value_v2", "value": brightness}]}


def commandBrightnessSet(bright_value):
    brightness = int(input("Enter the brightness value (10-1000): "))
    if brightness > 1000 or brightness < 10:
        print("Invalid value. Please enter a valid brightness value.\n")
        return None
    return {"commands": [{"code": "bright_value_v2", "value": brightness}]}


def commandTemp(temp_value):
    print("1. Increase\n2. Decrease\n3. Set")
    selection = int(input("Enter your choice: "))

    if selection == 1:
        temperature = temp_value + 100
        # max temperature at 1000
        if temperature > 1000:
            temperature = 1000
            print("Temperature already at maximum.")
    elif selection == 2:
        temperature = temp_value - 100
        # min temperature at 10
        if temperature < 10:
            temperature = 10
            print("Temperature already at minimum.")
    elif selection == 3:
        temperature = int(input("Enter the temperature value (10-1000): "))
        if temperature > 1000 or temperature < 10:
            print("Invalid value. Please enter a valid temperature value.\n")
            return None
    else:
        return None

    return {"commands": [{"code": "temp_value_v2", "value": temperature}]}


##################################################
################ Sonoff ##########################
##################################################


def commandSOFColorPayload():
    print(
        "Choose your color:\n1. White\n2. Yellow\n3. Red\n4. Green\n5. Blue\n6. Orange\n7. Purple\n"
    )
    selection = int(input("Color choice: "))
    if selection == 1:
        color = colourHelper.get_colour_rgb("white")

    elif selection == 2:
        color = colourHelper.get_colour_rgb("yellow")

    elif selection == 3:
        color = colourHelper.get_colour_rgb("red")

    elif selection == 4:
        color = colourHelper.get_colour_rgb("green")

    elif selection == 5:
        color = colourHelper.get_colour_rgb("blue")

    elif selection == 6:
        color = colourHelper.get_colour_rgb("orange")

    elif selection == 7:
        color = colourHelper.get_colour_rgb("purple")

    else:
        color = colourHelper.get_colour_rgb("purple")

    command = {
        "deviceid": LIGHT_SONOFF_DEVICE_ID,
        "data": {"ltype": "color", "color": color},
    }
    return command


def commandSOFColor():
    commandMode = "dimmable"
    payload = commandSOFColorPayload()
    return payload, commandMode


def commandSOFSwitchOff():
    commandMode = "switch"
    payload = {
        "deviceid": LIGHT_SONOFF_DEVICE_ID,
        "data": {"switch": "off"},
    }  # on/off switch
    return payload, commandMode


def commandSOFSwitchOn():
    commandMode = "switch"
    payload = {
        "deviceid": LIGHT_SONOFF_DEVICE_ID,
        "data": {"switch": "on"},
    }
    return payload, commandMode


def commandSOFSignal():
    commandMode = "signal_strength"
    payload = {"deviceid": LIGHT_SONOFF_DEVICE_ID, "data": {}}  # signal strength
    return payload, commandMode


def commandSOFStatus():
    commandMode = "info"
    payload = {"deviceid": LIGHT_SONOFF_DEVICE_ID, "data": {}}  # signal strength
    return payload, commandMode


def commandSOFStatusDetails(result):
    response_data = result.json()
    switch = response_data["data"]["switch"]
    ltype = response_data["data"]["ltype"]
    white = response_data["data"]["white"]
    color = response_data["data"]["color"]
    print("Switch LED:", switch)
    print("Work Mode:", ltype)
    """ print("White:", white)
    print("Color:", color) """

    # if colour mode
    if ltype == "color":
        colour = colourHelper.get_matching_rgb(color)
        if colour is not None:
            colour_led_value = colour
        print("LED Colour:", colour_led_value)
    # if white mode
    elif ltype == "white":
        print("Bright Value:", white["br"])
        print("Temp Value:", white["ct"])


def commandSOFBrightness(result):
    commandMode = "dimmable"
    response_data = result.json()
    white = response_data["data"]["white"]
    bright_value = white["br"]
    print("1. Increase\n2. Decrease\n3. Set")
    selection = int(input("Enter your choice: "))

    if selection == 1:
        brightness = bright_value + 10
        # max brightness at 1000
        if brightness > 100:
            brightness = 100
            print("Brightness already at maximum.")
    elif selection == 2:
        brightness = bright_value - 10
        # min brightness at 10
        if brightness < 1:
            brightness = 1
            print("Brightness already at minimum.")
    elif selection == 3:
        brightness = int(input("Enter the brightness value (1-100): "))
        if brightness > 100 or brightness < 1:
            print("Invalid value. Please enter a valid brightness value.\n")
            return None
    else:
        return None

    payload = {
        "deviceid": LIGHT_SONOFF_DEVICE_ID,
        "data": {"ltype": "white", "white": {"br": brightness, "ct": white["ct"]}},
    }
    return payload, commandMode


def commandSOFTemp(result):
    commandMode = "dimmable"
    response_data = result.json()
    white = response_data["data"]["white"]
    temp_value = white["ct"]
    print("1. Increase\n2. Decrease\n3. Set")
    selection = int(input("Enter your choice: "))

    if selection == 1:
        temperature = temp_value + 10
        # max brightness at 1000
        if temperature > 100:
            temperature = 100
            print("Temperature already at maximum.")
    elif selection == 2:
        temperature = temp_value - 10
        # min brightness at 10
        if temperature < 1:
            temperature = 1
            print("Temperature already at minimum.")
    elif selection == 3:
        temperature = int(input("Enter the temperature value (1-100): "))
        if temperature > 100 or temperature < 1:
            print("Invalid value. Please enter a valid temperature value.\n")
            return None
    else:
        return None

    payload = {
        "deviceid": LIGHT_SONOFF_DEVICE_ID,
        "data": {"ltype": "white", "white": {"br": white["br"], "ct": temperature}},
    }
    return payload, commandMode
