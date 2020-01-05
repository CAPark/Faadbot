import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions

class kick(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'kick')
    @has_permissions(manage_roles=True, kick_members=True)
    async def kick(self,ctx, member:discord.Member, *, reason=None ):
        await member.kick(reason=reason)

    @kick.error
    async def kickHandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Err: missing input \n \
**Command**: Kick \n \
**Description**: Moderation tool to kick users from the server \n \
**Alias(es)**: ``kick`` \n \
**Usage**: ``!kick <userID>`` \n ")                      

def setup(bot):
    bot.add_cog(kick(bot))