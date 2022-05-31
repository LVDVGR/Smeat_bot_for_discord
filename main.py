import audioop
import json
import requests
import discord
from discord.ext import commands
from config import settings
from hello import hello_phrases, shift_alt_phrase
import random
from youtube_dl import YoutubeDL
import time
from asyncio import sleep
from Templates import *


FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
               'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
bot = commands.Bot(command_prefix = settings['prefix'])

server = None
musical_queue = []



#-------------------------------------------------------------hello------------------------------------
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
async def руддщ(ctx):
    author = ctx.message.author
    check = ctx.message.content
    s = str(check)
    s = check.replace('Smeat ', '', 1)
    print(s)
    hello_index = random.randrange(0, 14)
    hi = hello_phrases[hello_index]
    await ctx.send(f'{hi}, {author.mention}!')
    shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
    shift = shift_alt_phrase[shiftAlt_index]
    await ctx.send(shift)
#----------------------------------------------------------------------------------------------------------






#-----------------------------------------------------------play---------------------------------------


def with_youtube(url):
    with YoutubeDL(YDL_OPTIONS) as ydl:

        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f'ytsearch: {url} ', download=False)['entrise'][0]

    url = info['formats'][0]['url']
    return url


def play_music(ctx, url):
    url = with_youtube(url)
    vc.play(discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source=url, **FFMPEG_OPTIONS))


@bot.command()
async def play(ctx, url):
    global vc
    musical_queue.append(url)
    print(musical_queue)
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        while vc.is_playing():
            await sleep(1)
        play_music(ctx, musical_queue[0])
        musical_queue.pop(0)
    else:
        play_music(ctx, musical_queue[0])
        musical_queue.pop(0)

@bot.command()
async def здфн(ctx, url):
    global vc
    musical_queue.append(url)
    print(musical_queue)
    try:
        voice_channel = ctx.message.author.voice.channel
        vc = await voice_channel.connect()
    except:
        print('Уже подключен или не удалось подключиться')

    if vc.is_playing():
        while vc.is_playing():
            await sleep(1)
        play_music(ctx, musical_queue[0])
        musical_queue.pop(0)
        print(musical_queue)
    else:
        play_music(ctx, musical_queue[0])
        musical_queue.pop(0)
        print(musical_queue)
#------------------------------------------------------------------------------------------------------------





#-----------------------------------------------add_song------------------------------------------------------
@bot.command()
async def add_playlist1(ctx, url):
    try:
        new_song = with_youtube(url)
        playlist1.append(new_song)
        await ctx.channel.send(f'Трек добавлен.')
        print(playlist1)

    except:

        await ctx.channel.send(f'{ctx.author.mention}, плейлист не найден!')
        await ctx.channel.send(f'Есть вероятность, что название плейлиста было написано не верно.')
#-------------------------------------------------------------------------------------------------------------




#---------------------------------------------------leave-----------------------------------------------------
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
async def дуфму(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice is None:
        await ctx.channel.send(f'{ctx.author.mention}, меня тут и не было!')
    else:
        await voice.disconnect()
#----------------------------------------------------------------------------------------------------------




#-------------------------------------------------stop---------------------------------------------------
@bot.command()
async def stop(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice.is_playing():
        await voice.pause()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, уже остановлено.')
#----------------------------------------------------------------------------------------------------------




#-------------------------------------------------------------resume------------------------------------
@bot.command()
async def resume(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, уже остановлено.')

async def куыгьу(ctx):
    global server
    server = ctx.guild
    voice = discord.utils.get(bot.voice_clients, guild = server)

    if voice.is_paused():
        await voice.resume()
    else:
        await ctx.channel.send(f'{ctx.author.mention}, уже остановлено.')
#----------------------------------------------------------------------------------------------------------





#-------------------------------------------------------volume--------------------------------------------
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
#----------------------------------------------------------------------------------------------------------




#----------------------------------------------show---------------------------------------------------
@bot.command()
async def show(ctx, search):
    new_search = str(search)
    url = 'https://some-random-api.ml/img/' + search
    response = requests.get(url)
    json_data = json.loads(response.text)

    embed = discord.Embed(color = 0xff9900, title = f'Random {new_search}')
    embed.set_image(url = json_data['link'])
    await ctx.send(embed = embed)
#----------------------------------------------------------------------------------------------------------





bot.run(settings['token'])
