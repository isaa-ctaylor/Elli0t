import os
from utils.bot import bot
from dotenv import load_dotenv

load_dotenv()

bot.loop.run_until_complete(bot.load_cogs())


@bot.event
async def on_ready():
    '''
    Called when the client is done preparing the data received from Discord. Usually after login is successful and the Client.guilds and co. are filled up.
    '''

    print("Bot is connected to discord.")


bot.run(os.getenv("TOKEN"))