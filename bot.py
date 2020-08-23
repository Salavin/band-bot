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
        await message.channel.send('cancelled')

    if 'agree' in tmpmessage:
        await message.channel.send('stop.')

    if 'pregame' in tmpmessage:
        if random.randrange(0,6,1) == 5:
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
            await message.channel.send('I love you too, <@' + str(message.author.id) + '>')
        else:
            await message.channel.send('Hello <@' + str(message.author.id) + '>')

client.run(TOKEN)

