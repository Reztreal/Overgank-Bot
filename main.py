import os
from function import checkEnemy
from discord.ext import commands
from keep_alive import live

bot_token = os.environ['TOKEN']
client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print("Bot is ready.")


@client.command()
async def use(ctx):
    await ctx.send(
        "To use the bot: !analyze 'nickname' 'region'. Don't forget to include quotes otherwise the bot won't work if you have a space in your nickname"
    )


@client.command()
async def analyze(ctx, arg1, arg2):
    await ctx.send('You passed -{}- and -{}-'.format(arg1, arg2))
    players = checkEnemy(arg1, arg2)
    await ctx.send(f"```\n{players}\n```")

live()
client.run(bot_token)

