import json
from secrets import BOT_TOKEN
import discord
import requests
from discord.ext import commands
from settings import Settings
import re

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Logged In As")
    print(bot.user.name)
    print("------")
    print(bot.user.id)
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="People Banning Users")
    )

GuildSettings = {}

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(int(payload.channel_id))
    message = await channel.fetch_message(payload.message_id)

    if (not message.author.id == bot.user.id or not "Created a poll to vote ban user" in message.content or "Voting has ended" in message.content): #ik this is really bad way to do this but whatever
        return

    settings = getGuildSettings(message.guild.id)

    mentions = re.findall(r"!?[0-9]{18}", message.content)

    userVotedToBan = mentions[0]
    userToBan = mentions[1]
    reactionList = message.reactions

    upCount = getReactionCount(reactionList, "👍")
    downCount = getReactionCount(reactionList, "👎")
    guild = bot.get_guild(payload.guild_id)

    if (upCount - downCount) >= settings.getVoteGap():
        await banUser(message,userToBan)
        await message.edit(content = message.content + "\n Voting has ended")

    elif (downCount - upCount) >= settings.getVoteGap():
        await banUser(message, userVotedToBan)
        await channel.send(f"Nobody Wants to ban <@{userToBan}> and <@{userVotedToBan}> is a coward.")
        await message.edit(content = message.content + f"\n Voting has ended")


async def banUser(message,userToBan):
    try:
        await message.guild.ban(discord.Object(userToBan))
        await message.reply(f"User <@{userToBan}> has been banned.")
    except Exception as e:
        await message.reply(f"Could not ban user <@{userToBan}> Because: {e}")

def getReactionCount(reactionList, reaction):
    for i in reactionList:
        if i.emoji == reaction:
            return i.count
    return 0



@bot.command("voteban")
async def voteban(ctx:discord.ext.commands.context.Context, user: discord.User = None):
    if user == None:
        await ctx.send("Please Mention A User To Ban.")
        return

    settings = Settings(ctx.guild.id)

    if settings.getBotChannel() != None:
        channel = bot.get_channel(settings.getBotChannel())
        message = await channel.send(f" {ctx.author.mention} Created a poll to vote ban user: " + user.mention)
    else:
        message = await ctx.reply(f" {ctx.author.mention} Created a poll to vote ban user: " + user.mention)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

@commands.has_permissions(administrator=True)
@bot.command("setbotchannel")
async def setbotchannel(ctx:discord.ext.commands.context.Context, channel: discord.TextChannel = None):
    if channel == None:
        await ctx.send("Please Mention A Channel.")
        return
    getGuildSettings(ctx.guild.id).setBotChannel(channel.id)
    await ctx.send("Bot Channel Set To: " + channel.mention)

@commands.has_permissions(administrator=True)
@bot.command("setvotegap")
async def setvotegap(ctx:discord.ext.commands.context.Context, count: int = None):
    if count == None:
        await ctx.send("Please Specify A Number.")
        return

    getGuildSettings(ctx.guild.id).setVoteGap(count)
    await ctx.send("Vote Gap Set To: " + str(count))

def getGuildSettings(guildID):
    if guildID not in GuildSettings:
        GuildSettings[guildID] = Settings(guildID)
    return GuildSettings[guildID]

bot.run(BOT_TOKEN)
