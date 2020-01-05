import discord

TOKEN = open("faadbotToken.txt", "r").read() #bot token

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return #prevents the bot from responding to its own messages

    if message.content.startswith('!exit'):
        msg = 'Closing helloWorld.py'.format(message)
        await message.channel.send(msg)
        await client.close()
    
    elif message.content.startswith('!'):
        msg = 'Hello World'.format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('-----')

client.run(TOKEN)
