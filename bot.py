import re
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageColor
from wordfilter import Wordfilter
import config
import lists
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
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
client.agreeCounter = 0  # I bound it to the client var because of wack scope issues
client.mute = False
wordfilter = Wordfilter()
wordfilter.clear_list()
wordfilter.add_words(config.banned_words)
client.last_response_time = datetime.now() - timedelta(minutes=3)
client.prev_dm_user = None


class GameDay:
    def __init__(self, opponent, date, band):
        self.opponent = opponent
        self.date = date
        self.band = band


# gamedays = {
#     1: GameDay('Louisiana', datetime(2020, 9, 12), 'Cardinal'),
#     2: GameDay('Oklahoma', datetime(2020, 10, 3), 'Gold'),
#     3: GameDay('Texas Tech', datetime(2020, 10, 10), 'Cardinal'),
#     4: GameDay('Baylor', datetime(2020, 11, 7), 'Gold'),
#     5: GameDay('Kansas State', datetime(2020, 11, 21), 'TBA'),
#     6: GameDay('West Virginia', datetime(2020, 12, 5), 'TBA')
# }


async def change_status():
    while True:
        # if ((datetime.now().hour == 17) or ((datetime.now().hour == 18)
        #                                     and (datetime.now().minute == 30))) and (datetime.now().weekday() < 5):
        #     await client.change_presence(
        #         activity=discord.Activity(name='band rehearsal', type=discord.ActivityType.watching))
        #     await asyncio.sleep(5100)
        # else:
        #     await client.change_presence(activity=discord.Game(name=random.choice(lists.songs)))
        # await asyncio.sleep(300)

        song = random.choice(lists.songs)
        await client.change_presence(activity=discord.Game(name=song.title))
        await asyncio.sleep(song.length)


async def mute(message):
    await message.channel.send(
        "Okay! For the next 15 minutes I will only respond to explicit commands (starting with '!').")
    client.mute = True
    await asyncio.sleep(900)
    client.mute = False
    await message.channel.send("I'm baaaaaaaaaaaaaack!")


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


def get_price():
    url = 'https://www.partycity.com/adult-inflatable-t-rex-dinosaur-costume---jurassic-world-P636269.html'
    response = requests.get(url)
    # Exits function if url is not found
    if response.status_code == 404:
        print('404 error! Could not find url ' + url)
        return None
    page = BeautifulSoup(response.text, "html.parser")
    price = page.find_all("span", attrs={'class': 'strong'})
    try:
        return float(price[2].string[2:])
    # If site changes and no longer returns usable price, default to 59.99
    except:
        print("Price Error Occurred.")
        return 59.99


def get_mt():
    while True:
        text = requests.get(mtUrl).json()['data']
        if not wordfilter.blacklisted(text):
            break
    return text


def get_exception():
    _, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


async def authorize(message):
    authorized = False
    for role in message.author.roles:
        if role.id == 750486445105479702:
            authorized = True
    if not authorized:
        await message.channel.send("Oops! Doesn't look like you have the correct permissions to run that command.")
    return authorized


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(discord.version_info)
    print('------')
    client.loop.create_task(change_status())


@client.event
async def on_member_join(member):
    found = False
    guild = client.get_guild(743519350501277716)
    for guildMember in guild.members:
        if guildMember == member:
            found = True
            break
    if not found:
        return
    guild = client.get_guild(746851271901708428)
    for guildMember in guild.members:
        if guildMember == member:
            return
            # If the member exists in both servers, don't send the welcome message
            # THIS CREATES AN EDGE CASE where if the user joined another server that this bot is in before joining the band server it won't send the message.
            # However I cannot foresee a way to fix this edge case, and the probability of this happening is very low anyways, so I'm not going to worry about it
    embed = discord.Embed(title="Welcome! :wave:",
                          description="Hello " + member.name + ", and welcome to the I.S.U.C.F.V.M.B. server! This is just a place for us to all hang out together, exchange memes, and have fun! Here are the rules for the server:\n\n"
                                                               "1: No NSFW\n"
                                                               "2: No harassing other members\n"
                                                               "3: Do not spam/troll the server\n"
                                                               "4: Be respectful of each other\n\n"
                                                               "If you feel uncomfortable or if you feel like you are being treated unfairly, please dm or mention <@262043915081875456>\n\n"
                                                               "PLEASE invite people to the server! The more people that join, the more active the server will be. You can even invite alumni!\n\n"
                                                               "If you have ANY suggestions for the server (ways to improve, emotes to add, etc), use the <#746895339818319923> channel, or dm <@262043915081875456>\n\n"
                                                               "Note: this server isn't sanctioned in any way by Carichner, Shields, or anyone else on Pro Staff; this is purely student-run.\n\n"
                                                               "Now that you have read the rules, head over to <#743972368707354734> to give yourself some roles! By giving yourself a section role, you will be given access to a private channel with just your section, and also a cool color for your name :eyes:\n\n"
                                                               "If you're on leadership (guide, captain, stu-staff, drum major), let me know and I can give you that role.\n\n")
    await member.send(embed=embed)


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        tmpmessage = message.content.lower()

        not_command = not tmpmessage.startswith('!')

        in_main_server = not isinstance(message.channel,
                                        discord.DMChannel) and message.channel.guild.id == 743519350501277716

        if isinstance(message.channel, discord.DMChannel):  # If we are being sent a DM, relay this to our server
            channel = client.get_channel(784197374959943731)
            author = client.get_user(message.author.id)
            client.prev_dm_user = author
            embed = discord.Embed(
                type="rich",
                description=message.content
            )
            embed.set_author(
                name=author.name + "#" + author.discriminator,
                icon_url=str(message.author.avatar_url))
            if len(message.attachments) > 0:
                embed.set_image(url=message.attachments[0].url)
            await channel.send(embed=embed)

        if message.channel.id == 784197374959943731:  # Responding to the previous user's DM
            if client.prev_dm_user is None:
                return
            if len(message.content) > 0:
                await client.prev_dm_user.send(content=message.content)
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    await client.prev_dm_user.send(content=attachment.url)

        if not_command and (client.mute is True):
            return

        if '!generatememe' in tmpmessage:
            async with message.channel.typing():
                if len(message.attachments) > 0:  # If the user included an image
                    filename = "upload/" + message.attachments[0].filename
                    await message.attachments[0].save(filename)
                    image = Image.open(filename).convert('RGB')
                    skip = 14
                elif len(message.mentions) > 0:  # If the user mentioned someone
                    filename = 'upload/avatarimg.jpg'
                    await message.mentions[0].avatar_url.save('tmp.webp')
                    image = Image.open('tmp.webp').convert('RGB')
                    image.save(filename, "jpeg")
                    os.remove("tmp.webp")
                    image = Image.open(filename)
                    if (len(message.content) > 36) and (message.content[36] == ' '):
                        skip = 37
                    else:
                        skip = 36
                else:  # If the user did not mention or include an image, use the previous image seen by the bot.
                    filename = 'upload/prevmeme.jpg'
                    image = Image.open('upload/previmg.jpg')  # Should already be converted
                    image.save(filename)
                    skip = 14
                font = ImageFont.truetype('impact.ttf', size=30)

                # Want max width or height of the image to be = 400
                maxsize = 400
                largest = max(image.size[0], image.size[1])
                scale = maxsize / float(largest)
                resize = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))
                if (not isinstance(message.channel, discord.DMChannel)) and (message.guild.id == 743519350501277716):
                    resize.save('upload/previmg.jpg',
                                "jpeg")  # So people can make memes from other memes, but only if from the main server.
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
                    w, _ = draw.textsize(line, font=font)
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
            if (len(message.attachments) > 0) and in_main_server:
                # Open image, convert to jpg and save as previmg.jpg, but only if from the main server.
                filename = message.attachments[0].filename.lower()
                # Check to see that we're actually saving an image
                if (filename[-3:] == 'jpg') or (filename[-3:] == 'png') or (filename[-4:] == "jpeg"):
                    await message.attachments[0].save("upload/" + filename)
                    image = Image.open("upload/" + filename)
                    if (image.format == "JPG") or (image.format == "PNG") or (image.format == "JPEG"):
                        image.convert("RGB").save('upload/previmg.jpg')
                        os.remove("upload/" + filename)

        if in_main_server and not_command:
            channel_id = message.channel.id
            # Prevent bot responding to messages in these channels:
            if channel_id in lists.valid_channels:
                return

        if (datetime.now() - client.last_response_time) > timedelta(
            minutes=2):  # Only run this if it has been at least 3 minutes since the last response
            for key in lists.responses.keys():
                if key in tmpmessage:
                    await message.channel.send(lists.responses[key])
                    client.last_response_time = datetime.now()
                    return  # Prevent bot from responding multiple times

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

        if ('box' in tmpmessage) and ('link' in tmpmessage) and ('?' in tmpmessage):
            await message.channel.send('Box link: https://iastate.box.com/v/ISUCFVMB2020')

        if 'carichnerbot' in tmpmessage:
            if 'love' in tmpmessage:
                await message.channel.send('I love you too, <@' + str(message.author.id) + '> :heart:')
            elif ('hello' in tmpmessage) or ('hi' in tmpmessage):
                await message.channel.send('Hello <@' + str(message.author.id) + '>')

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

        if "current weather" in tmpmessage or "!weather" in tmpmessage:
            weather = requests.get(weatherUrl).json()
            temp = str(round((weather['main']['temp'] - 273.15) * 9.0 / 5 + 32, 1))
            ms = 'It is currently ' + temp + '°F with a '
            ms += weather['weather'][0]['description']
            await message.channel.send(ms)

        if '$' in tmpmessage:
            amount_finder = r"[\$]{1}[\d,]+\.?\d{0,2}"
            amount_list = re.findall(amount_finder, tmpmessage)
            for x in amount_list:
                if '.' in x:
                    await message.channel.send("You can buy " + str(int(float((x[1:]).replace(',',
                                                                                              '')) / get_price())) + " inflatable T-Rex costumes with " + x + " from Party City! (!dinolink for link)")
                else:
                    msg = "You can buy " + str(int(int((x[1:]).replace(',', '')) // int(
                        get_price()))) + " inflatable T-Rex costumes with " + x + " from Party City! (!dinolink for link)"
                    if len(msg) > 2000:
                        await message.channel.send("You can buy")
                        await message.channel.send(str(int(int((x[1:]).replace(',', '')) // int(get_price()))))
                        await message.channel.send("inflateable T-Rex costumes with")
                        await message.channel.send(x)
                        await message.channel.send("from Party City! (!dinolink for link)")
                    else:
                        await message.channel.send(msg)

        if '!dinolink' in tmpmessage:
            await message.channel.send(
                "Here you go: https://www.partycity.com/adult-inflatable-t-rex-dinosaur-costume---jurassic-world-P636269.html")

        # if 'how long til gameday' in tmpmessage:
        #     for x in gamedays:
        #         if gamedays.get(x).date == datetime.today():
        #             await message.channel.send(
        #                 "It's GAMEDAY for " + gamedays.get(x).band + " band! Beat " + gamedays.get(x).opponent + '!')
        #             break
        #         if (gamedays.get(x).date - datetime.today()).days > 0:
        #             await message.channel.send("It is " + str(
        #                 (gamedays.get(x).date - datetime.today()).days) + " days until gameday for " + gamedays.get(
        #                 x).band + " band. We will play " + gamedays.get(x).opponent)
        #             break

        if ('!talk' in tmpmessage) and ('!generatememe' not in tmpmessage):
            await message.channel.send(get_mt())

        if '!help' in tmpmessage:
            user = client.get_user(message.author.id)
            await message.channel.send("Check your DMs! :mailbox_with_mail: :eyes:")
            embed = discord.Embed(type="rich",
                                  title="CarichnerBot Help",
                                  description="Hi there, I'm **CarichnerBot**! A lot of what I do is respond to certain keywords or react to certain messages, but I do have some commands:\n\n"
                                              "• `!help`: Shows this message.\n"
                                              "• `!talk`: Generates a string of gibberish using Markov Chains. *Disclaimer: may be inappropriate at times. If this says something you don't like, please mention @ mod.*\n"
                                              "• `!generatememe <text>`: This generates a meme with whatever image you attach to your message, along with whatever text you provide it. If you do not provide an image, the last image sent in the main server will be used. You can mention a user before your text to use their profile picture as the image. If you replace the text with `!talk` or `!random`, output from the `!talk` command will be put in place of the text.\n"
                                              "• `!stats`: Shows the uptime and memory usage for the bot.\n"
                                              "• `!date`: Displays the current date and time.\n"
                                              "• `!ping`: Shows the current ping for the bot.\n"
                                              "• `!avatar`: Displays the avatar for any users you mention along with this command. Ex: `!avatar @User`\n"
                                              "• `!dinolink`: Displays the link for the Party City dino costume.\n"
                                              "• `!mute`: Mutes the bot responses for 15 minutes expect for explicit '!' commands.\n"
                                              "• `!stop`: Sends the infamous 'stop.png'.\n"
                                              "• `!weather`: Gets the current weather.\n"
                                              "• `!forecast`: Gets the weather prediction for today at 5pm.")
            await user.send(embed=embed)

        if '!stats' in tmpmessage:
            p = subprocess.Popen("uptime", stdout=subprocess.PIPE, shell=True)
            (output, _) = p.communicate()
            await message.channel.send("Uptime: `" + str(output)[3: -3] + "`")
            process = psutil.Process(os.getpid())
            await message.channel.send("Memory: `" + str(process.memory_info().rss / float(1000000)) + " mb`")

        if '!date' in tmpmessage:
            p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
            (output, _) = p.communicate()
            await message.channel.send("`" + str(output)[2: -3] + "`")

        if '!ping' in tmpmessage:
            await message.channel.send("Pong! (`" + str(round(client.latency, 3)) + " s`)")

        if '!avatar' in tmpmessage:
            if len(message.mentions) > 0:
                for mentioned in message.mentions:
                    await message.channel.send(mentioned.avatar_url)
            else:
                await message.channel.send("No mentioned users!")

        if '!stop' in tmpmessage:
            await message.channel.send(file=discord.File("res/stop.png"))

        if '!restart' in tmpmessage:
            if await authorize(message):
                await message.channel.send("Be back soon (hopefully)!")
                print('Shutting down')
                print('------')
                sys.exit()

        if '!mute' in tmpmessage:
            if not client.mute:
                await mute(message)
            else:
                await message.channel.send("I've already been muted!")

    except Exception:
        await message.channel.send("Oh no, I threw an error! <@262043915081875456>")
        await message.channel.send("```" + get_exception() + "```")
        print(get_exception())


if not os.path.exists('upload'):
    os.mkdir('upload')

client.run(TOKEN)
