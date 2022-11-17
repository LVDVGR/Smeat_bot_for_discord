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



intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True

bot = commands.Bot(command_prefix = settings['prefix'], intents=intents)

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
            ctx.message.author.voice.channel.connect()
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
        try:
            await ctx.channel.send(f'И начинается наша вечерняя музыкальная программа с некого трека, название которого я еще не знаю, а мне собственно и до пизды!!')
            voice_channel = ctx.message.author.voice.channel
            vc = await voice_channel.connect()
        except:
            print('Уже подключен или не удалось подключиться')

        musical_queue.append(url)
        print(musical_queue)
        await ctx.channel.send(f'Трек находится на позиции {len(musical_queue) + 1}.')

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
        await ctx.send(f'{hi}, {author.mention}!')
        await ctx.send(f'Сейчас я расскажу тебе, что я умею на данный момент! ')
        await ctx.send(f'Команда hello - я просто с тобой приветствуюсь(представь как все грустно, '
                       f'что бы с тобой поздоровались тебе приходится командовать:))')
        await ctx.send(f'Команда play - после команды через пробел вставь ссылку с ютуба и я сыграю аудиоряд с этой ссылке.')
        await ctx.send(f'Команда repeat_song - если ты хочешь определённую песню заслушать до дыр, то аналогично команде выше использую эту команду.')
        await ctx.send(f'Команда recharge - по сути эта команда нужна, что бы выключить бесконечное повторение трека. '
                       f'Как говорил Сэм Винчестер "Песня хорошая, но не 50 раз подряд."')
        await ctx.send(f'Команда add_song - по сути эта команда не приносит пользы, но она есть, так как мой создатель работает над плейлистами, '
                       f'но еще не придумал как точно это будет выглядеть. По сути это просто наработка. ')
        await ctx.send(f'Команда leave - если ты меня хочешь выгнать с канала, то используй эту команду. Но не переживай, ты из дискорда всё равно уйдешь раньше меня:).')
        await ctx.send(f'Команда stop - если хочешь, что бы я остановил трек, который играет в данный момент, то используй эту команду.')
        await ctx.send(f'Команда resume - для того, что бы продолжить воспроизведение остановленного трека')
        await ctx.send(f'Команда volume - настрйока громкости меня, если конечно ползунок под моей аватаркой тебя не устраивает. '
                       f'Просто введи число во сколько раз хочешь сделать меня громче. Но помни, число от 0 до 2,'
                       f' где 0 - заткнуть меня вообще, 2 сделать в 2 раза громче. '
                       f'.'
                       f'.'
                       f'p.s. от 0 до 1 я все равно становлюсь тише, так работает умножение.')
        await ctx.send(f'Команда show - после этой команды ты можешь написать название животного на анлгийском и я скину тебе его фотку.')




@bot.command()
async def пуе_рудз(ctx):
        author = ctx.message.author
        check = ctx.message.content
        hello_index = random.randrange(0, 14)
        hi = hello_phrases[hello_index]
        await ctx.send(f'{hi}, {author.mention}!')
        await ctx.send(f'Сейчас я расскажу тебе, что я умею на данный момент! ')
        await ctx.send(f'Команда hello - я просто с тобой приветствуюсь(представь как все грустно, '
                       f'что бы с тобой поздоровались тебе приходится командовать:))')
        await ctx.send(f'Команда play - после команды через пробел вставь ссылку с ютуба и я сыграю аудиоряд с этой ссылки.')
        await ctx.send(f'Команда repeat_song - если ты хочешь определённую песню заслушать до дыр, то аналогично команде выше используй эту команду.')
        await ctx.send(f'Команда recharge - по сути эта команда нужна, что бы выключить бесконечное повторение трека. '
                       f'Как говорил Сэм Винчестер "Песня хорошая, но не 50 раз подряд."')
        await ctx.send(f'Команда add_song - по сути эта команда не приносит пользы, но она есть, так как мой создатель работает над плейлистами, '
                       f'но еще не придумал как точно это будет выглядеть. По сути это просто наработка. ')
        await ctx.send(f'Команда leave - если ты меня хочешь выгнать с канала, то используй эту команду. Но не переживай, ты из дискорда всё равно уйдешь раньше меня:).')
        await ctx.send(f'Команда stop - если хочешь, что бы я остановил трек, который играет в данный момент, то используй эту команду.')
        await ctx.send(f'Команда resume - для того, что бы продолжить воспроизведение остановленного трека')
        await ctx.send(f'Команда volume - настрйока громкости меня, если конечно ползунок под моей аватаркой тебя не устраивает. '
                       f'Просто введи число во сколько раз хочешь сделать меня громче. Но помни, число от 0 до 2,'
                       f' где 0 - заткнуть меня вообще, 2 - сделать в 2 раза громче. '
                       f'p.s. от 0 до 1 я все равно становлюсь тише, так работает умножение.')
        await ctx.send(f'.')
        await ctx.send(f'.')
        await ctx.send(f'Команда show - после этой команды ты можешь написать название животного на анлгийском и я скину тебе его фотку.')
    #------------------------------------------------------------------------------------------------------------


bot.run(token = settings['token'])
