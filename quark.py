import typing
import settings
import ytsearcher
from discord.ext import commands
from acquisition import rules

qenv = settings.Qenvs()
quark = commands.Bot(command_prefix='!', description=qenv.desc)


@quark.command()
async def ping(ctx):
    await ctx.send('pong')


@quark.command()
async def yt(ctx, search_term: str):
    yt = ytsearcher.YoutubeSearch()
    video_id = yt.search(search_term)
    await ctx.send(f'Youtube query with search term *{search_term}*". First hit was this:\nhttps://youtu.be/{video_id}')


@quark.command()
async def p2(ctx, power: int):
    await ctx.send(f'Two to the power of {power} equals to {2**power}')


@quark.command()
async def rule(ctx, rule_number: typing.Optional[int] = 0):
    await ctx.send(rules(rule_number))


if __name__ == '__main__':
    try:
        print(f'Starting Quark the Bot. Ctrl + C to exit the program.')
        quark.run(qenv.token)
    except:
        print(f'Could not start the bot, check .env file for settings...')
