#Author : CUNY Félicien
#Language : FR - French
#Date : 02/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord
from random import choice
import youtube_dl
from discord.ext import commands, tasks
from discord.voice_client import VoiceClient

class Musique(commands.Cog): #création de la classe pour le cog

    def __init__(self, universitebot): #connexion avec le bot
        self.universitebot = universitebot

    youtube_dl.utils.bug_reports_message = lambda: ''

    ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extracot)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
    ffmpeg_options = {
    'options': '-vn'
}

    ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=1):
            super().__init__(source, volume)

            self.data = data

            self.title = data.get('titre')
            self.url = data.get('url')

        @classmethod
        async def from_url(self, cls, url, *, loop=None, stream=False):
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]

            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    queue = []

    @commands.command(name='join', help='Cette commande au bot de rejoindre un salon')
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("Pas connecter a un channel vocal")
            return

        else:
            channel = ctx.message.author.voice.channel

        await channel.connect()

    @commands.command(name='queue', help='Cette commande ajoute une musique à la file')
    async def queue_(self, ctx, url):
        global queue

        queue.append(url)
        await ctx.send(f'`{url}` added to queue!')

    @commands.command(name='remove', help='Cette commande retire une musique de la liste')
    async def remove(self, ctx, number):
        global queue

        try:
            del(queue[int(number)])
            await ctx.send(f'La file en attente : `{queue}!`')

        except:
            await ctx.send('la file en attente est **empty** ou a un indexe **out of range**')

    @commands.command(name='play', help='Cette commande joue les musiques')
    async def play(self, ctx):
        global queue

        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await YTDLSource.from_url(queue[0], loop=client.loop)
            voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('**Now playing:** {}'.format(player.title))
        del(queue[0])

    @commands.command(name='pause', help='Cette commande met en pause la musique')
    async def pause(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.pause()

    @commands.command(name='resume', help='Cette commande reprend la musique')
    async def resume(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.resume()

    @commands.command(name='view', help='Cette commande montre la liste en attente')
    async def view(self, ctx):
        await ctx.send(f'Your queue is now `{queue}!`')

    @commands.command(name='leave', help='Cette commande fais quitter le bot')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        await voice_client.disconnect()

    @commands.command(name='stop', help='Cette commande arrête la musique')
    async def stop(self, ctx):
        server = ctx.message.guild
        voice_channel = server.voice_client

        voice_channel.stop()

def setup(universitebot):
    universitebot.add_cog(Musique(universitebot))
