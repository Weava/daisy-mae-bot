
import discord
import time
import aioschedule as schedule
import datetime
import asyncio
import creds

from discord.ext import commands, tasks

channelId = 693905240650416171
bot = commands.Bot(command_prefix='$')
bot.remove_command("help")
turnipPrices = {}

@bot.event
async def on_ready():
    print("The stalk market analyzer is up and running!")
    printReport.start()

@bot.command(pass_context=True)
async def report(ctx):
    if not bool(turnipPrices):
        await ctx.message.author.send( "Oh no! No one has reported any turnip prices! Maybe you can be the first?")
        await ctx.message.add_reaction("\U0001F44D")
    else:
        await ctx.message.author.send("Here are your turnip prices for the day! \n{}".format(printDictionary(turnipPrices)))
        await ctx.message.add_reaction("\U0001F44D")

@bot.command(pass_context=True)
async def help(ctx):
    message = """\n
    Hi! Daisy Mae here! Great to see you're taking an interest in the Stalk Market!
    This is a little tool I built to help you report the stalk price for turnips on your island, and share with all your friends!
    I'll automatically report the prices twice a day, based on fluctuations in the stalk market.

    Here's some things I can do for you

    $talks <Turnip price at current time> - I'll keep a record of your latest turnip price until the next change in the market (Example: $talks 420)
    $report - I'll report the stalk market prices directly to you!
    $letsTalk - Everyone needs a good chat now and then :)
    $thanks - A little thank you message!
    """
    await bot.get_channel(channelId).send(message)

@bot.command(pass_context=True)
async def talks(ctx, price):
    if price.isdigit():
        priceAsInt = int(price)
        if (priceAsInt > 10000):
            await ctx.message.author.send("The stalk market isn't THAT good. Maybe try something a bit smaller?")
            await ctx.message.add_reaction("\U0001F44E")
        else:
            turnipPrices[ctx.message.author.name] = price
            await ctx.message.add_reaction("\U0001F44D")
    else:
        await ctx.message.author.send("I only take and report turnip prices. Are you confusing me with someone else?")
        await ctx.message.add_reaction("\U0001F44E")

@bot.command(pass_context=True)
async def letsTalk(ctx):
    await ctx.message.author.send("You are a beautiful, lovely person, and you make everyone around you shine!")

@bot.command(pass_context=True)
async def thanks(ctx):
    await ctx.message.author.send("Thank you for using me for all your stalk market needs! I'm still a little new at this and not quite fully up to speed yet, so let me know if there's anything I can improve on by sending a letter to my assistant, Weava.")

@tasks.loop(seconds=5.0)
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
