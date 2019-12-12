import discord 
from discord.ext import commands
from discord.ext.commands import has_permissions

class add_role(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='add_role')
    @has_permissions(manage_roles=True)
    async def add_role(self, ctx, member : discord.Member,*, myrole=None):
        if(myrole == None):
            await ctx.send('Invalid command. \n!add_role <@member> <role>')
        else:
            user = ctx.message.author
            role = discord.utils.get(user.guild.roles, name=myrole)
            rolelist = []
            for roles in user.guild.roles:
                rolelist.append(roles.name)
            if(role == None):
                await ctx.send('Invalid role.\nMake sure to type in a valid role.\nBelow is the list of valid roles: ')
                await ctx.send(rolelist)
            else:
                await member.add_roles(role)
                await ctx.send(f'Successfully added the <{member}>\'s role to <{role}>')


    @commands.command(name='add_myrole')
    async def add_myrole(self, ctx,*, myrole=None):
        if(myrole == None):
            await ctx.send('Invalid command. \n!add_role <role>')
        else:
            user = ctx.message.author
            role = discord.utils.get(user.guild.roles, name=myrole)
            rolelist = []
            for roles in user.guild.roles:
                rolelist.append(roles.name)
            if(role == None):
                await ctx.send('Invalid role.\nMake sure to type in a valid role.\nBelow is the list of valid roles: ')
                await ctx.send(rolelist)
            else:
                await ctx.message.author.add_roles(role)
                await ctx.send(f'Successfully added the <{role}> from me.')

class del_role(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name = 'del_role')
    @has_permissions(manage_roles=True)
    async def del_role(self, ctx, member : discord.Member, *, myrole = None):
        if(myrole == None):
            await ctx.send('Invalid command. \n!del_role <@member> <role>')
        else:
            user = ctx.message.author
            role = discord.utils.get(user.guild.roles, name=myrole)
            role_list = []
            mem_role_list = []
            mem_roleNames = []
            for roles in user.guild.roles:
                role_list.append(roles.name)
            for memRoles in member.roles:
                mem_roleNames.append(memRoles.name)
                mem_role_list.append(memRoles)
            if(role == None or role not in mem_role_list):

                await ctx.send('Invalid role. \nMake sure to type in a valid role. OR Make sure to type in the member has. \nBelow is the list of valid roles: ')
                await ctx.send(role_list)
                await ctx.send('Below is the list of member roles.')
                await ctx.send(mem_roleNames)
            else:
                await member.remove_roles(role)
                await ctx.send(f'Successfully removed the <{member}>\'s role to <{role}>')

    @commands.command(name = 'del_myrole')
    async def del_myrole(self, ctx, *, myrole = None):
        if(myrole == None):
            await ctx.send('Invalid command. \n!del_myrole <role>')
        else:
            user = ctx.message.author
            role = discord.utils.get(user.guild.roles, name=myrole)
            role_list = []
            mem_role_list = []
            mem_roleNames = []
            for roles in user.guild.roles:
                role_list.append(roles.name)
            for memRoles in ctx.message.author.roles:
                mem_roleNames.append(memRoles.name)
                mem_role_list.append(memRoles)
            if(role == None or role not in mem_role_list):

                await ctx.send('Invalid role. \nMake sure to type in a valid role. OR Make sure to type in the member has. \nBelow is the list of valid roles: ')
                await ctx.send(role_list)
                await ctx.send('Below is the list of member roles.')
                await ctx.send(mem_roleNames)
            else:
                await ctx.message.author.remove_roles(role)
                await ctx.send(f'Successfully removed the <{role}> from me.')


def setup(bot):
    bot.add_cog(add_role(bot))
    bot.add_cog(del_role(bot))
