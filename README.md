# band-bot

Hi there, I'm **CarichnerBot**! A lot of what I do is respond to certain keywords or react to certain messages, but I do have some commands:

`!help`: Shows this message.
`!talk`: Generates a string of gibberish using Markov Chains. *Disclaimer: may be inappropriate at times. If this says something you don't like, please mention Slav.*
`!generatememe`: This generates a meme with whatever image you attach to your message, along with whatever text you provide it. For example, you can do `!generatememe Meme Text Here`, and it will generate a meme with that text at the bottom of your image.
Options:
* Adding `!talk` or `!random` produces gibberish for the meme text, the same from the `!talk` command. Ex: `!generatememe !talk`
* Mention someone to use their profile picture for the picture! Ex: `!generatememe @Someome *meme text here*`
* If you don't attach an image with `!generatememe`, it will use the last picture that was sent as the background. With this, you can essentially re-meme other peoples memes! Or, if someone posts a pic you know a funny caption for, just use `!generatememe *meme text here*`!
`!uptime`: Shows the uptime for the bot.
`!date`: Displays the current date and time.
`!ping`: Shows the current ping for the bot.
`!avatar`: Displays the avatar for any users you mention along with this command. Ex: `!avatar @User`

# Config

You will need to add your own `config.py` file if you would like to clone this repo and test yourself. The file must include the following:
* `TOKEN`: This is the token that you get when you create your bot. To see how to create your own bot and how to find your token, check out [this tutorial](https://discordpy.readthedocs.io/en/latest/discord.html).
* `weatherUrl` and `forecastUrl`: These links can be obtained after creating an account on [openweathermap](https://openweathermap.org/api) and generating api links for **Current Weather Data** and also **One Call API** (respective to `weatherUrl` and `forecastUrl`).
* `mtUrl`: This is an API that I shared and don't feel super confortable handing out, but if you really need it, let me know and I can get it to you.

# Bot Dev Discord server

To prevent spam of the actual server this bot is used in, please do all testing of the bot in our testing server. Join [here](https://discord.gg/JXue2md)!
