import requests
import json

# self command case
import devCommands

credentials = json.load(open("config/credentials.json"))
devices = json.load(open("config/devices.json"))
SONOFF_IP_ADDRESS = credentials["sonoff_ip"]
SONOFF_PORT = credentials["sonoff_port"]
LIGHT_SONOFF_DEVICE_ID = devices["light_sonoff_bathroom_id"]


payload = None
commandMode = None


def postRequest(payload, commandMode):
    url = f"http://{SONOFF_IP_ADDRESS}:{SONOFF_PORT}/zeroconf/{commandMode}"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response)
    return response


while True:
    print(
        "What would you like to do:\n1. Status\n2. Light\n3. Color\n4. Brightness\n5. Temperature\n6. Signal Strength"
    )

    # try except block
    try:
        selection = int(input("Enter your choice: "))

        if selection == 1:
            payload, commandMode = devCommands.commandSOFStatus()
            response = postRequest(payload, commandMode)
            if response.status_code == 200:
                (
                    switch,
                    ltype,
                    color,
                    brightness,
                    temperature,
                ) = devCommands.commandSOFStatusDetails(response)
                print("Switch LED:", switch)
                print("Work Mode:", ltype)
                # print value depending on work mode
                if ltype == "color":
                    print("LED Color:", color)
                elif ltype == "white":
                    print("Bright Value:", brightness)
                    print("Temp Value:", temperature)
            else:
                print("Request failed with status code: ", response.status_code)
            payload = None  # not sending commands afterwards

        elif selection == 2:
            print("Would you like to turn the light on (1) or off (2)")
            lightStat = int(input("Enter your choice: "))
            if lightStat == 1:
                print("switching on")
                payload, commandMode = devCommands.commandSOFSwitchOn()

            elif lightStat == 2:
                payload, commandMode = devCommands.commandSOFSwitchOff()
            else:
                print("Invalid option. Please try again.\n")

        elif selection == 3:
            print(
                "Choose your color:\n1. White\n2. Yellow\n3. Red\n4. Green\n5. Blue\n6. Orange\n7. Purple\n"
            )
            # type out the color name
            selection = input("Color choice: ").lower()

            payload, commandMode = devCommands.commandSOFColor(selection)

        elif selection == 4:
            payload, commandMode = devCommands.commandSOFStatus()
            response = postRequest(payload, commandMode)
            if response.status_code == 200:
                print("1. Increase\n2. Decrease\n3. Set")
                selection = int(input("Enter your choice: "))
                # pass selection to method
                if selection == 1 or selection == 2 or selection == 3:
                    payload, commandMode = devCommands.commandSOFBrightness(
                        response, selection
                    )
                else:
                    payload = None
            else:
                print("Request failed with status code: ", response.status_code)

        elif selection == 5:
            payload, commandMode = devCommands.commandSOFStatus()
            response = postRequest(payload, commandMode)
            if response.status_code == 200:
                print("1. Increase\n2. Decrease\n3. Set")
                selection = int(input("Enter your choice: "))
                if selection == 1 or selection == 2 or selection == 3:
                    payload, commandMode = devCommands.commandSOFTemp(
                        response, selection
                    )
                else:
                    payload = None
            else:
                print("Request failed with status code: ", response.status_code)

        elif selection == 6:
            payload, commandMode = devCommands.commandSOFSignal()

        else:
            print("Invalid command. Try again.\n")

        # print(payload)
        # print(commandMode)
        # post if there is a command
        if payload is not None:
            response = postRequest(payload, commandMode)
            if response.status_code == 200:
                response_data = response.json()
                # signal_strength = response_data["data"]["signalStrength"]
                print("Response data:", response_data)
            else:
                print("Request failed with status code: ", response.status_code)

    except Exception:
        print("An error occurred. Please try again.\n")

    loopContinue = input("Would you like to continue (y to continue): ")
    if loopContinue != "y":
        break
    print("Continuing...\n")
