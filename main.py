import asyncio
from typing import Final
import os
import discord
from discord import Intents, Client, Message
from dotenv import load_dotenv
# from responses import get_response
from discord import app_commands
from discord.ext import commands, tasks
from itertools import cycle
import yt_dlp
import wavelink
from wavelink.ext import spotify

load_dotenv()
TOKEN: Final[str]=os.getenv("DISCORD_TOKEN")

status = cycle(['/help',
                'Tutel!',
                'I have kids in my basement...'
                'War Thunder',
                'Gaming!',
                'Credits to SovietCosmoCat',
                'Chilling'
        ])

intents=discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)



# events

@bot.event
async def on_ready() -> None:
    change_status.start()
    print(f'{bot.user} is up and running!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logs=open('logs.txt','a')
        print(e,file=logs)
        print(e)
        logs.close()

@bot.event
async def on_wavelink_track_end(player:wavelink.Player, track:wavelink.YouTubeTrack,reason) -> None:
    return

@bot.tree.command(name="ping", description="Sends ping")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f'{interaction.user.mention} Pong! {round(bot.latency * 1000)} ms', ephemeral=True)

@bot.hybrid_command(name="echo", description="Echoes a message")
@app_commands.describe(message="The message to echo")
async def echo(ctx: commands.Context, message: str):
    await ctx.send(message)

@bot.tree.command(name="info", description="Info about user")
async def info(interaction: discord.Interaction, member: discord.Member) -> None:
    if member.premium_since == None:
        isNitro=":x:"
    else:
        isNitro=member.premium_since

    embed = discord.Embed(title=member.name, description=f"{member.mention} is cool\nJoined server at {member.joined_at.day}/{member.joined_at.month}/{member.joined_at.year}\nNitro boost: {isNitro}", color=member.color,)
    embed.set_thumbnail(url=member.display_avatar)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="spam", description="Spams a message")
@app_commands.describe(message="The message to spam")
@commands.has_permissions(administrator = True)
async def spam(interaction: discord.Interaction, message: str, amount: int) -> None:
        await interaction.response.send_message(f'SPAM ON THE WAY', ephemeral=True)
        for i in range(amount): await interaction.channel.send(message)


@bot.tree.command(name="dm", description="The direct message to user")
@app_commands.describe(message="The direct message to user")
async def dm(interaction: discord.Interaction,member: discord.Member, message: str):
    author=interaction.user
    interaction.user = member
    await interaction.user.send(message)
    await interaction.user.send(f'Message sent by {author} from {interaction.guild}')
    await interaction.response.send_message(f'Message sent to user', ephemeral=True)

@bot.tree.command(name="anondm", description="The anonymouse direct message to user")
@app_commands.describe(message="The direct message to user")
@commands.has_permissions(administrator = True)

async def anondmdm(interaction: discord.Interaction,member: discord.Member, message: str):
    interaction.user = member
    await interaction.user.send(message)
    await interaction.response.send_message(f'Message sent to user', ephemeral=True)



@bot.tree.command(name="clear", description="Deletes messages")
@commands.has_permissions(administrator = True, )
async def clear(ctx, amount: int) -> None:
    await ctx.channel.purge(limit=amount)
    # await discord.InteractionResponse.send_message(f'Deleted {amount} messages', ephemeral=True)

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction) -> None:
    return

@bot.tree.command(name="play", description="Play a song")
async def music(interaction: discord.Interaction, quary: str) -> None:
    discord.VoiceClient().connect(discord.Client.user)



@bot.tree.command(name="pause", description="Pause a song")
async def pause(interaction: discord.Interaction) -> None:
    return

@bot.tree.command(name="skip", description="Skip a song")
async def skip(interaction: discord.Interaction, number: int=1) -> None:
    return

@bot.tree.command(name="start", description="Start pasused song")
async def start(interaction: discord.Interaction) -> None:
    return





#
# voice_clients = {}
# yt_dlp_options = {"format":"bestaudio/best"}
# ytdl=yt_dlp.YoutubeDL(yt_dlp_options)
#
# ffmepg_options = {'options':'-vn'}
# @bot.tree.command(name="play", description="query:")
# async def music(interaction: discord.Interaction, query:str) -> None:
#     try:
#
#         voice_client = await discord.Member.voice.connect()
#         voice_clients[voice_client.guild.id]=voice_client
#
#     except Exception as e:
#         logs=open('logs.txt','a')
#         print(e,file=logs)
#         print(e)
#         logs.close()
#     try:
#
#         url=query
#         loop=asyncio.get_event_loop()
#         data= await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
#         song=data['url']
#         player = discord.FFmpegPCMAudio(song,**ffmepg_options)
#         voice_clients[interaction.message.voice_client.guild.id].play(player)
#     except Exception as e:
#         logs = open('logs.txt', 'a')
#         print(e, file=logs)
#         print(e)
#         logs.close()
#



# tasks
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


def main() -> None:
    bot.run(token=TOKEN)

if __name__=='__main__':
    main()

#
