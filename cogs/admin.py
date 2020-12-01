#Author : CUNY Félicien
#Language : FR - French
#Date : 01/12/2020
#Copyright : This code can be use for every member working on 'Universit'E-Bot' discord bot only. If you want to work on it, please contact me : felicien.cuny@outlook.fr

import discord
from discord.ext import commands, tasks

class Admin(commands.Cog): #création de la classe pour le cog

    def __init__(self, universitebot): #connexion avec le bot
        self.universitebot = universitebot

    @commands.Cog.listener() #Event dans un cog (obligatoire)
    async def on_ready(self): #lancement du bot en ligne
        print('success')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Erreur Argument')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount+1)

    @commands.command() #Command dans un cog
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command() #Command dans un cog
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
                return


def setup(universitebot):
    universitebot.add_cog(Admin(universitebot))
