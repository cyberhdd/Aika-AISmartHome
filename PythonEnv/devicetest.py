from tuya_iot import TuyaOpenAPI
from requests import get
import json

# self command case
from devCommands import commandChoice

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

while loopCont:
    print("Would you like to turn the light on (1) or off (2)")
    lightStat = int(input("Enter your choice: "))
    # print({type(lightStat)})

    # check choice
    commands = commandChoice(lightStat)
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
