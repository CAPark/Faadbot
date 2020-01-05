import discord
from discord.ext import commands

class shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'shutdown')
    async def shutdown(self, ctx):
        await ctx.send('Shutting down faadbot')
        await self.bot.logout()

def setup(bot):
    bot.add_cog(shutdown(bot))