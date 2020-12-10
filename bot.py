#Author : CUNY Félicien
#Language : FR - French
#Date : 01/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord #importation des modules discord
import random  #importation du random
import os #pour les cogs
import youtube_dl #permet le téléchargement youtube
import requests #permet l'API
import json #utiliser l'API
from random import choice
from discord.voice_client import VoiceClient
from discord.ext import commands, tasks#importation des fonctions pour discord bot
from itertools import cycle #importation de l'itération en cycle

universitebot = commands.Bot(command_prefix = '$') #prefixe à utiliser pour intéragir avec le bot

@universitebot.event #Déclarer à chaque fois que l'on veut une action du bot
async def on_ready(): #lancement du bot en ligne
    await universitebot.change_presence(status=discord.Status.idle, activity=discord.Game('Creation de tournoi...'))
    print('Le bot est pret') #indique que le bot est lancé.

@universitebot.command(help='Permet de connaitre sa latence') #Déclarer à chaque fois que l'on veut utiliser le bot
async def ping(ctx): #ping = nom de la commande; exemple $ping pourra être utiliser sur discord pour trigger le bot
    await ctx.send(f'Pong ! Tu as une connexion de {round(universitebot.latency * 1000)}ms')

@universitebot.command()
async def load(ctx, extension):
    universitebot.load_extension(f'cogs.{extension}')

@universitebot.command()
async def unload(ctx, extension):
    universitebot.unload_extension(f'cogs.{extension}')

@universitebot.command()
async def poll(ctx, *, arg):
    message = await ctx.send(arg)
    await message.add_reaction('✅')
    await message.add_reaction('❎')

for filename in os.listdir('./Universit-e-bot/cogs'):
    if filename.endswith('.py'):
        universitebot.load_extension(f'cogs.{filename[:-3]}')

universitebot.run('Token')
