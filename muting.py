import asyncio

muted = False


async def muter(channel):
    await channel.send(
        "Okay! For the next 15 minutes I will only respond to explicit commands (starting with '!').")
    global muted
    muted = True
    await asyncio.sleep(15)
    muted = False
    await channel.send("I'm baaaaaaaaaaaaaack!")
