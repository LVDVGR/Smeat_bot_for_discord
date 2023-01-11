import audioop
import json
import requests
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
import pandas
import psycopg2
import sqlalchemy



FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True',
                   'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}



intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True

bot = commands.Bot(command_prefix = settings['prefix'], intents=intents)

server = None


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

@bot.command()
async def где(ctx):
        author = ctx.message.author
        check = ctx.message.content
        s = str(check)
        s = check.replace('Smeat ', '', 1)
        print(s)
        hello_index = random.randrange(0, 14)
        hi = hello_phrases[hello_index]
        letter = 'Следующую записку ты найдешь в Вовином ящике для белья. В комоде.'
        happy_burthday = 'Поздравляю тебя с 18тилетием от всего сердца.\nЖелаю добра, любви, позитива и успеха во всех твоих делах.\nТы большая молодец.\nОставайся такой же.\n-Твой брат. /owo\   '
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'Добрая ночь, Александра. /"V"\ ')
        await ctx.send(embed=embed)
        embed = discord.Embed(color=discord.Color.dark_red(), description=happy_burthday)
        await ctx.send(embed=embed)
        embed = discord.Embed(color=discord.Color.dark_red(), description=letter)
        await ctx.send(embed=embed)





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
        import Templates
        global server
        server = ctx.guild
        voice = discord.utils.get(bot.voice_clients, guild=server)
        if 'https:' in url:

            try:
                plist = Playlist(url)
                for url_playlists in plist.video_urls:
                    try:
                        yt = YouTube(url_playlists)
                        with_youtube(url)
                        songs_titles.append(yt.title)
                        musical_queue.append(url_playlists)
                    except:
                        print('lose')
                print(songs_titles)
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
                              description=f'Трек {name} \nнаходится на позиции {len(musical_queue)}',
                              title='МУЗИКАЛ КВЕВЕ /"V"\ ')

        await ctx.send(embed=embed)

        try:
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
        except:
            print('Уже подключен или не удалось подключиться')

        print("ya zdes")

        for temp in range(len(musical_queue)):
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
        shiftAlt_index = random.randrange(0, len(shift_alt_phrase) - 1)
        shift = shift_alt_phrase[shiftAlt_index]
        embed = discord.Embed(color=discord.Color.dark_red(), description=f'{shift}')
        await ctx.send(embed=embed)

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
            search_request = url + ' ' + p_r + ' ' + p_r1 + ' ' + p_r2 + ' ' + p_r3 + ' ' + p_r4 + ' ' + \
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

        for this_song in musical_queue:
            try:
                if vc.is_playing():
                    ctx.message.author.voice.channel.connect()
                    while vc.is_playing():

                        await sleep(1)
                    play_music(ctx, this_song)
                    await ctx.send("im here blyat'")
                    embed = discord.Embed(color=discord.Color.dark_red(),
                                          description=f'{songs_titles[0]}',
                                          title='Сейчас играет /owo\ ')
                    await ctx.send(embed=embed)

                    musical_queue.pop(0)
                    songs_titles.pop(0)
                else:
                    play_music(ctx, musical_queue[0])
                    await ctx.send("im here")
                    embed = discord.Embed(color=discord.Color.dark_red(),
                                          description=f'{songs_titles[0]}',
                                          title='Сейчас играет /owo\ ')
                    await ctx.send(embed=embed)
                    musical_queue.pop(0)
                    songs_titles.pop(0)
            except:
                pass


    #------------------------------------------------------------------------------------------------------------

@bot.command()
async def queue(ctx):
    curr = 1
    songs_list = ''

    for song in songs_titles:
        songs_list += f'{curr}. {str(song)} \n'
        curr += 1
    print(songs_list)
    # embed = discord.Embed(color=discord.Color.dark_red(),
    #                       description=f'{songs_list}',
    #                       title='Список треков в очереди:')
    #
    # await ctx.send(embed=embed)
    await ctx.send('Cписок треков(красивая рамочка не вывозит большие списки, но я это исправлю!!)')
    await ctx.send(songs_list)



#---------------------------------------------------------create playlist----------------------------------------------
@bot.command()
async def create_playlist(ctx, name):
    from sqlalchemy import create_engine
    from config import creds
    import pandas as pd
    # engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(creds["user"], creds["password"],
    #                                                                        creds["host"], creds["db_name"]))
    # df = pd.read_sql(f"create table {name} (songs text)", engine)
    try:
        connection = psycopg2.connect(host=creds["host"], user=creds["user"],
                                  password=creds["password"], database=creds["db_name"])
        with connection.cursor() as cursor:
            cursor.execute(f"create table {name} (songs text)")
            connection.commit()
        embed = discord.Embed(color=discord.Color.dark_red(),
                              description=f'Создан плейлист с гордым названием "{name}"',
                              title='Поздравляем, у вас плейлист. /тwт\ ')
        await ctx.send(embed=embed)
    except Exception as error:
        print(f'{error}')



#---------------------------------------------------------add to playlist----------------------------------------------
@bot.command()
async def add_song_to(ctx, playlist_name, song_url):
        from sqlalchemy import create_engine
        from config import creds
        import pandas as pd
        # engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(creds["user"], creds["password"],
        #                                                                        creds["host"], creds["db_name"]))
        # df = pd.read_sql(f"create table {name} (songs text)", engine)
        try:
            connection = psycopg2.connect(host=creds["host"], user=creds["user"],
                                          password=creds["password"], database=creds["db_name"])
            with connection.cursor() as cursor:
                cursor.execute(f"insert into {playlist_name} (songs) values ('{song_url}')")
                connection.commit()
            embed = discord.Embed(color=discord.Color.dark_red(),
                                  description=f'Трек "{song_url}" добавлен в плейлист "{playlist_name}"',
                                  title='Пополнение. /хwх\ ')
            await ctx.send(embed=embed)
        except Exception as error:
            print(f'{error}')



#---------------------------------------------------------show playlist----------------------------------------------
@bot.command()
async def show_playlist(ctx, playlist_name):
        from sqlalchemy import create_engine
        from config import creds
        import pandas as pd

        try:
            engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(creds["user"], creds["password"],
                                                                                   creds["host"], creds["db_name"]))
            df = pd.read_sql(f"select * from {playlist_name}", engine)
            dff = df['songs'].values
            songs = dff.tolist()
            print(songs)
            embed = discord.Embed(color=discord.Color.dark_red(),
                                  description=f'Ниже ваш плейлист.',
                                  title='Показываю. /хwх\ ')
            await ctx.send(embed=embed)

            i = 1
            output = ''
            for song in songs:
                output += f"{str(i)}. {song} \n "
            await ctx.send(output)
        except Exception as error:
            print(f'{error}')

   #-----------------------------------------------delete from playlist------------------------------------------------------



@bot.command()
async def delete_song_from(ctx, playlist_name, song_url):
        from sqlalchemy import create_engine
        from config import creds
        import pandas as pd
        # engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(creds["user"], creds["password"],
        #                                                                        creds["host"], creds["db_name"]))
        # df = pd.read_sql(f"create table {name} (songs text)", engine)
        try:
            connection = psycopg2.connect(host=creds["host"], user=creds["user"],
                                          password=creds["password"], database=creds["db_name"])
            with connection.cursor() as cursor:
                cursor.execute(f"delete from {playlist_name} where songs = '{song_url}'")
                connection.commit()
            embed = discord.Embed(color=discord.Color.dark_red(),
                                  description=f'Трек "{song_url}" удалён из плейлиста "{playlist_name}"',
                                  title='Война еще не окончена..Мой дорогой предатель... /х_х\ ')
            await ctx.send(embed=embed)
        except Exception as error:
            print(f'{error}')





    #-----------------------------------------------recharge------------------------------------------------------
@bot.command()
async def recharge(ctx):
        global server
        server = ctx.guild
        voice = discord.utils.get(bot.voice_clients, guild=server)

        if voice is None:
            await ctx.channel.send(f'{ctx.author.mention}, меня тут и не было!')
        else:
            embed = discord.Embed(color=discord.Color.dark_red(),
                                  description=f'Я за пивом.',
                                  title='Один момент /:D\ ')
            await ctx.send(embed=embed)
            await voice.disconnect()

        await ctx.message.author.voice.channel.connect()
        embed = discord.Embed(color=discord.Color.dark_red(),
                              description=f'Свежайшее... светлое... чешское..)',
                              title='Я вернулся /омо\ ')
        await ctx.send(embed=embed)
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
async def skip(ctx):
    import Templates
    voice_client = ctx.message.guild.voice_client
    embed = discord.Embed(color=discord.Color.dark_red(),
                          description=f'Выполняю сложнейшую операцию по пропуску трека.',
                          title='Пропустим песню /-w-\ ')
    await ctx.send(embed=embed)
    if voice_client.is_playing():
        Templates.is_pause = True
        await voice_client.pause()
    #----------------------------------------------------------------------------------------------------------




    #-------------------------------------------------------------resume------------------------------------
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    import Templates
    voice_client = ctx.message.guild.voice_client
    embed = discord.Embed(color=discord.Color.dark_red(),
                          description=f'Продолжаем переполнять перепонки перемузыкой переидинахуй',
                          title='Продолжаем /TvT\ ')
    await ctx.send(embed=embed)
    if voice_client.is_paused():
        Templates.is_pause = False
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


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