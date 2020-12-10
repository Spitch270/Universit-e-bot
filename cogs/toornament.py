#Author : CUNY Félicien
#Language : FR - French
#Date : 01/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord
from discord.ext import commands, tasks

class Toornament(commands.Cog): #création de la classe pour le cog

    def __init__(self, universitebot): #connexion avec le bot
        self.universitebot = universitebot

    @commands.Cog.listener() #Event dans un cog (obligatoire)
    async def on_ready(self): #lancement du bot en ligne
        print('success')

    @commands.command()
    async def poll(self, ctx, *, arg):
        message = await ctx.send(arg)
        await message.add_reaction('✅')
        await message.add_reaction('❎')