import discord
import random
import requests
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

TOKEN = 'NzQ2ODQxNTE4NjcyOTY5Nzc5.X0GMXQ.HahdiAEzgxz1C9NrZHhAh4Bocxo'
weatherUrl = "https://api.openweathermap.org/data/2.5/weather?zip=50012,us&appid=7627fa673f7ae31176e1373748ff78ac"

forecastUrl = "https://api.openweathermap.org/data/2.5/onecall?lat=42.031257&lon=-93.652086&appid=7627fa673f7ae31176e1373748ff78ac"
mtUrl = "https://mt.ziad87.net/api/v1/gen"
timeFormat = "%A %I:%M%p"

client = discord.Client()

client.agreeCounter = 0  # i bound it to the client var because of wack scope issues


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

    if tmpmessage == 'agree':
        client.agreeCounter += 1
        if client.agreeCounter == 5:
            client.agreeCounter = 0
            await message.channel.send('stop.')
    else:
        client.agreeCounter = 0

    if 'pregame' in tmpmessage:
        if random.randrange(0, 6) == 5:
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
        if 'love' in tmpmessage:
            await message.channel.send('I love you too, <@' + str(message.author.id) + '> :heart:')
        elif ('hello' in tmpmessage) or ('hi' in tmpmessage):
            await message.channel.send('Hello <@' + str(message.author.id) + '>')

    if "let's go state" in tmpmessage:
        await message.channel.send('Where are we going?')

    if "lets go state" in tmpmessage:
        await message.channel.send('Where are we going?')

    if "cyclone power" in tmpmessage:
        tmpnum = random.randrange(1, 8)
        switcher = {
            1: "Take a shower?",
            2: "Eiffel Tower?",
            3: "Smell a flower?",
            4: "Buy some flower?",
            5: "Sweet and sour?",
            6: "Eisenhower?",
            7: "Protein powder?"
        }
        await message.channel.send(switcher.get(tmpnum, "Oh no! I threw an error!"))

    if "cyclone!" in tmpmessage:
        await message.channel.send("Power!")

    if "gamerz" in tmpmessage:
        tpose = '<:tpose:747146815522078730>'
        await message.add_reaction(tpose)

    if "carichner" in tmpmessage:
        chris = '<:chris:746792499812761606>'
        await message.add_reaction(chris)

    if ("is it a good day for band" in tmpmessage) or ("is it a great day for band" in tmpmessage) or (
            "is it going to rain" in tmpmessage):
        forecast = requests.get(forecastUrl).json()
        hourly = forecast['hourly']
        ms = ''
        for hour in hourly:
            timestamp = datetime.fromtimestamp(hour['dt'])
            if timestamp.hour == 17:
                temp = str(round((hour['temp'] - 273.15) * 9.0 / 5 + 32, 1))
                ms += 'On ' + timestamp.strftime(timeFormat) + ' it will be ' + temp + '°F with a '
                ms += hour['weather'][0]['description'] + '\n'
                ms += 'Looks like a GREAT day for a band rehearsal!'
                await message.channel.send(ms)
                break

    if "current weather" in tmpmessage:
        weather = requests.get(weatherUrl).json()
        temp = str(round((weather['main']['temp'] - 273.15) * 9.0 / 5 + 32, 1))
        ms = 'It is currently ' + temp + '°F with a '
        ms += weather['weather'][0]['description']
        await message.channel.send(ms)

    if (tmpmessage == '2') or (tmpmessage == 'two'):
        await message.channel.send("Buh!")

    if '!roll' in tmpmessage:
        await message.channel.send(str(random.randint(1, 100)))

    if '!generatememe' in tmpmessage:
        if len(message.attachments) > 0:
            filename = message.attachments[0].filename
            await message.attachments[0].save(filename)
            image = Image.open(filename)
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('impact.ttf', size=12)
            (x, y) = (50, 50)
            color = 'rgb(255,255,255)'

            draw.text((x, y), message.content[14:], fill=color, font=font)

            image.save(filename)

            await message.channel.send(file=discord.File(filename))
            os.remove(filename)
        else:
            await message.channel.send("No image attached!")

    if '!talk' in tmpmessage:
        text = requests.get(mtUrl).json()
        await message.channel.send(text['data'])

client.run(TOKEN)
