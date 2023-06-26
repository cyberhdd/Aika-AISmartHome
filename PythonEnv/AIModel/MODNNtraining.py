# AI model imports
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Load data from CSV
data = pd.read_csv(r"Dataset\testdatalightsw.csv")
queries = data["Sentence"].tolist()
intents = data["Category"].tolist()
actions = data["Action"].tolist()
unique_intents = data["Category"].unique()
unique_actions = data["Action"].unique()


print(unique_intents)
print(unique_actions)

# One-hot encoding for intents and actions
intent_label_encoder = LabelEncoder()
action_label_encoder = LabelEncoder()
encoded_intents = intent_label_encoder.fit_transform(intents)
encoded_actions = action_label_encoder.fit_transform(actions)

print(encoded_intents)
print(encoded_actions)


# preprocess using tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(queries)
print(tokenizer)  # testing
encoded_queries = tokenizer.texts_to_sequences(queries)
print(encoded_queries)  # testing
max_sequence_length = max(len(seq) for seq in encoded_queries)
padded_queries = pad_sequences(
    encoded_queries, maxlen=max_sequence_length
)  # padding as DNN require same size input
print(padded_queries)

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
onehot_intents = tf.keras.utils.to_categorical(
    encoded_intents, num_classes=len(unique_intents)
)
onehot_actions = tf.keras.utils.to_categorical(
    encoded_actions, num_classes=len(unique_actions)
)

print(onehot_intents)
print(onehot_actions)

# Train model -
model.fit(
    padded_queries,
    {"intent_output": onehot_intents, "action_output": onehot_actions},
    epochs=30,
)

# Save model
model.save("dnnmodel.h5")

#
#
#
# Load Model
# test query
input_query = "Its a bit too bright here"
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
