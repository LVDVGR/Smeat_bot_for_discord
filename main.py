import audioop
import json
import requests
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
async def stop(ctx):
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
        await ctx.channel.send(f'{ctx.author.mention}, уже остановлено.')



@bot.command()
async def volume(ctx, vol):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.author.voice.channel
    vol_new = int(vol)
    if voice and voice.is_connected():
        if 1 <= vol_new <= 200:
            voice.source = discord.PCMVolumeTransformer(
                voice.source, vol_new / 100)
            await ctx.send(f"Громкость увеличена в {vol_new / 100}.")
        else:
            await ctx.send("Недопустимый диапазон значений.")
    else:
        await ctx.send("Я не нахожусь в войс канале.")


@bot.command()
async def show(ctx, search):
    new_search = str(search)
    url = 'https://some-random-api.ml/img/' + search
    response = requests.get(url)
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0xff9900, title = f'Random {new_search}')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)


bot.run(settings['token'])

