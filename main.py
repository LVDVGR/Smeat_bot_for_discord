import discord
from discord.ext import commands
from config import settings
from hello import hello_phrases
import random
from youtube_dl import YoutubeDL

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
bot = commands.Bot(command_prefix = settings['prefix'])

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

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f'ytsearch: {url} ', download=False)['entrise'][0]

    url = info['formats'][0]['url']

    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))






bot.run(settings['token'])

