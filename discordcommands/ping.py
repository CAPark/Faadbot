import discord 
from discord.ext import commands

class ping(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'ping')
    async def ping(self,ctx):
        await ctx.send('pong!')

def setup(bot):
    bot.add_cog(ping(bot))