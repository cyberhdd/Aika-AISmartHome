import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import joblib

# code used to import replyHelper
# from Helper import replyHelper #can be used if helper file under
# .. to go up one file level
# to import helper (required if file in different folders on the same level)
import sys
import os

# Append Helper directory path to system path
helper_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Helper"))
sys.path.append(helper_path)
# Import the module
import replyHelper


# Load tokenizer
with open("tokenizer_v1_2.json", "r") as f:
    tokenizer_data = json.load(f)
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)


# Load label encoders
intent_label_encoder = joblib.load("intent_label_encoder_v1_2.pkl")
action_label_encoder = joblib.load("action_label_encoder_v1_2.pkl")


# testing
# Print intent label mappings
intent_labels = intent_label_encoder.classes_
encoded_intent_labels = intent_label_encoder.transform(intent_labels)
print("Intent labels: ", intent_labels)
print("Encoded intent labels: ", encoded_intent_labels)

# Print action label mappings
action_labels = action_label_encoder.classes_
encoded_action_labels = action_label_encoder.transform(action_labels)
print("Action labels: ", action_labels)
print("Encoded action labels: ", encoded_action_labels)


# Load trained model
model = tf.keras.models.load_model("dnnmodel_v1_2.h5")

# Load encoded queries
encoded_queries = joblib.load("encoded_queries_v1_2.pkl")


while True:
    # Example input query
    # input_query = "Whats the plug status"
    input_query = input("Query: ")

    # Tokenize and pad the input query
    encoded_input_query = tokenizer.texts_to_sequences([input_query])
    print(encoded_input_query)
    max_sequence_length = max(len(seq) for seq in encoded_queries)
    padded_input_queries = pad_sequences(
        encoded_input_query, maxlen=max_sequence_length
    )

    # predict
    intent_probabilities, action_probabilities = model.predict(padded_input_queries)
    print(
        "intent_probabilities: ",
        intent_probabilities,
        "\naction_probabilities: ",
        action_probabilities,
    )

    # Decode the predictions
    """ intent_label = intent_label_encoder.inverse_transform([np.argmax(intent_probabilities)])
    action_label = action_label_encoder.inverse_transform([np.argmax(action_probabilities)]) """
    intent_labels = intent_label_encoder.inverse_transform(
        np.argmax(intent_probabilities, axis=1)
    )
    action_labels = action_label_encoder.inverse_transform(
        np.argmax(action_probabilities, axis=1)
    )

    # the predicted labels
    intent_label = intent_labels[0]
    action_label = action_labels[0]
    print("Intent: ", intent_label)
    print("Action: ", action_label)

    # Check if one of the probabilities are higher than 0.8
    if intent_probabilities[0].max() > 0.8 or action_probabilities[0].max() > 0.8:
        # Perform action when both probabilities are higher than 0.8
        print("Your probabilities are high enough")
        print(f"Your {intent_labels} probability is at {intent_probabilities[0].max()}")
        print(f"Your {action_labels} probability is at {action_probabilities[0].max()}")

        if intent_labels == "bedroom" and action_labels == "on":
            reply_data = replyHelper.get_reply(intent_label, action_label)
            if reply_data:
                print("Reply:", reply_data)
            else:
                print("No reply available for the given intent and action")
    else:
        # Perform another action
        print("Your probabilities are too low")
        print(f"Your {intent_labels} probability is at {intent_probabilities[0][0]}")
        print(f"Your {action_labels} probability is at {action_probabilities[0][0]}")

    """ print("Intent Probabilities: ", intent_probabilities)
    print("Action Probabilities: ", action_probabilities) """
    loopContinue = input("Would you like to continue (e to exit): ")
    if loopContinue == "e":
        break
    print("Continuing...\n")
