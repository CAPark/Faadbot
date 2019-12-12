import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class purge(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='purge')
    async def purge(self, ctx, amount: int):

        await ctx.message.delete()

        if amount > 100:
            return await ctx.send("You can't purge more than 100messages.")
        try:
            await ctx.channel.purge(limit=amount + 1)

        except discord.HTTPException:
            pass

def setup(bot):
    bot.add_cog(purge(bot))
