# discord imports
import discord
from discord.ext import commands
from discord.ext import tasks  # for task implementation
from itertools import cycle  # for task to change between status
import json

# AI model imports
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


#########################################################################
########################### Credential Section #########################
#########################################################################
credentials = json.load(open("config/credentials.json"))
BOT_TOKEN = credentials["bot_token"]
# print(BOT_TOKEN)
channelID = json.load(open("config/channel.json"))


#########################################################################
########################### Discord Bot Section #########################
#########################################################################


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")


# intents = discord.Intents.default()
# intents.message_content = True
intents = discord.Intents.all()
intents.message_content = True
channel_list = [
    channelID["channel1"],
    channelID["channel2"],
    channelID["channel3"],
    channelID["channel4"],
]

client = commands.Bot(command_prefix="", intents=intents)
# list of bot status
status = cycle(["Learning Humanity", "Learning You", "Compiling Humanity", "Humanity"])


# when bot ready###################################################
@client.event
async def on_ready():
    print("Bot is ready")

    # bot status
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game("Learning Humanity...")
    )
    change_status.start()


# task implementation###############################################
@tasks.loop(seconds=100)
async def change_status():  # loop change status
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_message(message):
    if message.author.bot:  # if bot sender, stop
        return
    elif message.channel.id not in channel_list:  # if not in correct channel
        return
    else:
        sentence = message.content
        encoded_sentence = tokenizer.texts_to_sequences([sentence])  # tokenize
        padded_sentence = pad_sequences(encoded_sentence, maxlen=max_sequence_length)
        print(sentence)  # print in console
        # predict
        sentence_intent_probabilities, sentence_action_probabilities = model.predict(
            padded_sentence
        )
        print(
            "intent_probabilities: ",
            sentence_intent_probabilities,
            "\naction_probabilities: ",
            sentence_action_probabilities,
        )

        # Decode the predictions
        intent_label = intent_label_encoder.inverse_transform(
            [np.argmax(sentence_intent_probabilities)]
        )
        action_label = action_label_encoder.inverse_transform(
            [np.argmax(sentence_action_probabilities)]
        )
        print("Intent: ", intent_label)
        print("Action: ", action_label)

        send_message = "Intent: " + str(intent_label) + "\nAction: " + str(action_label)
        print(send_message)

        await message.channel.send(send_message)  # print in discord from bot


#########################################################################
########################### AI Training Section #########################
#########################################################################

# Load data from CSV
data = pd.read_csv(r"Dataset\testdatalightsw.csv")
queries = data["Sentence"].tolist()
intents = data["Category"].tolist()
actions = data["Action"].tolist()
unique_intents = data["Category"].unique()
unique_actions = data["Action"].unique()

print(unique_intents)
print(unique_actions)
# print(queries)
# print(intents)
# print(actions)

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
model.save("dnnmodel1.h5")

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


# bot token
client.run(BOT_TOKEN)
