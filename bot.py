import discord, random, requests, os, asyncio
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageColor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = 'NzQ2ODQxNTE4NjcyOTY5Nzc5.X0GMXQ.HahdiAEzgxz1C9NrZHhAh4Bocxo'
weatherUrl = "https://api.openweathermap.org/data/2.5/weather?zip=50012,us&appid=7627fa673f7ae31176e1373748ff78ac"
forecastUrl = "https://api.openweathermap.org/data/2.5/onecall?lat=42.031257&lon=-93.652086&appid=7627fa673f7ae31176e1373748ff78ac"
mtUrl = "https://mt.ziad87.net/api/v1/gen"
timeFormat = "%A %I:%M%p"

client = discord.Client()

client.agreeCounter = 0  # I bound it to the client var because of wack scope issues

songs = {
    1: 'Go Cyclones Go',
    2: 'Fights! <:cyclones:747516646473728120>',
    3: 'Rise Sons',
    4: 'For I For S',
    5: 'Fanfare',
    6: 'Bells',
    7: 'Armed Forces Fanface',
    8: 'First Down',
    9: 'Star Wars 2',
    10: 'Star Wars 3',
    11: 'Star Wars 4',
    12: 'Mo Bamba <:hornsdown:747516646738100234>',
    13: 'Atchafalaya',
    14: 'Fat Bottom Girls',
    15: 'Juicy Wiggle',
    16: 'Sweet Caroline',
    17: 'Sucker',
    18: "Eat 'em up",
    19: 'Third Down',
    20: 'Cyclone Power',
    21: "Let's Go State",
    22: 'Hero',
    23: 'Happy Birthday',
    24: 'Chorale Fights',
    25: 'Game of Thrones',
    26: 'Beer Barrel',
    27: 'Boat',
    28: 'Who Knows?',
    29: 'Whatcha gonna do?',
    30: 'Confident',
    31: 'Wings',
    32: 'Welper Wings!'
}


def change_status():
    if (datetime.hour == 17) or ((datetime.hour == 18) and (datetime.minute == 30)):
        await client.change_presence(activity=discord.Activity(name='band rehearsal', type=discord.ActivityType.watching))
    else:
        tmpnum = random.randrange(1, 33)
        await client.change_presence(activity=discord.Game(name=songs.get(tmpnum)))


scheduler = AsyncIOScheduler()
scheduler.add_job(change_status(), 'chron', minute=30)


def text_wrap(text, font, max_width):
    """Wrap text base on specified width.
    This is to enable text of width more than the image width to be display
    nicely.
    @params:
        text: str
            text to wrap
        font: obj
            font of the text
        max_width: int
            width to split the text with
    @return
        lines: list[str]
            list of sub-strings
    """
    lines = []

    # If the text width is smaller than the image width, then no need to split
    # just add it to the line list and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = text.split(' ')
        i = 0
        # append every word to a line while its width is shorter than the image width
        while i < len(words):
            line = ''
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            lines.append(line)
    return lines


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(activity=discord.Activity(name='all of you :eyes:', type=discord.ActivityType.watching))


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
            font = ImageFont.truetype('impact.ttf', size=25)

            # Want max width or height of the image to be = 400
            maxsize = 400
            largest = max(image.size[0], image.size[1])
            scale = maxsize / float(largest)
            rmg = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))

            x_start = (rmg.size[0] * 0.1)  # 10% left boundary

            if ('!random' in tmpmessage) or ('!talk' in tmpmessage):
                text = requests.get(mtUrl).json()['data']
            else:
                text = message.content[14:]
            lines = text_wrap(text, font, rmg.size[0] - x_start)
            line_height = font.getsize('hg')[1]

            y_start = (rmg.size[1] * 0.9) - (len(lines) * line_height)  # %90 from bottom minus size of lines

            draw = ImageDraw.Draw(rmg)
            white = ImageColor.getcolor('white', rmg.mode)
            shadow = ImageColor.getcolor('black', rmg.mode)

            y = y_start
            for line in lines:
                w, h = draw.textsize(line)
                x = ((rmg.size[0] - w) / 2) - x_start  # Center text. Not sure why but I also have to subtract 10%
                draw.text((x - 2, y), line, font=font, fill=shadow)
                draw.text((x + 2, y), line, font=font, fill=shadow)
                draw.text((x, y - 2), line, font=font, fill=shadow)
                draw.text((x, y + 2), line, font=font, fill=shadow)
                draw.text((x, y), line, fill=white, font=font)

                y = y + line_height

            rmg.save(filename)

            await message.channel.send(file=discord.File(filename))
            os.remove(filename)
        else:
            await message.channel.send("No image attached!")

    if ('!talk' in tmpmessage) and ('!generatememe' not in tmpmessage):
        await message.channel.send(requests.get(mtUrl).json()['data'])


client.run(TOKEN)