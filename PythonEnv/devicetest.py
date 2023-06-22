from tuya_iot import TuyaOpenAPI
from requests import get
from Helper import colourHelper
import json

# self command case
import devCommands

credentials = json.load(open("config/credentials.json"))
devices = json.load(open("config/devices.json"))
ACCESS_ID = credentials["tuya_access_id"]
ACCESS_KEY = credentials["tuya_access_secret"]

# endpoint for api (region: Western America Data Center	)
# https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4
ENDPOINT = "https://openapi.tuyaus.com"

USERNAME = credentials["tuya_username"]
PASSWORD = credentials["tuya_password"]

LIGHT_DEVICE_ID = devices["light_bedroom_id"]

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
connection = openapi.connect(USERNAME, PASSWORD, "60", "smartlife")
print(connection)

loopCont = True
lightStat = 1
work_mode_value = None  # to consider what status to print


while loopCont:
    print("What would you like to do:\n1. Status\n2. Light\n3. Color")

    selection = int(input("Enter your choice: "))

    if selection == 1:
        result = openapi.get(f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/status")

        if result["success"]:
            for item in result["result"]:
                if item["code"] == "switch_led":
                    switch_led_value = item["value"]
                    print("Switch LED:", switch_led_value)
                    continue
                if item["code"] == "work_mode":
                    work_mode_value = item["value"]
                    print("Work Mode:", work_mode_value)
                    continue
                # if colour mode
                if work_mode_value == "colour":
                    if item["code"] == "colour_data_v2":
                        colour_led_value = item["value"]
                        colour = colourHelper.get_matching_colour(colour_led_value)
                        if colour is not None:
                            colour_led_value = colour
                        print("LED Colour:", colour_led_value)

    elif selection == 2:
        print("Would you like to turn the light on (1) or off (2)")
        lightStat = int(input("Enter your choice: "))
        # print({type(lightStat)})

        # check choice
        commands = devCommands.commandChoice(lightStat)
        print(commands)

        if commands is not None:
            result = openapi.post(
                f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/commands", commands
            )
            print(result)

    elif selection == 3:
        # check choice
        commands = devCommands.colorChoice()
        print(commands)

        if commands is not None:
            result = openapi.post(
                f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/commands", commands
            )
            print(result)

    loopContinue = input("Would you like to continue (y to continue): ")
    if loopContinue == "y":
        print("Continuing...\n")
    else:
        break


""" commands = {"commands": [{"code": "switch_led", "value": True}]}
result = openapi.post(f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/commands", commands)
print(result) """
