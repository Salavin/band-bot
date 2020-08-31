import re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageColor
from wordfilter import Wordfilter
import config
import discord
import os
import psutil
import random
import requests
import subprocess
import asyncio
import linecache
import sys
from bs4 import BeautifulSoup

TOKEN = config.TOKEN
weatherUrl = config.weatherUrl
forecastUrl = config.forecastUrl
mtUrl = config.mtUrl
timeFormat = "%A %I:%M%p"
client = discord.Client()
client.agreeCounter = 0  # I bound it to the client var because of wack scope issues
wordfilter = Wordfilter()
wordfilter.clear_list()
wordfilter.add_words(['porn', 'fap', 'brazzers', 'nigger', 'niggar', 'masturbate', 'dick', 'dyke', 'fatso', 'fatass', 'faggot', 'homo', 'homosexual', 'gay', 'lesbian', 'hooker', 'pornhub', 'brazzers', 'pornstar', 'porn-star', 'redtube', 'negro', 'nig', 'nig-nog', 'nigga', 'nigguh', 'prostitute', 'pussy', 'retard', 'shemale', 'skank', 'slut', 'street-shitter', 'tits', 'trannie', 'tranny', 'whore', 'wigger', 'cum', 'daddy', 'titties', 'tit', 'sex', 'pinis', 'piinis', 'ngr', 'liberal', 'lib', 'liberals', 'libs', 'republican', 'repub', 'republicans', 'repubs', 'wank', 'wanker', 'deepthroat', 'sperm', 'pron', 'bitch'])

songs = {
    1: 'Go Cyclones Go',
    2: 'Fights!',
    3: 'Rise Sons',
    4: 'For I For S',
    5: 'Fanfare',
    6: 'Bells',
    7: 'Armed Forces Fanface',
    8: 'First Down',
    9: 'Star Wars 2',
    10: 'Star Wars 3',
    11: 'Star Wars 4',
    12: 'Mo Bamba',
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
    32: 'Welper Wings!',
    33: 'Singing Playing'
}

class GameDay:
    def __init__(self, opponent, date, band):
        self.opponent = opponent
        self.date = date
        self.band = band

gamedays = {
    1: GameDay('Louisiana', datetime(2020, 9, 12), 'Cardinal'),
    2: GameDay('Oklahoma', datetime(2020, 10, 3), 'Gold'),
    3: GameDay('Texas Tech', datetime(2020, 10, 10), 'Cardinal'),
    4: GameDay('Baylor', datetime(2020, 11, 7), 'Gold'),
    5: GameDay('Kansas State', datetime(2020, 11, 21), 'TBA'),
    6: GameDay('West Virginia', datetime(2020, 12, 5), 'TBA')
}

async def change_status():
    while True:
        if ((datetime.now().hour == 17) or ((datetime.now().hour == 18) and (datetime.now().minute == 30))) and (datetime.now().weekday() < 5):
            await client.change_presence(activity=discord.Activity(name='band rehearsal', type=discord.ActivityType.watching))
            await asyncio.sleep(5100)
        else:
            tmpnum = random.randrange(1, 34)
            await client.change_presence(activity=discord.Game(name=songs.get(tmpnum)))
        await asyncio.sleep(300)


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
    
def getPrice():
    url ='https://www.partycity.com/adult-inflatable-t-rex-dinosaur-costume---jurassic-world-P636269.html'
    response = requests.get(url)
    #Exits function if url is not found
    if response.status_code == 404:
        print('404 error! Could not find url ' + url)
        return None
    page = BeautifulSoup(response.text, "html.parser")
    price = page.find_all("span", attrs={'class':'strong'})
    try: 
        return float(price[2].string[2:])
    #If site changes and no longer returns useable price, default to 59.99
    except:
        print("Price Error Occured")
        return 59.99


def get_mt():
    while True:
        text = requests.get(mtUrl).json()['data']
        if not wordfilter.blacklisted(text):
            break
    return text


def get_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


async def authorize(message):
    authorized = False
    for role in message.author.roles:
        if role.id == 743537185268957294:
            authorized = True
    if not authorized:
        await message.channel.send("Oops! Doesn't look like you have the correct permissions to run that command.")
    return authorized


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    client.loop.create_task(change_status())


@client.event
async def on_message(message):
    try:
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

        if ('texas' in tmpmessage) or ('mo bamba' in tmpmessage) or ('horns down' in tmpmessage):
            hornsdown = '<:hornsdown:747516646738100234>'
            await message.add_reaction(hornsdown)

        if 'cyclones' in tmpmessage:
            cyclones = '<:cyclones:747516646473728120>'
            await message.add_reaction(cyclones)

        if ("is it a good day for band" in tmpmessage) or \
           ("is it a great day for band" in tmpmessage) or \
           ("is it going to rain" in tmpmessage) or \
           ("is today a good day for band" in tmpmessage) or \
           ("is today a great day for band" in tmpmessage) or \
           ("forecast" in tmpmessage):
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
            
        if ('thirsty' in tmpmessage) or ('drink' in tmpmessage):
            await message.channel.send("Hydrate or Diedrate!")

        if '$' in tmpmessage:
            amount_finder = r"[\$]{1}[\d,]+\.?\d{0,2}"
            amount_list = re.findall(amount_finder, tmpmessage)
            for x in amount_list:
                await message.channel.send("You can buy " + str(int(float(x[1:])/getPrice())) + " inflatable T-Rex costumes with " + x + " from Party City! (!dinolink for link)")

        if '!dinolink' in tmpmessage:
            await message.channel.send("Here you go: https://www.partycity.com/adult-inflatable-t-rex-dinosaur-costume---jurassic-world-P636269.html")
        
        if 'how long til gameday' in tmpmessage:
            for x in gamedays:
                if gamedays.get(x).date == datetime.today():
                    await message.channel.send("It's GAMEDAY for " + gamedays.get(x).band + " band! Beat " + gamedays.get(x).opponent + '!')
                    break
                if (gamedays.get(x).date - datetime.today()).days > 0:
                    await message.channel.send("It is " + str((gamedays.get(x).date - datetime.today()).days) + " days until gameday for " + gamedays.get(x).band + " band. We will play " + gamedays.get(x).opponent)
                    break

        if '!roll' in tmpmessage:
            await message.channel.send(str(random.randint(1, 100)))

        if '!generatememe' in tmpmessage:
            async with message.channel.typing():
                if len(message.attachments) > 0:
                    filename = message.attachments[0].filename
                    await message.attachments[0].save(filename)
                    image = Image.open(filename).convert('RGB')
                    skip = 14
                elif len(message.mentions) > 0:
                    filename = 'avatarimg.jpg'
                    await message.mentions[0].avatar_url.save('tmp.webp')
                    image = Image.open('tmp.webp').convert('RGB')
                    image.save(filename, "jpeg")
                    os.remove("tmp.webp")
                    image = Image.open(filename)
                    if message.content[36] == ' ':
                        skip = 37
                    else:
                        skip = 36
                else:
                    filename = 'prevmeme.jpg'
                    image = Image.open('previmg.jpg')  # Should already be converted
                    image.save(filename)
                    skip = 14
                font = ImageFont.truetype('/home/pi/bot/impact.ttf', size=30)

                # Want max width or height of the image to be = 400
                maxsize = 400
                largest = max(image.size[0], image.size[1])
                scale = maxsize / float(largest)
                resize = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))
                resize.save('previmg.jpg', "jpeg")  # So people can make memes from other memes
                padding = (resize.size[0] * 0.1)  # 10% left boundary

                if ('!random' in tmpmessage) or ('!talk' in tmpmessage):
                    text = get_mt()
                else:
                    text = message.content[skip:]
                lines = text_wrap(text, font, resize.size[0] - padding)
                line_height = font.getsize('hg')[1]

                y_start = (resize.size[1] * 0.9) - (len(lines) * line_height)  # %90 from bottom minus size of lines

                draw = ImageDraw.Draw(resize)
                white = ImageColor.getcolor('white', resize.mode)
                shadow = ImageColor.getcolor('black', resize.mode)

                y = y_start
                for line in lines:
                    w, h = draw.textsize(line, font=font)
                    x = (resize.size[0] - w) / 2
                    change = .5
                    while change != 2:
                        draw.text((x + change, y + change), line, font=font, fill=shadow)
                        draw.text((x + change, y - change), line, font=font, fill=shadow)
                        draw.text((x - change, y + change), line, font=font, fill=shadow)
                        draw.text((x - change, y - change), line, font=font, fill=shadow)
                        change += 0.5
                    draw.text((x, y), line, fill=white, font=font)
                    y = y + line_height
                resize.save(filename)
                await message.channel.send(file=discord.File(filename))
                os.remove(filename)
        else:
            if len(message.attachments) > 0:
                # Open image, convert to jpg, and save as previmg.jpg
                filename = message.attachments[0].filename
                await message.attachments[0].save(filename)
                image = Image.open(message.attachments[0].filename).convert('RGB')
                image.save('previmg.jpg')
                os.remove(filename)

        if ('!talk' in tmpmessage) and ('!generatememe' not in tmpmessage):
            await message.channel.send(get_mt())

        if '!help' in tmpmessage:
            await message.channel.send("Hi there, I'm CarichnerBot! A lot of what I do is respond to certain keywords or react to certain messages, but I do have some commands:\n\n"
                                       "`!help`: Shows this message.\n\n"
                                       "`!talk`: Generates a string of gibberish using Markov Chains. *Disclaimer: may be inappropriate at times. If this says something you don't like, please mention Slav.*\n\n"
                                       "`!generatememe`: This generates a meme with whatever image you attach to your message, along with whatever text you provide it. For example, you can do `!generatememe Meme Text Here`, and it will generate a meme with that text at the bottom of your image.\n"
                                       "Options:\n"
                                       "* Adding `!talk` or `!random` produces gibberish for the meme text, the same from the `!talk` command. Ex: `!generatememe !talk`\n"
                                       "* Mention someone to use their profile picture for the picture! Ex: `!generatememe @Someome *meme text here*`\n"
                                       "* If you don't attach an image with `!generatememe`, it will use the last picture that was sent as the background. With this, you can essentially re-meme other peoples memes! Or, if someone posts a pic you know a funny caption for, just use `!generatememe *meme text here*`!\n\n"
                                       "`!stats`: Shows the uptime and memory usage for the bot.\n\n"
                                       "`!date`: Displays the current date and time.\n\n"
                                       "`!ping`: Shows the current ping for the bot.\n\n"
                                       "`!avatar`: Displays the avatar for any users you mention along with this command. Ex: `!avatar @User`"
                                       "`!dinolink`: Displays the link for the Party City dino costume.")

        if '!stats' in tmpmessage:
            p = subprocess.Popen("uptime", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            await message.channel.send("Uptime: `" + str(output)[3: -3] + "`")
            process = psutil.Process(os.getpid())
            await message.channel.send("Memory: `" + str(process.memory_info().rss / float(1000000)) + " mb`")

        if '!date' in tmpmessage:
            p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            await message.channel.send("`" + str(output)[2: -3] + "`")

        if '!ping' in tmpmessage:
            await message.channel.send("Pong! (`" + str(round(client.latency, 3)) + " s`)")

        if '!avatar' in tmpmessage:
            if len(message.mentions) > 0:
                for mentioned in message.mentions:
                    await message.channel.send(mentioned.avatar_url)
            else:
                await message.channel.send("No mentioned users!")

        if '!restart' in tmpmessage:
            if await authorize(message):
                await message.channel.send("Be back soon (hopefully)!")
                print('Shutting down')
                print('------')
                sys.exit()

    except Exception:
        await message.channel.send("Oh no, I threw an error! <@262043915081875456>")
        await message.channel.send("```" + get_exception() + "```")
        print(get_exception())


client.run(TOKEN)
