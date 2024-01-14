import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix='/', intents=intents)

class Timer:
    time_left : int
    func = None
    args : tuple

    def __init__(self, length, func, *args) -> None:
        self.time_left = length
        self.func = func
        self.args = args
        self.timer.start()        

    @tasks.loop(seconds=1)
    async def timer(self):
        if(self.time_left <= 0):
            await self.func(self.args)
            self.timer.stop()    
        self.time_left -= self.timer.seconds

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def kick_me(ctx, length, *args):
    scale = parse_scale(args)
    Timer(int(length) * scale, disconnect_member, ctx.author)

@bot.command()
async def kick_all(ctx, length, *args):
    scale = parse_scale(args)
    channel = discord.VoiceChannel
    if(ctx.author.voice == None):
        await ctx.send("You aren't in a vc!")
        return
    else:
        channel = ctx.author.voice.channel
    Timer(int(length) * scale, clear_vc, channel)


def parse_scale(args):
    scale = 1
    for arg in args:
        if(arg.equals("-s")):
            scale = 1
        elif(arg.equals("-m")):
            scale = 60
        elif(arg.equals("-h")):
            scale = 3600
    
    return scale

#channel (one of the discord text channel types (theres a few))
#message (string)
async def send_message(args : tuple):
    channel : discord.channel = args[0]
    message : str = args[1]
    await channel.send(message)

#member (discord.member)
#channel (discord.VoiceChannel)
async def move_member(args : tuple):
    member : discord.member = args[0]
    #if there is no second arg, assume the voice channel is none(will kick member)
    channel : discord.VoiceChannel = None
    if(len(args) > 1):
        channel = args[1]

    #if the member is not currently in a voice chat, return
    if(member.voice.channel == None):
        return
    
    #move the member to the channel
    await member.move_to(channel)

async def disconnect_member(args : tuple):
    member : discord.member = args[0]
    await member.move_to(None)


async def clear_vc(args : tuple):
    members = args[0].members
    for m in members:
        await disconnect_member(tuple([m]))

if __name__ == "__main__":
    if TOKEN != "placeholder":
        bot.run('MTA5Mzk1OTg1ODU3Mjc1OTA5MQ.GFaVae.aPegfUeatUAgxbmvihy_sa4QxwpQbA9xjnPiIs')
    else:
        raise Exception("No token passed for bot in .env file")
