from time import sleep
import typing

from discord import message
import settings
import ytsearcher
import discord
from barchart import draw_horizontal_barchart, cleanup_file
from qintel import QuarksMonitors
from quarksbar import Rom
from discord.ext import commands, tasks
from acquisition import rules


all_intents = discord.Intents.all()
qenv = settings.Qenvs()
influx_info = {'host': qenv.influxdb_host, 'port': qenv.influxdb_port,
               'user': qenv.influxdb_user, 'pass': qenv.influxdb_pass, 'db': qenv.influxdb_name}
qm = QuarksMonitors(infdb=influx_info)

quark = commands.Bot(command_prefix='!',
                     description=qenv.desc, intents=all_intents, owner_id=qenv.owner)


@quark.command()
async def ping(ctx):
    current_guild = quark.get_guild(ctx.message.guild.id)
    print(
        f'User {ctx.message.author.name} called command `ping` at *{current_guild}*')
    await ctx.send(f'pong  *{ctx.message.author.name}*')


@quark.command()
async def yt(ctx, search_term: str):
    yt = ytsearcher.YoutubeSearch()
    video_id = yt.search(search_term)
    await ctx.send(f'Youtube query with search term *{search_term}*. First hit was this:\nhttps://youtu.be/{video_id}')


@quark.command()
async def played(ctx, user: typing.Optional[str] = None, server: typing.Optional[str] = qenv.server):
    totals_dict = qm.calculate_all_activities(member_name=user)
    message = ''
    for key, value in totals_dict.items():
        message += f'**{key}**: {value}minutes\n'
    await ctx.send(f'> Play times since 21.2.2021\n{message}')


@quark.command()
async def bar(ctx, user: typing.Optional[str] = None):
    current_guild = quark.get_guild(ctx.message.guild.id)
    print(
        f'User {ctx.message.author.name} asked for barchart at *{current_guild}*')
    totals = qm.calculate_all_activities(
        member_name=user, current_guild=current_guild)
    barchart_file = draw_horizontal_barchart(totals, member=user)
    await ctx.send(f'Here\'s the latest info, but you didn\'t here it from me!\n')
    await ctx.send(file=discord.File(barchart_file))
    cleanup_file(barchart_file)


@quark.command()
async def p2(ctx, power: int):
    await ctx.send(f'> 2 to the power of {power} equals to: **{2**power}**')


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
