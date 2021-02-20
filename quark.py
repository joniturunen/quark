import typing
import settings
import ytsearcher
import discord
from quarksbar import Rom
from discord.ext import commands, tasks
from acquisition import rules

all_intents = discord.Intents.all()
qenv = settings.Qenvs()

quark = commands.Bot(command_prefix='!',
                     description=qenv.desc, intents=all_intents, owner_id=qenv.owner)
influx_info = {'host': qenv.influxdb_host, 'port': qenv.influxdb_port,
               'user': qenv.influxdb_user, 'pass': qenv.influxdb_pass, 'db': qenv.influxdb_name}


@quark.command()
async def ping(ctx):
    await ctx.send('pong')


@quark.command()
async def yt(ctx, search_term: str):
    yt = ytsearcher.YoutubeSearch()
    video_id = yt.search(search_term)
    await ctx.send(f'Youtube query with search term *{search_term}*. First hit was this:\nhttps://youtu.be/{video_id}')


@quark.command()
async def rom(ctx, server: typing.Optional[str] = qenv.server):
    # Do some stuff with Rom, ask most played or something
    await ctx.send('Not implemented yet')


@quark.command()
async def p2(ctx, power: int):
    await ctx.send(f'>2 to the power of {power} equals to: **{2**power}**')


@quark.command()
async def rule(ctx, rule_number: typing.Optional[int] = 0):
    await ctx.send(rules(rule_number))

# Call for rom to do duties and give him quark and bot_id
rom = Rom(quark, qenv.bot_id, monitored_server='3sum',
          infdb=influx_info)

if __name__ == '__main__':
    try:
        print(f'Starting Quark the Bot. Ctrl + C to exit the program.')
        quark.run(qenv.token)
    except:
        print(f'Could not start the bot, check .env file for settings...')
