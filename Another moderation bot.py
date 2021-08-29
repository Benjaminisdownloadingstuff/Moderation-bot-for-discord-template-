import os
from discord import channel
from discord.colour import Color
from discord.ext import commands
import discord
from dotenv import load_dotenv
from discord import Member
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import random

load_dotenv('DISCORD_TOKEN.env')#loads client secret from the .env file in the same directory
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
bot = commands.Bot(command_prefix='^') #change it to whatever you want
bot.remove_command("help")

@bot.event
async def on_ready():
    activity = discord.Game(name="A game", type=3) #you can change from playing to watching, etc 
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready!")

@bot.event
async def on_message(message): # deletes any slur in the curseWord list
    await bot.process_commands(message)
    if message.author.id == bot.user:
        #await bot.process_commands(message)
        return
    msg_content = message.content.lower()
    curseWord = ['curse1', 'curse2','curse3']
    if any(word in msg_content for word in curseWord):
        await message.delete()
        em = discord.Embed(title=" Warning!", description="", color=0xB026FF)
        em.add_field(name="Slur used", value="Heya, please refrain from using slurs! mwah :heart:")
        em.set_footer(text="E-whore development")
        await message.channel.send(embed=em)

@bot.command()
@commands.has_permissions(ban_members=True)#bans members if admin role is true
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",color=0xB026FF)
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        ban = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}",color=0xB026FF)
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)

@bot.command()#makes an announcement in the given given channel ID
@commands.has_permissions(administrator=True)
async def announce(ctx, channel: int, announcements:str):
  channel = bot.get_channel(channel)
  em = discord.Embed(title=f":loudspeaker: Announcement", description="Listen up!",color=0xB026FF)
  em.add_field(name="Announcement:", value=announcements)
  em.set_footer(text="sorry for the ping T-T")
  await channel.send(embed=em)
  
  await channel.send('@everyone')


@bot.command()## get mentioned users avatar
async def av(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@bot.command()##help command
async def help(ctx):
    em = discord.Embed(title="E-whore command list:", description="", color=0x2f3136)
    em.add_field(name="`^ban {user}`", value="Bans the user.")
    em.add_field(name="`^kick {user}`", value="Kicks user.")
    em.add_field(name="`^avatar {user}`", value="Gets the mentioned users pfp.")
    em.add_field(name="`^announce {channel ID} {Your announcement here within quotes.}`", value="Announces whatever the admin/owner types in the specified channel.")
    em.set_footer(text="GitHub Discord bot made by Sachit71")
    await ctx.send(embed=em)

## you can always add more commands emotes, actions build whole economies and music capabilities, etc etc 
## this is just a basic moderation bot to get you started

bot.run(TOKEN)
client.run(TOKEN)