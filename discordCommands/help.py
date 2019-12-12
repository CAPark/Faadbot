import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')

    @commands.command(aliases=['helpme', 'HELPME', 'helpME', 'HELPme', 'HELP', 'commands', 'COMMANDS', 'h'])
    async def help(self, ctx):
        delim = []
        await ctx.send('List of bot commands: \n')
        CLfile = open("commandList.txt", "r")
        for line in CLfile:
            delim = line.split(".")
            await ctx.send('!' + delim[1])           
        CLfile.close()
        
        await ctx.send("**DETAILS**")
        await ctx.send("**For Every User**")
        await ctx.send("1. !help")
        await ctx.send("*HELP ALIASES: \"!help, !helpme, !HELPME, !helpME, !HELPme, !HELP, !commands, !COMMANDS, !h\"")
        await ctx.send("2. !ping: for \"pong!\" message.")
        await ctx.send("3. !shutdown")
        await ctx.send("4. !reboot")
        await ctx.send("5. !purge <number>: for CLEAN the messages")
        await ctx.send("*Can't delete more than 100 messages.*")
        await ctx.send("6. !nickname <nickname>")
        await ctx.send("*!nickname: for reset to default nickname.*")
        await ctx.send("7. !add_role <role>")
        await ctx.send("8. !del_role <role>")

        await ctx.send("**GAME**")
        await ctx.send("9. !Whelp: for Game Manual Page.")

        await ctx.send("**Only for Admin**")
        await ctx.send("10. !kick <@member> <reason>")
        await ctx.send("11. !ban <@member> <reason>")
        await ctx.send("12. !add_role <@member> <role>")
        await ctx.send("13. !del_role <@member> <role>")
   

def setup(bot):
    bot.add_cog(Help(bot))
