import audioop
import json
import requests
import discord
from discord.ext import commands
from config import settings
from hello import hello_phrases, shift_alt_phrase, get_help_txt
import random
from youtube_dl import YoutubeDL
import time
from asyncio import sleep
from pytube import Search, YouTube, Playlist
from Templates import *



FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
                   'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}



intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True

bot = commands.Bot(command_prefix = settings['prefix'], intents=intents)

server = None
musical_queue = []
songs_titles = []


    #-------------------------------------------------------------hello------------------------------------
@bot.command()
async def hello(ctx):
        author = ctx.message.author
        check = ctx.message.content
        s = str(check)
        s = check.replace('Smeat ', '', 1)      # создание текста сообщения рандомом
        print(s)                                # Создание рамки, где ее цвет указывается в color, а текст в description
        hello_index = random.randrange(0, 14)
        hi = hello_phrases[hello_index]
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{hi}, {author.mention}!')
        await ctx.send(embed=embed)

@bot.command()
async def руддщ(ctx):
        author = ctx.message.author
        check = ctx.message.content
        s = str(check)
        s = check.replace('Smeat ', '', 1)
        print(s)
        hello_index = random.randrange(0, 14)
        hi = hello_phrases[hello_index]

        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{hi}, {author.mention}!')
        await ctx.send(embed=embed)

        shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
        shift = shift_alt_phrase[shiftAlt_index]

        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{shift}')
        await ctx.send(embed=embed)
    #----------------------------------------------------------------------------------------------------------






    #-----------------------------------------------------------play---------------------------------------


def with_youtube(url):
        with YoutubeDL(YDL_OPTIONS) as ydl:

            if 'https:' in url:
                info = ydl.extract_info(url, download=False)
            else:
                info = ydl.extract_info(f'ytsearch: {url} ', download=False)['entrise'][0]

        url = info['formats'][0]['url']
        return url


def play_music(ctx, url):
        url = with_youtube(url)
        vc.play(discord.FFmpegPCMAudio(executable=settings['ffmpeg_path'], source=url, **FFMPEG_OPTIONS))


@bot.command()
async def play(ctx, url, p_r='', p_r1='', p_r2='', p_r3='', p_r4='', p_r5='', p_r6='', p_r7='', p_r8='', p_r9='', p_r10=''):
        name = ''

        if 'https:' in url:

            try:
                plist = Playlist(url)
                for url_playlists in plist.video_urls:
                    try:
                        yt = YouTube(url_playlists)
                        songs_titles.append(yt.title)
                        musical_queue.append(url_playlists)
                    except:
                        print('lose')
            except:
                yt = YouTube(url)
                songs_titles.append(yt.title)
                musical_queue.append(url)


        else:
            search_request = url + ' ' + p_r + ' ' + p_r1 + ' ' + p_r2 + ' ' + p_r3 + ' ' + p_r4 + ' ' +\
                             p_r5 + ' ' + p_r6 + ' ' + p_r7 + ' ' + p_r8 + ' ' + p_r9 + ' ' + p_r10
            s_request = Search(search_request)
            for getting_url in s_request.results:
                url = getting_url.watch_url
                name = getting_url.title
                musical_queue.append(url)
                songs_titles.append(name)
                break

        global vc

        embed = discord.Embed(color=discord.Color.dark_red(),
                              description=f'Трек {name} \nнаходится на позиции {len(musical_queue) + 1}',
                              title='МУЗИКАЛ КВЕВЕ /"V"\ ')

        await ctx.send(embed=embed)

        try:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
        except:
            print('Уже подключен или не удалось подключиться')


        for temp in range (len(musical_queue)):
            try:
                if vc.is_playing():
                    ctx.message.author.voice.channel.connect()
                    while vc.is_playing():
                        await sleep(1)
                    play_music(ctx, musical_queue[0])

                    embed = discord.Embed(color=discord.Color.dark_red(),
                                          description=f'{songs_titles[0]}',
                                          title='Сейчас играет /owo\ ')
                    await ctx.send(embed=embed)

                    musical_queue.pop(0)
                    songs_titles.pop(0)
                else:
                    play_music(ctx, musical_queue[0])
                    musical_queue.pop(0)
                    songs_titles.pop(0)
            except:
                pass

@bot.command()
async def здфн(ctx, url, p_r='', p_r1='', p_r2='', p_r3='', p_r4='', p_r5='', p_r6='', p_r7='', p_r8='', p_r9='', p_r10=''):

        name = ''

        shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
        shift = shift_alt_phrase[shiftAlt_index]
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{shift}')
        await ctx.send(embed=embed)

        if 'https:' in url:
            yt = YouTube(url)
            name = yt.title
        else:
            search_request = url + ' ' + p_r + ' ' + p_r1 + ' ' + p_r2 + ' ' + p_r3 + ' ' + p_r4 + ' ' +\
                             p_r5 + ' ' + p_r6 + ' ' + p_r7 + ' ' + p_r8 + ' ' + p_r9 + ' ' + p_r10
            s_request = Search(search_request)
            for getting_url in s_request.results:
                url = getting_url.watch_url
                name = getting_url.title
                break

        global vc
        try:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
        except:
            print('Уже подключен или не удалось подключиться')

        musical_queue.append(url)
        songs_titles.append(name)
        print(musical_queue)

        embed = discord.Embed(color=discord.Color.dark_red(),
                              description=f'Трек {name} \nнаходится на позиции {len(musical_queue) + 1}',
                              title='МУЗИКАЛ КВЕВЕ /"V"\ ')

        await ctx.send(embed=embed)

        if vc.is_playing():
            while vc.is_playing():
                await sleep(1)
            play_music(ctx, musical_queue[0])
            musical_queue.pop(0)
            songs_titles.pop(0)
            print(musical_queue)
        else:
            play_music(ctx, musical_queue[0])
            musical_queue.pop(0)
            songs_titles.pop(0)
            print(musical_queue)
    #------------------------------------------------------------------------------------------------------------

@bot.command()
async def queue(ctx):
    curr = 1
    songs_list = ''

    for song in songs_titles:
        songs_list += f'{curr}. {str(song)} \n'
        curr += 1

    # embed = discord.Embed(color=discord.Color.dark_red(),
    #                       description=f'{songs_list}',
    #                       title='Список треков в очереди:')
    #
    # await ctx.send(embed=embed)
    await ctx.send('Cписок треков(большая рамочка не вывозит большие списки, но я это исправлю!!)')
    await ctx.send(songs_list)


    #-----------------------------------------------recharge------------------------------------------------------
@bot.command()
async def recharge(ctx):
        global server
        server = ctx.guild
        voice = discord.utils.get(bot.voice_clients, guild=server)

        if voice is None:
            await ctx.channel.send(f'{ctx.author.mention}, меня тут и не было!')
        else:
            await voice.disconnect()

        await ctx.message.author.voice.channel.connect()
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

        shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
        shift = shift_alt_phrase[shiftAlt_index]
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{shift}')
        await ctx.send(embed=embed)

        server = ctx.guild
        voice = discord.utils.get(bot.voice_clients, guild = server)
        if voice is None:
            await ctx.channel.send(f'{ctx.author.mention}, меня тут и не было!')
        else:
            await voice.disconnect()
    #----------------------------------------------------------------------------------------------------------




    #-------------------------------------------------stop---------------------------------------------------
@bot.command()
async def stop( ctx):
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
@bot.command()
async def куыгьу(ctx):
        global server

        shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
        shift = shift_alt_phrase[shiftAlt_index]
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{shift}')
        await ctx.send(embed=embed)

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


    #----------------------------------------------repeat_song---------------------------------------------------
@bot.command()
async def repeat_song(ctx, url):
        await ctx.send("Что бы остановить повторение музыки используйте команду recharge.")
        global vc
        musical_queue.append(url)
        print(musical_queue)
        try:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
        except:
            print('Уже подключен или не удалось подключиться')
        while True:
            if vc.is_playing():
                while vc.is_playing():
                    await sleep(1)
                play_music(ctx, musical_queue[0])
            else:
                play_music(ctx, musical_queue[0])
    #------------------------------------------------------------------------------------------------------------




    #--------------------------------help------------------------------------------------------------------------
@bot.command()
async def get_help(ctx):
        author = ctx.message.author
        check = ctx.message.content
        hello_index = random.randrange(0, 14)
        hi = hello_phrases[hello_index]

        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{hi}, {author.mention}!')
        await ctx.send(embed=embed)

        embed = discord.Embed(color=discord.Color.dark_red(), description=get_help_txt, title='Сейчас я расскажу тебе, что я умею на данный момент!')
        await ctx.send(embed=embed)






@bot.command()
async def пуе_рудз(ctx):
        author = ctx.message.author
        check = ctx.message.content
        hello_index = random.randrange(0, 14)
        hi = hello_phrases[hello_index]

        shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
        shift = shift_alt_phrase[shiftAlt_index]
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{shift}')
        await ctx.send(embed=embed)

        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{hi}, {author.mention}!')
        await ctx.send(embed=embed)

        embed = discord.Embed(color=discord.Color.dark_red(), description=get_help_txt, title='Сейчас я расскажу тебе, что я умею на данный момент!')
        await ctx.send(embed=embed)
    #------------------------------------------------------------------------------------------------------------


bot.run(token = settings['token'])