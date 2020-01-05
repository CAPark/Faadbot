import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions

class ban(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'ban')
    @has_permissions(manage_roles=True, ban_members=True)
    async def ban(self,ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

def setup(bot):
    bot.add_cog(ban(bot))