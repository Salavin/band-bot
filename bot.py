import discord
import random

TOKEN = 'NzQ2ODQxNTE4NjcyOTY5Nzc5.X0GMXQ.HahdiAEzgxz1C9NrZHhAh4Bocxo'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    tmpmessage = message.content.lower()

    if 'cool' in tmpmessage:
        await message.channel.send('Ice Cold!')

    if 'go cyclones' in tmpmessage:
        await message.channel.send('Yeah! Cyclones!')

    if 'we love the cyclones' in tmpmessage:
        await message.channel.send('Yeah! Love')

    if 'sense' in tmpmessage:
        await message.channel.send('Dollars!')

    if 'dig' in tmpmessage:
        await message.channel.send('With a shovel!')

    if 'super' in tmpmessage:
        await message.channel.send('Super duper dad!')

    if 'step show' in tmpmessage:
        await message.channel.send('Cancelled.')

    if (tmpmessage == 'agree') and (random.randrange(0,6) == 5):
        await message.channel.send('stop.')

    if 'pregame' in tmpmessage:
        if random.randrange(0,6) == 5:
            await message.channel.send('ON the field :wink:')
        else:
            await message.channel.send('Off the field!')

    if 'rise sons' in tmpmessage:
        await message.channel.send('Starts with drums!')

    if ('box' in tmpmessage) and ('link' in tmpmessage) and ('?' in tmpmessage):
        await message.channel.send('Box link: https://iastate.box.com/v/ISUCFVMB2020')

    if 'hey band' in tmpmessage:
        await message.channel.send('Hey what?')

    if 'tweet tweet tweet' in tmpmessage:
        await message.channel.send('GO STATE')

    if 'carichnerbot' in tmpmessage:
        if ('love' in tmpmessage):
            await message.channel.send('I love you too, <@' + str(message.author.id) + '> :heart:')
        else:
            await message.channel.send('Hello <@' + str(message.author.id) + '>')

    if "let's go state" in tmpmessage:
        await message.channel.send('Where are we going?')

    if "lets go state" in tmpmessage:
        await message.channel.send('Where are we going?')

    if "cyclone power" in tmpmessage:
        tmpNum = random.randrange(1,8)
        switcher = {
            1: "Take a shower?",
            2: "Eiffel Tower?",
            3: "Smell a flower?",
            4: "Buy some flower?",
            5: "Sweet and sour?",
            6: "Eisenhower?",
            7: "Protein powder?"
        }
        await message.channel.send(switcher.get(tmpNum, "Oh no! I threw an error!"))

    if "cyclone!" in tmpmessage:
        await message.channel.send("Power!")

    if "gamerz" in tmpmessage:
        tpose = '<:tpose:747146815522078730>'
        await message.add_reaction(tpose)

    if "carichner" in tmpmessage:
        chris = '<:chris:746792499812761606>'
        await message.add_reaction(chris)

client.run(TOKEN)

