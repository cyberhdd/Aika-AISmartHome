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

# helper module
from Helper import extractSlotsHelper
from Helper import nerHelper

#########################################################################
########################### Credential Section #########################
#########################################################################
# for config
credentials = json.load(open("config/credentials.json"))
BOT_TOKEN = credentials["bot_token"]
# print(BOT_TOKEN)
channelID = json.load(open("config/channel.json"))

# for loading model
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
Teach = False
WaitMode = False
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


# Wait for the next user input
def check_user_input(msg, message):
    return msg.author == message.author and msg.channel == message.channel


@client.event
async def on_message(message):
    global Teach  # accessing a global variable defined beforehand
    global WaitMode
    if message.author.bot:  # if bot sender, stop
        return
    elif Teach == True:  # ensure new message is not for teaching
        return
    elif WaitMode == True:  # if bot on wait mode
        return
    elif message.channel.id not in channel_list:  # if not in correct channel
        """#for testing excluded channel
        print("Message incoming")
        channel_id_print = message.channel.id
        print(channel_id_print)
        print(type(channel_id_print))
        print(channel_list)
        await message.channel.send(
            "This channel isnt included"
        )  # print in discord from bot"""
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
            # print labels for testing
            labels = "Intent: " + str(intent_label) + "\nAction: " + str(action_label)
            await message.channel.send(labels)  # print in discord from bot

            # Perform action when both probabilities are higher than 0.8
            print("Your probabilities are high enough")
            print(
                f"Your {intent_labels} probability is at {intent_probabilities[0].max()}"
            )
            print(
                f"Your {action_labels} probability is at {action_probabilities[0].max()}"
            )

            if intent_labels == "bedroom" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "bedroom" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "bedroom" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "bathroom" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "bathroom" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "bathroom" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "plug" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "plug" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "plug" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "plug" and action_labels == "power":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "both" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "both" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "both" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")

            # brightness control, handles for all brightness
            elif action_labels == "brightness":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                print(reply_data)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                    room = extractSlotsHelper.extract_slots(input_query)
                    print("Extraction room: ", room)
                    bright_var = nerHelper.extract_number(input_query)
                    print("Extraction brightness: ", bright_var)

                    # if room not specified, request user input
                    if room is None:
                        await message.channel.send(
                            "Where do you want change the brightness? (bedroom/bathroom)"
                        )
                        try:
                            WaitMode = True  # Wait mode
                            await message.channel.send("Wait Mode: On (10s)")
                            location_message = await client.wait_for(
                                "message",
                                check=lambda msg: check_user_input(msg, message),
                                timeout=10,
                            )
                            location = location_message.content
                            room = extractSlotsHelper.get_slots(location)

                            if room is None:
                                reply_data = "No such location, please try again"  # change the reply data to an error
                                await message.channel.send("Wait Mode: Off")
                                WaitMode = False
                                return
                        except asyncio.TimeoutError:
                            print("No location received within the timeout")
                            WaitMode = False  # Wait mode off
                            await message.channel.send("Wait Mode: Off")
                            return

                    # if brightness not specified
                    if bright_var is None:
                        # input brightness value
                        await message.channel.send(
                            "Set a value from 1 to 100 for the brightness (10s)"
                        )
                        try:
                            WaitMode = (
                                True  # set wait mode to true for brightness input
                            )
                            brightness = await client.wait_for(
                                "message",
                                check=lambda msg: check_user_input(msg, message),
                                timeout=10,
                            )
                            WaitMode = False
                            # check the brightness value input
                            # check if any number input
                            bright_var = nerHelper.extract_number(brightness.content)
                            # bright_var = int(brightness.content)
                            print(bright_var, type(bright_var))
                            # no number
                            if bright_var is None:
                                reply_data = "Sorry, only digits. Please try again"  # change the reply data to an error
                                return
                        except ValueError:
                            WaitMode = False
                            return None

                    # adjust the brightness value input
                    # maximum and minimum brightness
                    if bright_var < 1:
                        bright_var = 1
                        await message.channel.send(
                            "Brightness value set to minimum (1)"
                        )
                    elif bright_var > 100:
                        bright_var = 100
                        await message.channel.send(
                            "Brightness value set to maximum (100)"
                        )
                    print(bright_var)

                    # brightness for bedroom
                    if room == "bedroom":
                        reply_data = "Bedroom brightness has been changed to " + str(
                            bright_var
                        )

                    # brightness for bathroom
                    elif room == "bathroom":
                        reply_data = "Bathroom brightness has been changed to " + str(
                            bright_var
                        )
                    else:
                        print(room, " error")
                else:
                    print("No reply available for the given intent and action")

            elif intent_labels == "both" and action_labels == "color":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "light" and action_labels == "on":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "light" and action_labels == "off":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")
            elif intent_labels == "light" and action_labels == "status":
                reply_data = replyHelper.get_reply(intent_label, action_label)
                # for error handling
                if reply_data:
                    print("Reply:", reply_data)
                else:
                    print("No reply available for the given intent and action")

            # others with labels above threshold but not defined above
            else:
                reply_data = replyHelper.get_reply("error", "repeat")

        else:
            # Perform no intent action
            reply_data = replyHelper.get_reply("error", "teach")
            print("Reply:", reply_data)
            """ print("Your probabilities are too low")
            print(f"Your {intent_labels} probability is at {intent_probabilities[0][0]}")
            print(f"Your {action_labels} probability is at {action_probabilities[0][0]}") """

            # save user query and intended action if low probability
            # await message.channel.send(reply_data + "\nIntended action:")
            await message.channel.send(reply_data)
            try:
                Teach = True  # Teach mode
                await message.channel.send("Teach Mode: On (20s)")
                """ action_message = await client.wait_for(
                    "message", check=check_user_input, timeout=20
                ) """
                action_message = await client.wait_for(
                    "message",
                    check=lambda msg: check_user_input(msg, message),
                    timeout=20,
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
                return

        # print if no reply data from any intent and is None
        if reply_data is None:
            reply_data = "Sorry, I didnt get that"
        send_message = reply_data
        # print(send_message)
        await message.channel.send(send_message)  # print in discord from bot
        return


#########################################################################
########################## AI Prediction Section ########################
#########################################################################


# bot token
client.run(BOT_TOKEN)
