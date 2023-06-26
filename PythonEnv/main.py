# discord imports
import discord
from discord.ext import commands
from discord.ext import tasks  # for task implementation
from itertools import cycle  # for task to change between status
import json
import asyncio

# AI model imports
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from Helper import replyHelper
from Helper import userInputHelper
import joblib

# Device imports
from Helper import tuyaCommandHelper
from Helper import sofCommandHelper

#########################################################################
########################### Credential Section #########################
#########################################################################
# For discord
credentials = json.load(open("config/credentials.json"))
BOT_TOKEN = credentials["bot_token"]
# print(BOT_TOKEN)
channelID = json.load(open("config/channel.json"))

# For model
# Load tokenizer
with open("tokenizer_v1_2.json", "r") as f:
    tokenizer_data = json.load(f)
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_data)
# Load label encoders
intent_label_encoder = joblib.load("intent_label_encoder_v1_2.pkl")
action_label_encoder = joblib.load("action_label_encoder_v1_2.pkl")
# Load encoded queries
encoded_queries = joblib.load("encoded_queries_v1_2.pkl")
# Load trained model
model = tf.keras.models.load_model("dnnmodel_v1_2.h5")

# For device
openapi, tuyaConnection = tuyaCommandHelper.tuyaConnection()
print(openapi, tuyaConnection)
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
    channelID["channel5"],
]

# bool to activate teaching and not respond to messages
# Teach = False

client = commands.Bot(command_prefix="", intents=intents)
# list of bot status
status = cycle(["Learning Humanity", "Learning You", "Compiling Humanity", "Humanity"])


# when bot ready###################################################
@client.event
async def on_ready():
    print("Bot is ready")

    """ # bool to activate teaching and not respond to messages
    Teach = False """

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
    global Teach  # accessing a global variable defined beforehand
    if message.author.bot:  # if bot sender, stop
        return
    # elif Teach == True:  # ensure new message is not for teaching
    # return
    elif message.channel.id not in channel_list:  # if not in correct channel
        return
    else:
        print("Message processing")
        input_query = message.content
        # Tokenize and pad the input query
        encoded_input_query = tokenizer.texts_to_sequences([input_query])
        print(encoded_input_query)
        max_sequence_length = max(len(seq) for seq in encoded_queries)
        padded_input_queries = pad_sequences(
            encoded_input_query, maxlen=max_sequence_length
        )
        print(input_query)  # print in console

        # predict
        intent_probabilities, action_probabilities = model.predict(padded_input_queries)
        print(
            "intent_probabilities: ",
            intent_probabilities,
            "\naction_probabilities: ",
            action_probabilities,
        )

        # Decode the predictions
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
        if intent_probabilities[0].max() > 0.7 and action_probabilities[0].max() > 0.7:
            """# print labels for testing
            labels = "Intent: " + str(intent_label) + "\nAction: " + str(action_label)
            await message.channel.send(labels)  # print in discord from bot"""

            # Perform action when both probabilities are higher than 0.8
            print("Your probabilities are high enough")
            print(
                f"Your {intent_labels} probability is at {intent_probabilities[0].max()}"
            )
            print(
                f"Your {action_labels} probability is at {action_probabilities[0].max()}"
            )

            # bedroom on
            if intent_labels == "bedroom" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("bedroom light on")
                else:
                    print("No reply available for the given intent and action")

            # bedroom off
            elif intent_labels == "bedroom" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("bedroom light off")
                else:
                    print("No reply available for the given intent and action")

            # bedroom status
            elif intent_labels == "bedroom" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print(reply_data)
                    tuyaCommandHelper.tuyaCommands("bedroom light status")
                else:
                    print("No reply available for the given intent and action")

            # bathroom on
            elif intent_labels == "bathroom" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    sofCommandHelper.sofCommands("bathroom light on")
                else:
                    print("No reply available for the given intent and action")

            # bathroom off
            elif intent_labels == "bathroom" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    sofCommandHelper.sofCommands("bathroom light off")
                else:
                    print("No reply available for the given intent and action")

            # bathroom status
            elif intent_labels == "bathroom" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    sofCommandHelper.sofCommands("bathroom light status")
                else:
                    print("No reply available for the given intent and action")

            # plug on
            elif intent_labels == "plug" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("plug on")
                else:
                    print("No reply available for the given intent and action")

            # plug off
            elif intent_labels == "plug" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("plug off")
                else:
                    print("No reply available for the given intent and action")

            # plug status
            elif intent_labels == "plug" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("plug status")
                else:
                    print("No reply available for the given intent and action")

            # plug power
            elif intent_labels == "plug" and action_labels == "power":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("plug power")
                else:
                    print("No reply available for the given intent and action")

            # both on
            elif intent_labels == "both" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("bedroom light on")
                    sofCommandHelper.sofCommands("bathroom light on")
                else:
                    print("No reply available for the given intent and action")

            # both off
            elif intent_labels == "both" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("bedroom light off")
                    sofCommandHelper.sofCommands("bathroom light off")
                else:
                    print("No reply available for the given intent and action")

            # both status
            elif intent_labels == "both" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    tuyaCommandHelper.tuyaCommands("bedroom light status")
                    sofCommandHelper.sofCommands("bathroom light status")
                else:
                    print("No reply available for the given intent and action")

            # both brightness
            elif intent_labels == "both" and action_labels == "brightness":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)

                else:
                    print("No reply available for the given intent and action")

            # both color
            elif intent_labels == "both" and action_labels == "color":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")

            # light on
            elif intent_labels == "light" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")

            # light off
            elif intent_labels == "light" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")

            # light status
            elif intent_labels == "light" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")

        else:
            # Perform no intent action
            reply_data = replyHelper.get_reply("error", "repeat")
            print("Reply:", reply_data)
            print("Your probabilities are too low")
            print(
                f"Your {intent_labels} probability is at {intent_probabilities[0][0]}"
            )
            print(
                f"Your {action_labels} probability is at {action_probabilities[0][0]}"
            )

            """ # save user query and intended action if low probability
            # Wait for the next user input
            def check_user_input(msg):
                return msg.author == message.author and msg.channel == message.channel

            # await message.channel.send(reply_data + "\nIntended action:")
            await message.channel.send(reply_data)
            try:
                Teach = True  # Teach mode
                await message.channel.send("Teach Mode: On (20s)")
                action_message = await client.wait_for(
                    "message", check=check_user_input, timeout=20
                )
                action_input = action_message.content
                userInputHelper.append_data(input_query, action_input)
                print(f"Saved!\Query: {input_query}\nIntent & Action: {action_input}")
                confirm_message = "Thanks! I'll learn it in a bit"

                await message.channel.send(confirm_message)
                Teach = False  # Teach mode off
                await message.channel.send("Teach Mode: Off")
                return
            except asyncio.TimeoutError:
                print("No input received within the timeout")
                Teach = False  # Teach mode off
                await message.channel.send("Teach Mode: Off")
                return """

        send_message = reply_data
        # print(send_message)
        await message.channel.send(send_message)  # print in discord from bot
        return


#########################################################################
########################## AI Prediction Section ########################
#########################################################################


# bot token
client.run(BOT_TOKEN)
