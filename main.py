import discord
from discord.ext import commands
from config import settings

bot = commands.Bot(command_prefix = settings['prefix'])

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f'Привет, {author.mention}!')

bot.run(settings['token'])