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
async def played(ctx, server: typing.Optional[str] = None, user: typing.Optional[str] = None,):
    current_guild = quark.get_guild(ctx.message.guild.id) if server is None else server
    member_name = None if user is None else user
    print(
        f'User {ctx.message.author.name} asked for played information for *{current_guild}*')
    totals_dict = qm.calculate_all_activities(member_name=user, current_guild=current_guild)
    message = ''
    for key, value in totals_dict.items():
        message += f'**{key}**: {value}minutes\n'
    await ctx.send(f'> Played time on {current_guild}:\n{message}')


@quark.command()
async def bar(ctx, user: typing.Optional[str] = None, server: typing.Optional[str] = None):
    current_guild = quark.get_guild(ctx.message.guild.id) if server is None else server
    print(
        f'User {ctx.message.author.name} asked for barchart for *{current_guild}*')
    totals = qm.calculate_all_activities(
        member_name=user, current_guild=current_guild)
    barchart_file = draw_horizontal_barchart(
        totals, current_guild=current_guild, member=user, bar_colors=qenv.bar_colors)
    await ctx.send(f'Here\'s the latest info from the past week!\n')
    await ctx.send(file=discord.File(barchart_file))
    cleanup_file(barchart_file)


@quark.command()
async def p2(ctx, power: int):
    await ctx.send(f'> 2 to the power of {power} equals to: **{2**power}**')


@quark.command()
async def rule(ctx, rule_number: typing.Optional[int] = 0):
    await ctx.send(rules(rule_number))

# Call for rom to do duties and give him quark and bot_id
rom = Rom(quark, qenv.bot_id, infdb=influx_info)

if __name__ == '__main__':
    try:
        print(f'Starting Quark the Bot. Ctrl + C to exit the program.')
        quark.run(qenv.token)
    except:
        print(f'Could not start the bot, check .env file for settings...')
