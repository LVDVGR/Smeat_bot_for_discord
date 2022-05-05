import discord
from discord.ext import commands
from config import settings
from hello import hello_phrases
import random

bot = commands.Bot(command_prefix = settings['prefix'])

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    hello_index = random.randrange(0, 14)
    hi = hello_phrases[hello_index]
    await ctx.send(f'{hi}, {author.mention}!')

bot.run(settings['token'])

