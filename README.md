# Band Bot

## About
Band Bot is a simple ping-pong style Discord bot that responds to a set of commands and phrases. This bot can also react to messages when certain phrases are said, as well as generate meme images and random text chats.

## Purpose
This bot was written specifically for a Discord server for members of the ISUCF'V'MB at Iowa State University. The bot's main purpose is to provide easy access to important information and links to aid members with being prepared and ready to go for rehearsals and performances. The bot also acts as a means of entertainment with the meme generator and random text function.

## Usage
### Commands
* `!help`: Sends help message to user, or displays help for a specific command.
* `!talk`: Generates a string of gibberish using Markov Chains. *Disclaimer: may be inappropriate at times. If this says something you don't like, please mention @ mod.*
* `!generatememe <text>`: This generates a meme with whatever image you attach to your message, along with whatever text you provide it. If you do not provide an image, the last image sent in the main server will be used. You can mention a user before your text to use their profile picture as the image. If you replace the text with `!talk` or `!random`, output from the `!talk` command will be put in place of the text.
* `!stats`: Shows the uptime and memory usage for the bot.
* `!date`: Displays the current date and time.
* `!ping`: Shows the current ping for the bot.
* `!avatar`: Displays the avatar for any users you mention along with this command. Ex: `!avatar @User`
* `!mute`: Mutes the bot responses for a certain time based on the config.
* `!stop`: Sends the infamous 'stop.png'.
* `!boxlink`: Provides a link to the Box.
* `!weather`: Gets the current weather.
* `!forecast`: Gets the weather prediction for today at 5pm.

### Other
Band Bot can react or respond to certain phrases said in server text channels. It also has custom now playing statuses that show for specified amounts of time based on the length set per item.

## Configuration
You will need to add your own `config.py` if you would like to clone this repo and test yourself. The file must include:
* `TOKEN`: This is the token that you get when you create your bot. To see how to create your own bot and how to find your token, check out [this tutorial](https://discordpy.readthedocs.io/en/latest/discord.html).
* `weatherUrl` and `forecastUrl`: These links can be obtained after creating an account on [openweathermap](https://openweathermap.org/api) and generating api links for **Current Weather Data** and also **One Call API** (respective to `weatherUrl` and `forecastUrl`).
* `mtUrl`: This is an API that was shared with me and don't feel super confortable handing out, but if you really need it, let me know and I can get it to you.
* `box_link`: A link to the band's Box page.

## Contributing
If you wish to contribute to this project, please fork the repo, create a new feature branch, and make your commits. After you are finished, make a pull request to the main branch of the original repo.
