
import discord
import time
import datetime
import asyncio
from creds import client_secret
from botStrings import help_message, empty_report, price_report, error_too_high, error_invalid_input, lets_talk, thanks_copy

from discord.ext import commands, tasks

# TODO: Make this not hardcoded; use Discord roles instead
channelId = 693905240650416171

bot = commands.Bot(command_prefix='$')
bot.remove_command("help")

# TODO: Stop relying only on in-memory cache, use database configuration
turnipPrices = {}

@bot.event
async def on_ready():
    print("The stalk market analyzer is up and running!")
    printReport.start()

@bot.command(pass_context=True)
async def report(ctx):
    if not bool(turnipPrices):
        await ctx.message.channel.send(empty_report)
    else:
        await ctx.message.channel.send(price_report.format(printDictionary(turnipPrices)))

@bot.command(pass_context=True)
async def help(ctx):
    await bot.get_channel(channelId).send(help_message)

@bot.command(pass_context=True)
async def talks(ctx, price):
    if price.isdigit():
        priceAsInt = int(price)
        if (priceAsInt > 10000):
            await ctx.message.author.send(error_too_high)
            await ctx.message.add_reaction("\U0001F44E")
        else:
            turnipPrices[ctx.message.author.name] = price
            await ctx.message.add_reaction("\U0001F44D")
    else:
        await ctx.message.author.send(error_invalid_input)
        await ctx.message.add_reaction("\U0001F44E")

@bot.command(pass_context=True)
async def letsTalk(ctx):
    await ctx.message.author.send(lets_talk)

@bot.command(pass_context=True)
async def thanks(ctx):
    await ctx.message.author.send(thanks_copy)

@tasks.loop(seconds=60.0)
async def printReport():
    currentTime = datetime.datetime.now()
    firstTurnipTime = currentTime.replace(hour=15, minute=30, second=0, microsecond=0)
    firstTurnipTimeEnd = currentTime.replace(hour=15, minute=31, second=0, microsecond=0)
    secondTurnipTime = currentTime.replace(hour=21, minute=0, second=0, microsecond=0)
    secondTurnipTimeEnd = currentTime.replace(hour=21, minute=1, second=0, microsecond=0)

    if is_in_time(currentTime, firstTurnipTime, firstTurnipTimeEnd) or is_in_time(currentTime, secondTurnipTime, secondTurnipTimeEnd):
        prettyMap = printDictionary(turnipPrices)
        if prettyMap.strip():
            await bot.get_channel(channelId).send(prettyMap)
        clearMap()

def is_in_time(currentTime, targetTime, targetTimeThreshold):
    return (currentTime >= targetTime and currentTime <= targetTimeThreshold)

def printDictionary(dict):
    str = ""
    for item, amount in dict.items():
        str += "{} : {} Bells".format(item, amount)
        str += "\n"
    return str

def clearMap():
    turnipPrices.clear()

bot.run(client_secret)
