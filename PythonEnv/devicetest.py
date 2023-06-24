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
PLUG_DEVICE_ID = devices["plug_power"]

openapi = TuyaOpenAPI(ENDPOINT, ACCESS_ID, ACCESS_KEY)
connection = openapi.connect(USERNAME, PASSWORD, "60", "smartlife")
print(connection)

lightStat = None
work_mode_value = None  # to consider what status to print


while True:
    print(
        "What would you like to do:\n1. Status\n2. Light\n3. Color\n4. Brightness\n5. Temperature\n6. Plug Status\n7. Power Consumption\n8. Plug On\n9. Plug Off"
    )

    # try except block
    try:
        selection = int(input("Enter your choice: "))

        if selection == 1:
            commands = None  # get status not a command
            result = openapi.get(f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/status")
            if result["success"]:
                devCommands.commandStatus(result)

        elif selection == 2:
            print("Would you like to turn the light on (1) or off (2)")
            lightStat = int(input("Enter your choice: "))
            # check choice
            commands = devCommands.commandChoice(lightStat)
            print(commands)

        elif selection == 3:
            # check choice
            commands = devCommands.colorChoice()
            print(commands)

        elif selection == 4:
            # get current brightness
            result = openapi.get(f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/status")

            if result["success"]:
                for item in result["result"]:
                    if item["code"] == "bright_value_v2":
                        bright_value = item["value"]
                        break
            # get brightness command
            commands = devCommands.commandBrightness(bright_value)
            print(commands)

        elif selection == 5:
            # get current temperature
            result = openapi.get(f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/status")

            if result["success"]:
                for item in result["result"]:
                    if item["code"] == "temp_value_v2":
                        temp_value = item["value"]
                        break
            # get temp command
            commands = devCommands.commandTemp(temp_value)
            print(commands)

        elif selection == 6:
            commands = None  # get status not a command
            result = openapi.get(f"/v1.0/iot-03/devices/{PLUG_DEVICE_ID}/status")
            if result["success"]:
                devCommands.commandStatusPlug(result)

        elif selection == 7:
            commands = None  # get status not a command
            result = openapi.get(f"/v1.0/iot-03/devices/{PLUG_DEVICE_ID}/status")
            if result["success"]:
                power_value = devCommands.commandStatusPlugPower(result)
                print("Current power (W):", float(power_value / 10))

        elif selection == 8:
            switchMode = True
            commands = devCommands.commandPlugSwitch(switchMode)
            result = openapi.post(
                f"/v1.0/iot-03/devices/{PLUG_DEVICE_ID}/commands", commands
            )
            print(commands)
            commands = None  # Dont continue executing

        elif selection == 9:
            switchMode = False
            commands = devCommands.commandPlugSwitch(switchMode)
            result = openapi.post(
                f"/v1.0/iot-03/devices/{PLUG_DEVICE_ID}/commands", commands
            )
            print(commands)
            commands = None  # Dont continue executing

        else:
            print("Invalid command. Try again.\n")

        # post if there is a command
        if commands is not None:
            result = openapi.post(
                f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/commands", commands
            )
            print(result)

    except Exception:
        print("An error occurred. Please try again.\n")

    loopContinue = input("Would you like to continue (y to continue): ")
    if loopContinue != "y":
        break
    print("Continuing...\n")


""" commands = {"commands": [{"code": "switch_led", "value": True}]}
result = openapi.post(f"/v1.0/iot-03/devices/{LIGHT_DEVICE_ID}/commands", commands)
print(result) """
