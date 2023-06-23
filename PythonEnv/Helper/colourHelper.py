import json

# Define the colour dictionary
colours = {
    "white": {
        "name": "White",
        "hsv": {"h": 0, "s": 0, "v": 1000},
        "rgb": {"br": 100, "r": 255, "g": 255, "b": 255},
    },
    "yellow": {
        "name": "Yellow",
        "hsv": {"h": 60, "s": 1000, "v": 1000},
        "rgb": {"br": 100, "r": 255, "g": 255, "b": 0},
    },
    "red": {
        "name": "Red",
        "hsv": {"h": 0, "s": 1000, "v": 1000},
        "rgb": {"br": 100, "r": 255, "g": 0, "b": 0},
    },
    "green": {
        "name": "Green",
        "hsv": {"h": 120, "s": 1000, "v": 1000},
        "rgb": {"br": 100, "r": 0, "g": 255, "b": 0},
    },
    "blue": {
        "name": "Blue",
        "hsv": {"h": 240, "s": 1000, "v": 1000},
        "rgb": {"br": 100, "r": 0, "g": 0, "b": 255},
    },
    "orange": {
        "name": "Orange",
        "hsv": {"h": 30, "s": 1000, "v": 1000},
        "rgb": {"br": 100, "r": 255, "g": 165, "b": 0},
    },
    "purple": {
        "name": "Purple",
        "hsv": {"h": 270, "s": 1000, "v": 1000},
        "rgb": {"br": 100, "r": 128, "g": 0, "b": 128},
    },
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


def get_colour_rgb(selection):
    if selection in colours:
        return colours[selection]["rgb"]
    return None  # Return None for invalid colour selections


def get_matching_rgb(colour_led_value):
    for colour_name, colour_data in colours.items():
        rgb_data = colour_data["rgb"]
        if (
            rgb_data["r"] == colour_led_value["r"]
            and rgb_data["g"] == colour_led_value["g"]
            and rgb_data["b"] == colour_led_value["b"]
        ):
            return colour_name
    return None
