import discord
from discord.ext import commands


class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Change nickname
    # Format: !nickname new_name
    # Leave 'new_name' empty to reset back to original user name
    @commands.command(name='nickname')
    async def nickname(self, ctx, *, name: str = None):
        if name is None:
            # await ctx.message.delete()
            await ctx.message.author.edit(nick=name)
            await ctx.send('Reset nickname back to %s' % ctx.message.author.name)
        else:
            await ctx.message.author.edit(nick=name)
            await ctx.send('Changed nickname to %s' % name)


def setup(bot):
    bot.add_cog(Nickname(bot))
