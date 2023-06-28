import discord


async def wait_for_user_input(message, check_user_input):
    await message.channel.send("Wait Mode: On (10s)")
    user_message = await client.wait_for(
        "message",
        check=lambda msg: check_user_input(msg, message),
        timeout=10,
    )
    return user_message


def check_user_input(msg, original_message):
    return (
        msg.author == original_message.author
        and msg.channel == original_message.channel
    )


# method to obtain the brightness value
async def brightnessInput(message, check_user_input, client):
    await message.channel.send("Set a value from 1 to 100 for the brightness (10s)")
    brightness = await client.wait_for(
        "message",
        check=lambda msg, original_message=message: check_user_input(
            msg, original_message
        ),
        timeout=10,
    )
    # check if value is an integer
    try:
        bright_var = int(brightness.content)
        print(bright_var, type(bright_var))

        # maximum and minimum brightness
        if bright_var < 1:
            bright_var = 1
            await message.channel.send("Brightness value set to minimum (1)")
        elif bright_var > 100:
            bright_var = 100
            await message.channel.send("Brightness value set to maximum (100)")
        return bright_var
    except ValueError:
        return None
