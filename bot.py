from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageColor
from discord.utils import get
from wordfilter import Wordfilter
from discord.ext import commands

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
import re

TOKEN = config.TOKEN
BOX_LINK = config.box_link
MUTE_TIME = 14
COOLDOWN = 2
BAND_SERVER = 743519350501277716
TEST_SERVER = 746851271901708428
MESSAGES_CHANNEL = 784197374959943731

weatherUrl = config.weatherUrl
forecastUrl = config.forecastUrl
mtUrl = config.mtUrl
timeFormat = "%A %I:%M%p"
intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)
client.agreeCounter = 0
wordfilter = Wordfilter()
wordfilter.clearList()
wordfilter.addWords(config.banned_words)
client.last_response_time = datetime.now() - timedelta(minutes=COOLDOWN + 1)
client.mutedTime = datetime.now() - timedelta(minutes=MUTE_TIME + 1)
client.prev_dm_user = None


class GameDay:
    def __init__(self, opponent, date):
        self.opponent = opponent
        self.date = date


gamedays = {
    1: GameDay('University of Northern Iowa', datetime(2021, 9, 4)),
    2: GameDay('University of Iowa', datetime(2021, 9, 11)),
    3: GameDay('Kansas', datetime(2021, 10, 2)),
    4: GameDay('Oklahoma State', datetime(2021, 10, 23)),
    5: GameDay('Texas', datetime(2021, 11, 6)),
    6: GameDay('TCU', datetime(2021, 11, 26))
}


async def change_status():
    """Occasionally changes the status of the bot."""
    while True:
        if ((datetime.now().hour == 17) or ((datetime.now().hour == 18)
                                            and (datetime.now().minute == 30))) and (datetime.now().weekday() < 5):
            await client.change_presence(
                activity=discord.Activity(name='band rehearsal', type=discord.ActivityType.watching))
            await asyncio.sleep(5100)
        else:
            song = random.choice(lists.songs)
            await client.change_presence(activity=discord.Game(name=song.title))
            await asyncio.sleep(song.length)

        # song = random.choice(lists.songs)
        # await client.change_presence(activity=discord.Game(name=song.title))
        # await asyncio.sleep(song.length)


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


def get_mt():
    """Gets a string of random text from the MT API continuously until it finds a string that passes the word filter."""
    while True:
        text = requests.get(mtUrl).json()['data']
        if not wordfilter.blacklisted(text):
            break
    return text


def get_forecast():
    """Gets the forecast for today at 5pm."""
    forecast = requests.get(forecastUrl).json()
    hourly = forecast['hourly']
    ms = ''
    for hour in hourly:
        timestamp = datetime.fromtimestamp(hour['dt'])
        if timestamp.hour == 17:
            temp = str(round((hour['temp'] - 273.15) * 9.0 / 5 + 32, 1))
            ms += f'On {timestamp.strftime(timeFormat)} it will be {temp} °F with a '
            ms += hour['weather'][0]['description'] + '\n'
            ms += 'Looks like a GREAT day for a band rehearsal!'
            return ms


def get_exception():
    """Handling thrown exception from bot."""
    _, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)


async def handle_roles(payload: discord.RawReactionActionEvent, adding):
    """Handles adding/removing roles to/from users."""
    guild = client.get_guild(payload.guild_id)
    roles = guild.roles
    member = guild.get_member(payload.user_id)
    emoji = str(client.get_emoji(payload.emoji.id))
    for react in lists.reacts:
        if emoji == lists.reacts[react][1] or payload.emoji.name == lists.reacts[react][1]:
            role = get(roles, id=lists.reacts[react][0])
            if adding:
                await member.add_roles(role)
            else:
                await member.remove_roles(role)


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
    guild = client.get_guild(BAND_SERVER)
    for guildMember in guild.members:
        if guildMember == member:
            found = True
            break
    if not found:
        return
    guild = client.get_guild(TEST_SERVER)
    for guildMember in guild.members:
        if guildMember == member:
            return
            # If the member exists in both servers, don't send the welcome message
            # THIS CREATES AN EDGE CASE where if the user joined another server that this bot is in before joining the band server it won't send the message.
            # However I cannot foresee a way to fix this edge case, and the probability of this happening is very low anyways, so I'm not going to worry about it
    embed = discord.Embed(title="Welcome! :wave:",
                          description=f"Hello {member.name}, and welcome to the I.S.U.C.F.V.M.B. server! This is just a place for us to all hang out together, exchange memes, and have fun! Here are the rules for the server:\n\n"
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
        if message.author == client.user or "youtu.be" in message.content:
            return

        tmpmessage = message.content.lower()

        in_main_server = not isinstance(message.channel, discord.DMChannel) and message.channel.guild.id == BAND_SERVER

        if isinstance(message.channel, discord.DMChannel):  # If we are being sent a DM, relay this to our server
            try:
                if message.author.id in config.blockedUsers:
                    await message.channel.send("Sorry, but you are blacklisted from sending messages!")
                    return
            except AttributeError:
                print("Missing `blockedUsers` list in `config.py`.")
            channel = client.get_channel(MESSAGES_CHANNEL)
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

        if message.channel.id == MESSAGES_CHANNEL:  # Responding to the previous user's DM
            if client.prev_dm_user is None:
                return
            if len(message.content) > 0:
                await client.prev_dm_user.send(content=message.content)
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    await client.prev_dm_user.send(content=attachment.url)

        if (len(message.attachments) > 0) and in_main_server:
            # Open image, convert to jpg and save as previmg.jpg, but only if from the main server.
            filename = message.attachments[0].filename.lower()
            # Check to see that we're actually saving an image
            if (filename[-3:] == 'jpg') or (filename[-3:] == 'png') or (filename[-4:] == "jpeg"):
                await message.attachments[0].save(f"upload/{filename}")
                image = Image.open(f"upload/{filename}")
                if (image.format == "JPG") or (image.format == "PNG") or (image.format == "JPEG"):
                    image.convert("RGB").save('upload/previmg.jpg')
                    os.remove(f"upload/{filename}")

        if in_main_server and not tmpmessage.startswith('!'):
            channel_id = message.channel.id
            # Prevent bot responding to messages in these channels:
            if channel_id in lists.valid_channels:
                return

        if ((datetime.now() - client.last_response_time) > timedelta(minutes=COOLDOWN)) and \
           (datetime.now() - client.mutedTime > timedelta(minutes=MUTE_TIME)):
            for key in lists.responses.keys():
                regex = re.findall(f"\\b{key}\\b", tmpmessage)
                if len(regex) > 0:
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
            await message.channel.send(f'Box link: {BOX_LINK}')

        if 'carichnerbot' in tmpmessage:
            if 'love' in tmpmessage:
                await message.channel.send(f'I love you too, <@{str(message.author.id)}> :heart:')
            elif ('hello' in tmpmessage) or ('hi' in tmpmessage):
                await message.channel.send(f'Hello <@{str(message.author.id)}>')

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
           ("is today a great day for band" in tmpmessage):
            async with message.channel.typing():
                forecast = get_forecast()
            await message.channel.send(forecast)

        if 'how long until gameday' in tmpmessage:
            for x in gamedays:
                if gamedays.get(x).date == datetime.today():
                    await message.channel.send(
                        "It's GAMEDAY for " + gamedays.get(x).band + " band! Beat " + gamedays.get(x).opponent + '!')
                    break
                if (gamedays.get(x).date - datetime.today()).days > 0:
                    await message.channel.send("It is " + str(
                        (gamedays.get(x).date - datetime.today()).days) + " days until gameday. We will play " + gamedays.get(x).opponent + '.')
                    break

    except Exception:
        await message.channel.send("Oh no, I threw an error! <@262043915081875456>")
        await message.channel.send("```" + get_exception() + "```")
        print(get_exception())

    await client.process_commands(message)


if not os.path.exists('upload'):
    os.mkdir('upload')


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.command(brief="Generates a meme with input text.")
    async def generatememe(self: discord.ext.commands.Context, *, arg=None):
        """
        Usage: `generatememe (optional @User) (optional meme text | !talk | !random)`

        Generates a meme with whatever image you attach to your message, along with whatever text you provide it. If you do not provide an image, the last image sent in the server will be used. You can mention a user before your text to use their profile picture as the image. If you replace the text with `!talk` or `!random`, output from the `!talk` command will be put in place of the text.
        """
        async with self.typing():
            if len(self.message.attachments) > 0:  # If the user included an image
                filename = "upload/" + self.message.attachments[0].filename
                await self.message.attachments[0].save(filename)
                image = Image.open(filename).convert('RGB')
                skip = 0
            elif len(self.message.mentions) > 0:  # If the user mentioned someone
                filename = 'upload/avatarimg.jpg'
                await self.message.mentions[0].avatar_url.save('tmp.webp')
                image = Image.open('tmp.webp').convert('RGB')
                image.save(filename, "jpeg")
                os.remove("tmp.webp")
                image = Image.open(filename)
                skip = 22
            else:  # If the user did not mention or include an image, use the previous image seen by the bot.
                filename = 'upload/prevmeme.jpg'
                image = Image.open('upload/previmg.jpg')  # Should already be converted
                image.save(filename)
                skip = 0
            font = ImageFont.truetype('impact.ttf', size=30)

            # Want max width or height of the image to be = 400
            maxsize = 400
            largest = max(image.size[0], image.size[1])
            scale = maxsize / float(largest)
            resize = image.resize((int(image.size[0] * scale), int(image.size[1] * scale)))
            if (not isinstance(self.message.channel, discord.DMChannel)) and (self.message.guild.id == BAND_SERVER):
                resize.save('upload/previmg.jpg',
                            "jpeg")  # So people can make memes from other memes, but only if from the main server.
            padding = (resize.size[0] * 0.1)  # 10% left boundary

            if arg is not None:
                if ('!random' in arg) or ('!talk' in arg):
                    text = get_mt()
                else:
                    text = arg[skip:]
            else:
                text = ""
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
        await self.send(file=discord.File(filename))
        os.remove(filename)

    @client.command(brief="Generates a string of gibberish using Markov Chains.")
    async def talk(self: discord.ext.commands.Context):
        """Generates a string of gibberish using Markov Chains. *Disclaimer: may be inappropriate at times. If this says something you don't like, please mention @mod.*"""
        async with self.typing():
            message = get_mt()
        await self.send(message)

    @client.command(brief="Sends help message.")
    async def help(self, *args):
        """
        Usage: `!help (optional command | commands)`

        Sends help message to user, or displays help for a specific command.
        """
        if len(args) == 0:
            await self.send("Check your DMs! :mailbox_with_mail: :eyes:")
            description = "Hi there, I'm **CarichnerBot**! A lot of what I do is respond to certain keywords or react to certain messages, but I do have some commands:\n\n"
            for command in client.commands:
                description += f"• `!{command.name}`: {command.brief if command.brief is not None else command.help}\n"
            embed = discord.Embed(type="rich", title="CarichnerBot Help", description=description)
            await self.author.send(embed=embed)
        else:
            for arg in list(set([i for i in args])):
                try:
                    description = getattr(Commands, arg).help
                    embed = discord.Embed(type="rich",
                                          title=arg,
                                          description=description)
                    await self.send(embed=embed)
                except AttributeError:
                    await self.send(f"`{arg}` doesn't appear to be a command, sorry!")

    @client.command()
    async def forecast(self: discord.ext.commands.Context):
        """Gets the weather prediction for today at 5pm."""
        async with self.typing():
            forecast = get_forecast()
        await self.send(forecast)

    @client.command()
    async def weather(self: discord.ext.commands.Context):
        """Gets the current weather."""
        async with self.typing():
            weather = requests.get(weatherUrl).json()
            temp = str(round((weather['main']['temp'] - 273.15) * 9.0 / 5 + 32, 1))
            ms = 'It is currently ' + temp + '°F with a '
            ms += weather['weather'][0]['description']
        await self.send(ms)

    @client.command()
    async def stats(self: discord.ext.commands.Context):
        """Shows the uptime and memory usage for the bot."""
        p = subprocess.Popen("uptime", stdout=subprocess.PIPE, shell=True)
        (output, _) = p.communicate()
        await self.send(f"Uptime: `{str(output)[3: -3]}`")
        process = psutil.Process(os.getpid())
        await self.send(f"Memory: `{str(process.memory_info().rss / float(1000000))} mb`")

    @client.command()
    async def date(self: discord.ext.commands.Context):
        """Displays the current date and time."""
        p = subprocess.Popen("date", stdout=subprocess.PIPE, shell=True)
        (output, _) = p.communicate()
        await self.send("`" + str(output)[2: -3] + "`")

    @client.command()
    async def ping(self: discord.ext.commands.Context):
        """Shows the current ping for the bot."""
        await self.send(f"Pong! (`{str(round(client.latency, 3))} s`)")

    @client.command(brief="Displays the avatar for any users you mention.")
    async def avatar(self: discord.ext.commands.Context):
        """
        Usage: `!avatar (optional @User(s))`

        Displays the avatar for any users you mention.
        """
        if len(self.message.mentions) > 0:
            for mentioned in self.message.mentions:
                await self.send(mentioned.avatar_url)
        else:
            await self.send(self.author.avatar_url)

    @client.command()
    async def stop(self: discord.ext.commands.Context):
        """Sends the infamous 'stop.png'."""
        await self.send(file=discord.File("res/stop.png"))

    @client.command(brief=f"Mutes responses for {str(MUTE_TIME + 1)} minute{'s' if MUTE_TIME > 1 else ''}.", help=f"Mutes the bot responses for {str(MUTE_TIME + 1)} minute{'s' if MUTE_TIME > 1 else ''} except for explicit commands.")
    async def mute(self: discord.ext.commands.Context):
        """Mutes the bot responses for a certain time based on the config."""
        if datetime.now() - client.mutedTime > timedelta(minutes=MUTE_TIME):
            await self.send(f"Okay! For the next {str(MUTE_TIME + 1)} minute{'s' if MUTE_TIME > 1 else ''} I will only respond to explicit commands (starting with '!').")
            client.mutedTime = datetime.now()
            await self.send(f"I will be back at {(client.mutedTime + timedelta(minutes=MUTE_TIME + 1)).strftime('%I:%M %p').lstrip('0')}.")
        else:
            await self.send(f"I've already been muted! I'll be back at {(client.mutedTime + timedelta(minutes=MUTE_TIME + 1)).strftime('%I:%M').lstrip('0')}")

    @client.command()
    @commands.has_role(750486445105479702)
    async def restart(self: discord.ext.commands.Context):
        """Restarts the bot, given the user has the correct role."""
        await self.send("Be back soon (hopefully)!")
        print('Shutting down')
        print('------')
        sys.exit()

    @client.command(brief="Generates the react message embed for users to grant themselves roles for sections or colleges.")
    @commands.has_role(750486445105479702)
    async def reactRoles(self: discord.ext.commands.Context, arg):
        """
        Usage: `!reactRoles section|college`

        Generates the react message embed for users to grant themselves roles for sections or colleges.
        """
        if arg not in ["section", "college"]:
            await self.send("Looks like you're missing `section` or `college` from your arguments. Try again!")
        else:
            description = f"React to this message with which {arg} you're in!\n\n"

            if arg == "section":
                specifiedList = lists.sections
            else:
                specifiedList = lists.colleges
            for item in specifiedList:
                description += f"{specifiedList[item][1]} : {item}\n"
            embed = discord.Embed(type="rich",
                                  title=arg.capitalize(),
                                  description=description)
            message = await self.send(embed=embed)
            for item in specifiedList:
                await message.add_reaction(specifiedList[item][1])

    @client.command()
    async def boxlink(self: discord.ext.commands.Context):
        """Provides a link to the Box."""
        await self.send(BOX_LINK)

    @client.command()
    async def schedule(self: discord.ext.commands.Context):
        """Lists the schedule of games."""
        message = ""
        for gameNum in gamedays:
            try:
                if datetime.now() > gamedays[gameNum].date:
                    message += "~~• " + gamedays[gameNum].date.strftime("%b %-d") + ": " + gamedays[gameNum].opponent + "~~\n"
                else:
                    message += "• " + gamedays[gameNum].date.strftime("%b %-d") + ": " + gamedays[gameNum].opponent + "\n"
            except ValueError:
                if datetime.now() > gamedays[gameNum].date:
                    message += "~~• " + gamedays[gameNum].date.strftime("%b %#d") + ": " + gamedays[gameNum].opponent + "~~\n"
                else:
                    message += "• " + gamedays[gameNum].date.strftime("%b %#d") + ": " + gamedays[gameNum].opponent + "\n"
        await self.send(message)

    @client.event
    async def on_command_error(self: discord.ext.commands.Context, error):
        """Global command error handler."""
        if isinstance(error, discord.ext.commands.MissingRole):
            await self.send("Oops, it looks like you don't have the correct role for running this!")
        else:
            await self.send(error)

    @client.event
    async def on_raw_reaction_add(self: discord.RawReactionActionEvent) -> None:
        if self.user_id == 746841518672969779 or self.channel_id != lists.react_channel:
            return
        print(self)  # For debugging purposes in case this breaks again
        await handle_roles(self, True)

    @client.event
    async def on_raw_reaction_remove(self: discord.RawReactionActionEvent) -> None:
        if self.user_id == 746841518672969779 or self.channel_id != lists.react_channel:
            return
        print(self)  # For debugging purposes in case this breaks again
        await handle_roles(self, False)


client.run(TOKEN)
