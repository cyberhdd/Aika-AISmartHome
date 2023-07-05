import requests
import json

# self command case
from Helper import devCommands

credentials = json.load(open("config/credentials.json"))
devices = json.load(open("config/devices.json"))
SONOFF_IP_ADDRESS = credentials["sonoff_ip"]
SONOFF_PORT = credentials["sonoff_port"]
LIGHT_SONOFF_DEVICE_ID = devices["light_sonoff_bathroom_id"]


payload = None
commandMode = None


def postRequest(payload, commandMode):
    try:
        url = f"http://{SONOFF_IP_ADDRESS}:{SONOFF_PORT}/zeroconf/{commandMode}"
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print(response)
        return response
    except Exception:
        print("An error occurred. Please try again.\n")
        return None


def sofBrightnessSet(bright_var):
    try:
        payload, commandMode = devCommands.commandSOFStatus()
        response = postRequest(payload, commandMode)
        if response.status_code == 200:
            payload, commandMode = devCommands.commandSOFBrightnessSet(
                response, bright_var
            )
        else:
            print("Request failed with status code: ", response.status_code)

        if payload is not None:
            response = postRequest(payload, commandMode)
            if response.status_code == 200:
                response_data = response.json()
                print("Response data:", response_data)
                return response_data
            else:
                print("Request failed with status code: ", response.status_code)
    except Exception:
        print("An error occurred. Please try again.\n")
        return None


def sofColorSet(color):
    try:
        payload, commandMode = devCommands.commandSOFColor(color)
        if payload is not None:
            response = postRequest(payload, commandMode)
            if response.status_code == 200:
                response_data = response.json()
                print("Response data:", response_data)
                return response_data
            else:
                print("Request failed with status code: ", response.status_code)
                return None
    except Exception:
        print("An error occurred. Please try again.\n")
        return None


def sofBrightnessIncrease(bright_var):
    payload, commandMode = devCommands.commandSOFStatus()
    response = postRequest(payload, commandMode)
    if response.status_code == 200:
        payload, commandMode = devCommands.commandSOFBrightnessSet(response, bright_var)
    else:
        print("Request failed with status code: ", response.status_code)

    if payload is not None:
        response = postRequest(payload, commandMode)
        if response.status_code == 200:
            response_data = response.json()
            print("Response data:", response_data)
        else:
            print("Request failed with status code: ", response.status_code)


def sofCommands(selection):
    """print(
        "What would you like to do:\n1. Status\n2. Light\n3. Color\n4. Brightness\n5. Temperature\n6. Signal Strength"
    )
    """
    # try except block
    try:
        if selection == "bathroom light status":
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

                return (
                    switch,
                    ltype,
                    color,
                    brightness,
                    temperature,
                )
            else:
                print("Request failed with status code: ", response.status_code)

            return None

        elif selection == "bathroom light on" or selection == "bathroom light off":
            if selection == "bathroom light on":
                print("switching on")
                payload, commandMode = devCommands.commandSOFSwitchOn()

            elif selection == "bathroom light off":
                payload, commandMode = devCommands.commandSOFSwitchOff()
            else:
                print("Invalid option. Please try again.\n")

        elif selection == "bathroom light color":
            print(
                "Choose your color:\n1. White\n2. Yellow\n3. Red\n4. Green\n5. Blue\n6. Orange\n7. Purple\n"
            )
            # type out the color name
            selection = input("Color choice: ").lower()
            payload, commandMode = devCommands.commandSOFColor(selection)

        elif selection == "bathroom light brightness":
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

        elif selection == "bathroom light temp":
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
        return None

    return
