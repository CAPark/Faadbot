import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


class Slowmode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Sets the chat to slowmode <time(sec)>
    @commands.command(name='slowmode')
    @has_permissions(manage_channels=True, manage_guild=True)
    async def slowmode(self, ctx, *, time=None):
        if time is None:
            currentDelay = ctx.channel.slowmode_delay
            if currentDelay == 0:
                await ctx.send('Slowmode is currently disabled for channel: **{}**'.format(ctx.channel))
            else:
                await ctx.send('Current slowmode delay for channel **{}** '
                               'is set to **{}** seconds'.format(ctx.channel, currentDelay))
            return

        time = time is not None and time.isdigit() and int(time)
        if time not in range(0, 180):
            await ctx.send('Please specify a slowmode delay value between **1** and **180** seconds,'
                           ' or **0** to disable.')
        elif time == 0:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send('Disabled slowmode delay for channel: **{}**'.format(ctx.channel))
        else:
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send('Set the slowmode delay for channel **{}** to **{}** seconds.'.format(ctx.channel, time))


def setup(bot):
    bot.add_cog(Slowmode(bot))
