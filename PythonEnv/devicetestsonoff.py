import requests
import json


credentials = json.load(open("config/credentials.json"))
devices = json.load(open("config/devices.json"))
SONOFF_IP_ADDRESS = credentials["sonoff_ip"]
SONOFF_PORT = credentials["sonoff_port"]
LIGHT_SONOFF_DEVICE_ID = devices["light_sonoff_bathroom_id"]


commandSwitch = {
    "deviceid": LIGHT_SONOFF_DEVICE_ID,
    "data": {"switch": "off"},
}  # on/off switch
commandSignal = {"deviceid": LIGHT_SONOFF_DEVICE_ID, "data": {}}  # signal strength

commandModeSwitch = "switch"
commandModeSignal = "signal_strength"

payload = commandSwitch
url = f"http://{SONOFF_IP_ADDRESS}:{SONOFF_PORT}/zeroconf/{commandModeSwitch}"

headers = {"Content-Type": "application/json"}
response = requests.post(url, headers=headers, data=json.dumps(payload))
print(response)
if response.status_code == 200:
    response_data = response.json()
    # signal_strength = response_data["data"]["signalStrength"]
    print("Signal Strength:", response_data)
else:
    print("Request failed with status code: ", response.status_code)
