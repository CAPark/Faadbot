import discord
from discord.ext import commands

#just reloads all modules as a means of restarting
class reboot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name = 'reboot')
    async def reboot(self, ctx):
        module = []
        await ctx.send('Rebooting faadbot modules, please standby')
        CLfile = open("commandList.txt", "r")
        for line in CLfile:
            module = line.split("\n")
            self.bot.unload_extension(module[0])
            self.bot.load_extension(module[0])
            await ctx.send(module[0] + ' reloaded \n')
        CLfile.close()
        await ctx.send('reboot of modules complete')

def setup(bot):
    bot.add_cog(reboot(bot))