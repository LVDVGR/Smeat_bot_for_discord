import audioop

import discord
from discord.ext import commands
from config import settings
from hello import hello_phrases
import random
from youtube_dl import YoutubeDL
import time

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
bot = commands.Bot(command_prefix = settings['prefix'])

server = None

def recharge(music):
    music = False
    return music

@bot.command()
async def hello(ctx):
    author = ctx.message.author
    check = ctx.message.content
    s = str(check)
    s = check.replace('Smeat ', '', 1)
    print(s)
    hello_index = random.randrange(0, 14)
    hi = hello_phrases[hello_index]
    await ctx.send(f'{hi}, {author.mention}!')

@bot.command()
async def play(ctx, url):
    vc = await ctx.message.author.voice.channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=server)

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f'ytsearch: {url} ', download=False)['entrise'][0]

    url = info['formats'][0]['url']
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))



@bot.command()
async def leave(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice is None:
        await ctx.channel.send(f'{ctx.author.mention}, меня тут и не было!')
    else:
        await voice.disconnect()

@bot.command()
async def stoping(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, уже остановлено.')

@bot.command()
async def resume(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, мелодия уже на паузе.')

print()









bot.run(settings['token'])

