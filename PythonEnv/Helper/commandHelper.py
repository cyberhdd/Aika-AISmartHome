# Device imports
from Helper import tuyaCommandHelper
from Helper import sofCommandHelper
from Helper import replyHelper
from Helper import extractSlotsHelper
from Helper import nerHelper
import asyncio


# method to check for used sending message is the original sender being waited for
def check_user_input(msg, message):
    return msg.author == message.author and msg.channel == message.channel


# Function for handling "bedroom on"
def handle_bedroom_on(reply_data):
    if reply_data:
        print("Reply:", reply_data)
        tuyaCommandHelper.tuyaCommands("bedroom light on")
    else:
        print("No reply available for the given intent and action")


# Function for handling "bedroom off"
def handle_bedroom_off(reply_data):
    if reply_data:
        print("Reply:", reply_data)
        tuyaCommandHelper.tuyaCommands("bedroom light off")
    else:
        print("No reply available for the given intent and action")


# Function for handling "bedroom status"
async def handle_bedroom_status(reply_data, message):
    if reply_data:
        print(reply_data)
        (
            switch_led_value,
            work_mode_value,
            bright_value,
            temp_value,
            colour_led_value,
        ) = tuyaCommandHelper.tuyaCommands("bedroom light status")
        reply = "Check the connection"
        status = "off"
        if switch_led_value == True:
            status = "on"
        if work_mode_value == "colour":
            reply = (
                "Bedroom Light: "
                + status
                + "\nMode: "
                + str(work_mode_value)
                + "\nColor: "
                + str(colour_led_value)
            )
        elif work_mode_value == "white":
            reply = (
                "Bedroom Light: "
                + status
                + "\nMode: "
                + str(work_mode_value)
                + "\nBrightness: "
                + str((int(bright_value / 10)))
            )  # range for tuya is 10 - 1000
        await message.channel.send(reply)
    else:
        print("No reply available for the given intent and action")


# Function for handling "bathroom on"
def handle_bathroom_on(reply_data):
    if reply_data:
        print("Reply:", reply_data)
        sofCommandHelper.sofCommands("bathroom light on")
    else:
        print("No reply available for the given intent and action")


# Function for handling "bathroom off"
def handle_bathroom_off(reply_data):
    if reply_data:
        print("Reply:", reply_data)
        sofCommandHelper.sofCommands("bathroom light off")
    else:
        print("No reply available for the given intent and action")


# Function for handling "bathroom status"
async def handle_bathroom_status(reply_data, message):
    if reply_data:
        print("Reply:", reply_data)
        (
            switch,
            ltype,
            color,
            brightness,
            temperature,
        ) = sofCommandHelper.sofCommands("bathroom light status")
        reply = "Check the connection"
        if ltype == "color":
            reply = (
                "Bathroom Light: "
                + str(switch)
                + "\nMode: "
                + str(ltype)
                + "\nColor: "
                + str(color)
            )
        elif ltype == "white":
            reply = (
                "Bathroom Light: "
                + str(switch)
                + "\nMode: "
                + str(ltype)
                + "\nBrightness: "
                + str(brightness)
            )
        await message.channel.send(reply)
    else:
        print("No reply available for the given intent and action")


# Function for handling "plug on"
def handle_plug_on(reply_data):
    if reply_data:
        print("Reply:", reply_data)
        tuyaCommandHelper.tuyaCommands("plug on")
    else:
        print("No reply available for the given intent and action")


# Function for handling "plug off"
def handle_plug_off(reply_data):
    if reply_data:
        print("Reply:", reply_data)
        tuyaCommandHelper.tuyaCommands("plug off")
    else:
        print("No reply available for the given intent and action")


# Function for handling "plug status"
async def handle_plug_status(reply_data, message):
    if reply_data:
        print("Reply:", reply_data)
        (
            switch_plug_value,
            power_value,
            current_value,
            voltage_value,
        ) = tuyaCommandHelper.tuyaCommands("plug status")
        status = "off"
        if switch_plug_value == True:
            status = "on"
            print(switch_plug_value, "is on")
        reply = (
            "Plug: "
            + status
            + "\nPower (W): "
            + str(power_value)
            + "\nCurrent (mA): "
            + str(current_value)
            + "\nVoltage (V): "
            + str(voltage_value)
        )
        await message.channel.send(reply)
    else:
        print("No reply available for the given intent and action")


# Function for handling "plug power"
async def handle_plug_power(reply_data, message):
    if reply_data:
        print("Reply:", reply_data)
        power_value = tuyaCommandHelper.tuyaCommands("plug power")
        reply = "Power (W): " + str(power_value)
        await message.channel.send(reply)
    else:
        print("No reply available for the given intent and action")


# Function for handling "brightness control"
async def handle_brightness_control(reply_data, message, input_query, client):
    if reply_data:
        print("Reply:", reply_data)
        room = extractSlotsHelper.extract_slots(input_query)
        print("Extraction room: ", room)
        bright_var = nerHelper.extract_number(input_query)
        print("Extraction brightness: ", bright_var)

        # if room not specified, request user input
        if room is None:
            await message.channel.send(
                "Where do you want to change the brightness? (bedroom/bathroom)"
            )
            try:
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
                    return reply_data
            except asyncio.TimeoutError:
                reply_data = "No location received within the timeout"
                await message.channel.send("Wait Mode: Off")
                return reply_data

        # if brightness not specified
        if bright_var is None:
            # input brightness value
            await message.channel.send(
                "Set a value from 1 to 100 for the brightness (10s)"
            )
            try:
                brightness = await client.wait_for(
                    "message",
                    check=lambda msg: check_user_input(msg, message),
                    timeout=10,
                )
                # check the brightness value input
                # check if any number input
                bright_var = nerHelper.extract_number(brightness.content)
                # bright_var = int(brightness.content)
                print(bright_var, type(bright_var))
                # no number
                if bright_var is None:
                    reply_data = "Sorry, only digits. Please try again"  # change the reply data to an error
                    return reply_data
            except asyncio.TimeoutError:
                reply_data = "No brightness received within the timeout"
                await message.channel.send("Wait Mode: Off")
                return reply_data

        # adjust the brightness value input
        # maximum and minimum brightness
        if bright_var < 1:
            bright_var = 1
            await message.channel.send("Brightness value set to minimum (1)")
        elif bright_var > 100:
            bright_var = 100
            await message.channel.send("Brightness value set to maximum (100)")
        print(bright_var)

        # brightness for bedroom
        if room == "bedroom":
            if bright_var is not None:
                # tuya devices range from 10 to 1000, * 10
                setBrightness = tuyaCommandHelper.tuyaBrightnessSet(bright_var * 10)
            if setBrightness is not None:
                reply_data = "Bedroom brightness has been changed to " + str(bright_var)
            return reply_data

        # brightness for bathroom
        elif room == "bathroom":
            if bright_var is not None:
                setBrightness = sofCommandHelper.sofBrightnessSet(bright_var)
            if setBrightness is not None:
                reply_data = "Bathroom brightness has been changed to " + str(
                    bright_var
                )
            return reply_data
        else:
            print(room, " error")
            return None
    else:
        print("No reply available for the given intent and action")
    return None


# Function for handling "color control"
async def handle_color_control(reply_data, message, input_query, client):
    if reply_data:
        print("Reply:", reply_data)
        room = extractSlotsHelper.extract_slots(input_query)
        print("Extraction room: ", room)
        color = extractSlotsHelper.extract_color_slots(input_query)
        print("Extraction color: ", color)

        # if room not specified, request user input
        if room is None:
            await message.channel.send(
                "Where do you want to change the color? (bedroom/bathroom)"
            )
            try:
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
                    return reply_data
            except asyncio.TimeoutError:
                reply_data = "No location received within the timeout"
                await message.channel.send("Wait Mode: Off")
                return reply_data

        # if color not specified, request user input
        if color is None:
            await message.channel.send(
                "What color do you want? (white, yellow, red, green, blue, orange, purple)"
            )
            try:
                await message.channel.send("Wait Mode: On (10s)")
                color_message = await client.wait_for(
                    "message",
                    check=lambda msg: check_user_input(msg, message),
                    timeout=10,
                )
                color_content = color_message.content
                color = extractSlotsHelper.get_color_slots(color_content)

                if room is None:
                    reply_data = "No such color, please try again"  # change the reply data to an error
                    await message.channel.send("Wait Mode: Off")
                    return reply_data
            except asyncio.TimeoutError:
                reply_data = "No color received within the timeout"
                await message.channel.send("Wait Mode: Off")
                return reply_data

        # color for bedroom
        if room == "bedroom":
            if color is not None:
                setColor = tuyaCommandHelper.tuyaColorSet(color)
            if setColor is not None:
                reply_data = "Bedroom light color has been changed to " + str(color)
            return reply_data

        # color for bathroom
        elif room == "bathroom":
            if color is not None:
                setColor = sofCommandHelper.sofColorSet(color)
            if setColor is not None:
                reply_data = "Bathroom light color has been changed to " + str(color)
            return reply_data
        else:
            print(room, " error")
            return None
    else:
        print("No reply available for the given intent and action")
    return None


# Function for handling "light on"
async def handle_light_on(reply_data, message, client):
    if reply_data:
        await message.channel.send(reply_data)
        try:
            await message.channel.send("Wait Mode: On (10s)")
            location_message = await client.wait_for(
                "message",
                check=lambda msg: check_user_input(msg, message),
                timeout=10,
            )
            location = location_message.content
            room = extractSlotsHelper.get_all_location_slots(location)

            if room is None:
                reply_data = "No such location, please try again"  # change the reply data to an error
                await message.channel.send("Wait Mode: Off")
                return reply_data
        except asyncio.TimeoutError:
            print("No location received within the timeout")
            reply_data = "No such location, please try again"
            await message.channel.send("Wait Mode: Off")
            return reply_data

        # room for bedroom
        if room == "bedroom":
            handle_bedroom_on(reply_data)
            reply_data = replyHelper.get_reply("bedroom", "on")

        # room for bathroom
        elif room == "bathroom":
            handle_bathroom_on(reply_data)
            reply_data = replyHelper.get_reply("bathroom", "on")

        # room for both
        elif room == "both":
            handle_bathroom_on(reply_data)
            handle_bedroom_on(reply_data)
            reply_data = replyHelper.get_reply("both", "on")
        else:
            print(room, " error")
            return None
        print("Reply:", reply_data)
        # await message.channel.send(reply_data)
        return reply_data
    else:
        print("No reply available for the given intent and action")


# Function for handling "light off"
async def handle_light_off(reply_data, message, client):
    if reply_data:
        await message.channel.send(reply_data)
        try:
            await message.channel.send("Wait Mode: On (10s)")
            location_message = await client.wait_for(
                "message",
                check=lambda msg: check_user_input(msg, message),
                timeout=10,
            )
            location = location_message.content
            room = extractSlotsHelper.get_all_location_slots(location)

            if room is None:
                reply_data = "No such location, please try again"  # change the reply data to an error
                await message.channel.send("Wait Mode: Off")
                return reply_data
        except asyncio.TimeoutError:
            print("No location received within the timeout")
            reply_data = "No such location, please try again"
            await message.channel.send("Wait Mode: Off")
            return reply_data

        # room for bedroom
        if room == "bedroom":
            handle_bedroom_off(reply_data)
            reply_data = replyHelper.get_reply("bedroom", "off")

        # room for bathroom
        elif room == "bathroom":
            handle_bathroom_off(reply_data)
            reply_data = replyHelper.get_reply("bathroom", "off")

        # room for both
        elif room == "both":
            handle_bathroom_off(reply_data)
            handle_bedroom_off(reply_data)
            reply_data = replyHelper.get_reply("both", "off")
        else:
            print(room, " error")
            return None
        print("Reply:", reply_data)
        # await message.channel.send(reply_data)
        return reply_data
    else:
        print("No reply available for the given intent and action")


# Function for handling "light status"
async def handle_light_status(reply_data, message, client):
    if reply_data:
        await message.channel.send(reply_data)
        try:
            await message.channel.send("Wait Mode: On (10s)")
            location_message = await client.wait_for(
                "message",
                check=lambda msg: check_user_input(msg, message),
                timeout=10,
            )
            location = location_message.content
            room = extractSlotsHelper.get_all_location_slots(location)

            if room is None:
                reply_data = "No such location, please try again"  # change the reply data to an error
                await message.channel.send("Wait Mode: Off")
                return reply_data
        except asyncio.TimeoutError:
            print("No location received within the timeout")
            reply_data = "No such location, please try again"
            await message.channel.send("Wait Mode: Off")
            return reply_data

        # room for bedroom
        if room == "bedroom":
            await handle_bedroom_status(reply_data, message)
            reply_data = replyHelper.get_reply("bedroom", "status")

        # room for bathroom
        elif room == "bathroom":
            await handle_bathroom_status(reply_data, message)
            reply_data = replyHelper.get_reply("bathroom", "status")

        # room for both
        elif room == "both":
            await handle_bedroom_status(reply_data, message)
            await handle_bathroom_status(reply_data, message)
            reply_data = replyHelper.get_reply("both", "status")
        else:
            print(room, " error")
            return None
        print("Reply:", reply_data)
        # await message.channel.send(reply_data)
        return reply_data
    else:
        print("No reply available for the given intent and action")
