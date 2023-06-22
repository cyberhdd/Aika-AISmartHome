import json

# Define the colour dictionary
colours = {
    "white": {"name": "White", "hsv": {"h": 0, "s": 0, "v": 1000}},
    "yellow": {"name": "Yellow", "hsv": {"h": 60, "s": 1000, "v": 1000}},
    "red": {"name": "Red", "hsv": {"h": 0, "s": 1000, "v": 1000}},
    "green": {"name": "Green", "hsv": {"h": 120, "s": 1000, "v": 1000}},
    "blue": {"name": "Blue", "hsv": {"h": 240, "s": 1000, "v": 1000}},
    "orange": {"name": "Orange", "hsv": {"h": 30, "s": 1000, "v": 1000}},
    "purple": {"name": "Purple", "hsv": {"h": 270, "s": 1000, "v": 1000}},
}


def get_colour_command(selection):
    if selection in colours:
        return {
            "commands": [
                {"code": "colour_data_v2", "value": colours[selection]["hsv"]}
            ],
        }

    return None  # Return None for invalid colour selections


# to get colour name from status hsv
def get_matching_colour(colour_led_value):
    # convert to dict
    colour_led_dict = json.loads(colour_led_value)
    h_value = colour_led_dict["h"]
    for colour_name, colour_data in colours.items():
        hsv_data = colour_data["hsv"]
        if hsv_data["h"] == h_value:
            return colour_name
    return None
