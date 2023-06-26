import json

# Path to user input data file
json_file_path = "PythonEnv/Helper/userInputData.json"


def append_data(query, action):
    # Read the existing JSON file, have to load and rewrite to keep copy
    try:
        with open(json_file_path, "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {}

    # Add the new entry to the existing dictionary
    existing_data[query] = action

    # Write the updated data back to the JSON file
    with open(json_file_path, "w") as f:
        json.dump(existing_data, f, indent=4)
