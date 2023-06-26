import json
import random

# Load the replies from the JSON file
with open("PythonEnv/Helper/replyData.json", "r") as f:
    replies_data = json.load(f)


def get_reply(intent_label, action_label):
    # print(replies_data)
    print(replies_data.keys())
    print(replies_data["bedroom"].keys())
    if intent_label in replies_data and action_label in replies_data[intent_label]:
        seq = replies_data[intent_label][action_label]
        if seq:
            reply = random.choice(seq)
        else:
            return "No reply found for the given intent and action."
    else:
        return "Invalid intent or action label."

    return reply
