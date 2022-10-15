import json
from secrets import BOT_TOKEN
import discord
import requests
from discord.ext import commands
from settings import Settings


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


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(int(payload.channel_id))
    message = await channel.fetch_message(payload.message_id)

    if (not message.author.id == bot.user.id or not message.content.startswith("Vote To Ban User:")):
        return
    userToBan = message.mentions[0].id

    reactionList = message.reactions

    upCount = getReactionCount(reactionList, "👍")
    downCount = getReactionCount(reactionList, "👎")
    if (upCount - downCount) >= 5:
        guild = bot.get_guild(payload.guild_id)
        try:
            await guild.ban(discord.Object(userToBan))
            await channel.send(f"User {userToBan} has been banned.")
        except Exception as e:
            await channel.send(f"Could not ban user {userToBan} Because: {e}")

        await message.delete()


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
        ctx = bot.get_channel(settings.getBotChannel())

    message = await ctx.send("Vote To Ban User: " + user.mention)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

@commands.has_permissions(administrator=True)
@bot.command("setbotchannel")
async def setbotchannel(ctx:discord.ext.commands.context.Context, channel: discord.TextChannel = None):
    if channel == None:
        await ctx.send("Please Mention A Channel.")
        return

    settings = Settings(ctx.guild.id)
    settings.setBotChannel(channel.id)
    await ctx.send("Bot Channel Set To: " + channel.mention)

bot.run(BOT_TOKEN)
