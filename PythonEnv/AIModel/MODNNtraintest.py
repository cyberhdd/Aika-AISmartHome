# AI model imports
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import joblib

# for plotting confusion matrix
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


####################################################################
######################## Train Model ###############################
####################################################################

# Load data from CSV
data = pd.read_csv(r"Dataset\datasetv1_2.csv")
queries = data["Sentence"].tolist()
intents = data["Category"].tolist()
actions = data["Action"].tolist()
unique_intents = data["Category"].unique()
unique_actions = data["Action"].unique()

# Save tokenizer for all queries # this one is used if all queries used to train
""" tokenizer = Tokenizer()
tokenizer.fit_on_texts(queries)
tokenizer_json = tokenizer.to_json()
with open("tokenizer_v1.json", "w") as f:
    json.dump(tokenizer_json, f) """


print(unique_intents)
print(unique_actions)

# One-hot encoding for intents and actions
intent_label_encoder = LabelEncoder()
action_label_encoder = LabelEncoder()
encoded_intents = intent_label_encoder.fit_transform(intents)
encoded_actions = action_label_encoder.fit_transform(actions)
# save the label_encoder
joblib.dump(intent_label_encoder, "intent_label_encoder_v1_2.pkl")
joblib.dump(action_label_encoder, "action_label_encoder_v1_2.pkl")

print(encoded_intents)
print(encoded_actions)


# split train and test set
# Split data into train and test sets
(
    train_queries,
    test_queries,
    train_intents,
    test_intents,
    train_actions,
    test_actions,
) = train_test_split(
    queries, encoded_intents, encoded_actions, test_size=0.2, random_state=42
)


# preprocess using tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(train_queries)
# tokenize and export for prediction
tokenizer_json = tokenizer.to_json()
with open("tokenizer_v1_2.json", "w") as f:
    json.dump(tokenizer_json, f)

print(tokenizer)  # testing
encoded_train_queries = tokenizer.texts_to_sequences(train_queries)
encoded_test_queries = tokenizer.texts_to_sequences(test_queries)
print(encoded_train_queries)  # testing
max_sequence_length = max(
    len(seq) for seq in encoded_train_queries + encoded_test_queries
)
padded_train_queries = pad_sequences(
    encoded_train_queries, maxlen=max_sequence_length
)  # padding as DNN require same size input
print(padded_train_queries)
padded_test_queries = pad_sequences(encoded_test_queries, maxlen=max_sequence_length)

# Save the encoded queries
encoded_queries = encoded_train_queries + encoded_test_queries
joblib.dump(encoded_queries, "encoded_queries_v1_2.pkl")

# Build Deep Neural Network Model
model = keras.Sequential()
model.add(  # embedding layer for the tokenization index
    keras.layers.Embedding(
        input_dim=len(tokenizer.word_index) + 1,
        output_dim=100,
        input_length=max_sequence_length,
    )
)
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64, activation="relu"))
model.add(keras.layers.Dense(32, activation="relu"))
# Model Output
# Intent Output - create a layer for intent output
intent_output = keras.layers.Dense(
    len(unique_intents), activation="softmax", name="intent_output"
)(model.layers[-1].output)
# Action Output - create a layer for action output
action_output = keras.layers.Dense(
    len(unique_actions), activation="softmax", name="action_output"
)(model.layers[-1].output)
# Combine Input and Output
model = keras.Model(inputs=model.inputs, outputs=[intent_output, action_output])


# Compile model
model.compile(
    optimizer="adam",
    loss={
        "intent_output": "categorical_crossentropy",
        "action_output": "categorical_crossentropy",
    },
    metrics={"intent_output": "accuracy", "action_output": "accuracy"},
)


# Convert encoded intents and actions into one-hot encoded format ([0 1 0])
onehot_train_intents = keras.utils.to_categorical(
    train_intents, num_classes=len(unique_intents)
)
onehot_test_intents = keras.utils.to_categorical(
    test_intents, num_classes=len(unique_intents)
)
onehot_train_actions = keras.utils.to_categorical(
    train_actions, num_classes=len(unique_actions)
)
onehot_test_actions = keras.utils.to_categorical(
    test_actions, num_classes=len(unique_actions)
)


print(onehot_train_intents)
print(onehot_train_actions)

# Train model -
model.fit(
    padded_train_queries,
    {"intent_output": onehot_train_intents, "action_output": onehot_train_actions},
    validation_data=(
        padded_test_queries,
        {"intent_output": onehot_test_intents, "action_output": onehot_test_actions},
    ),
    epochs=10,
)

# Save model
model.save("dnnmodel_v1_2.h5")


####################################################################
################## Model Confusion Matrix ##########################
####################################################################
# Get the predictions for the validation data
validation_predictions = model.predict(padded_test_queries)
intent_predictions = np.argmax(validation_predictions[0], axis=1)
action_predictions = np.argmax(validation_predictions[1], axis=1)
# Create confusion matrices
intent_confusion = confusion_matrix(test_intents, intent_predictions)
action_confusion = confusion_matrix(test_actions, action_predictions)
# Plot confusion matrices
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
sns.heatmap(intent_confusion, annot=True, cmap="Blues", fmt="d", cbar=False)
plt.xlabel("Predicted Intent")
plt.ylabel("True Intent")
plt.title("Intent Confusion Matrix")

plt.subplot(1, 2, 2)
sns.heatmap(action_confusion, annot=True, cmap="Blues", fmt="d", cbar=False)
plt.xlabel("Predicted Action")
plt.ylabel("True Action")
plt.title("Action Confusion Matrix")

plt.tight_layout()
plt.show()


####################################################################
###################### Test Query Model ############################
####################################################################
# Load Model
# test query
input_query = "What is the bathroom light status"
encoded_input_query = tokenizer.texts_to_sequences([input_query])  # tokenize
print(encoded_input_query)
padded_input_queries = pad_sequences(encoded_input_query, maxlen=max_sequence_length)
print(padded_input_queries)

# predict
intent_probabilities, action_probabilities = model.predict(padded_input_queries)
print(
    "intent_probabilities: ",
    intent_probabilities,
    "\naction_probabilities: ",
    action_probabilities,
)

# Decode the predictions
intent_label = intent_label_encoder.inverse_transform([np.argmax(intent_probabilities)])
action_label = action_label_encoder.inverse_transform([np.argmax(action_probabilities)])

print("Intent: ", intent_label)
print("Action: ", action_label)
print("Intent Probabilities: ", intent_probabilities)
print("Action Probabilities: ", action_probabilities)
print("Unique Actions: ", unique_actions)
print("Encoded actions: ", encoded_actions)

""" [light switch]
[none off on] """
# alphabetical order

# Load label encoders
intent_label_encoder = joblib.load("intent_label_encoder_v1_2.pkl")
action_label_encoder = joblib.load("action_label_encoder_v1_2.pkl")

# Print label encoders
print("Test Intent Label Encoder: ", intent_label_encoder)
print("Test Action Label Encoder: ", action_label_encoder)

# Print label encoder classes
intent_classes = intent_label_encoder.classes_
action_classes = action_label_encoder.classes_

print("Test Intent Label Encoder Classes: ", intent_classes)
print("Test Action Label Encoder Classes: ", action_classes)
