import difflib


room_options = ["bathroom", "bedroom"]


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
