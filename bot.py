import discord

TOKEN = 'NzQ2ODQxNTE4NjcyOTY5Nzc5.X0GMXQ.dvOV6vnJv1vNMy1uHTdkAciELpc'

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

    if 'cool' in message.content:
        await message.channel.send('Ice Cold!')

    if 'Go Cyclones' in message.content:
        await message.channel.send('Yeah! Cyclones!')

    if 'We love the Cyclones' in message.content:
        await message.channel.send('Yeah! Love')

    if 'sense' in message.content:
        await message.channel.send('Dollars!')

    if 'dig' in message.content:
        await message.channel.send('With a shovel!')

    if 'super' in message.content:
        await message.channel.send('Super duper dad!')

    if 'step show' in message.content:
        await message.channel.send('cancelled')

client.run(TOKEN)

