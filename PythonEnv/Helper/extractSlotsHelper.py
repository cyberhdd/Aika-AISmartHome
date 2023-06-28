import difflib
from Helper import colourHelper

room_options = ["bathroom", "bedroom"]
room_options_all = ["bathroom", "bedroom", "both"]
color_options = list(colourHelper.colours.keys())


# to extract location from query
def extract_slots(query):
    words = query.lower().split()
    # iterate through each word
    for word in words:
        for room in room_options:
            # If the word is 70% similar to the room option
            if difflib.SequenceMatcher(None, word, room).ratio() >= 0.7:
                # Slot found with high similarity score, return the room
                return room
    return None


# to extract color from query
def extract_color_slots(query):
    words = query.lower().split()
    # iterate through each word
    for word in words:
        for color in color_options:
            # If the word is 70% similar to the color option
            if difflib.SequenceMatcher(None, word, color).ratio() >= 0.7:
                # Slot found with high similarity score, return the color
                return color
    return None


# to get location from user input (may be a sentence)
def get_slots(location):
    words = location.lower().split()
    for word in words:
        matches = difflib.get_close_matches(word, room_options, n=1, cutoff=0.7)
        if matches:
            location = matches[0]
            print(location)
            return location
    return None


# to get all location from user input (may be a sentence)
def get_all_location_slots(location):
    words = location.lower().split()
    for word in words:
        matches = difflib.get_close_matches(word, room_options_all, n=1, cutoff=0.7)
        if matches:
            location = matches[0]
            print(location)
            return location
    return None


# to get color from user input (may be a sentence)
def get_color_slots(color):
    words = color.lower().split()
    for word in words:
        matches = difflib.get_close_matches(word, color_options, n=1, cutoff=0.7)
        if matches:
            color = matches[0]
            print(color)
            return color
    return None
