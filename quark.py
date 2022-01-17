from time import sleep
from discord import message
from barchart import draw_horizontal_barchart, cleanup_file
from qintel import QuarksMonitors
from quarksbar import Rom
from discord.ext import commands, tasks
from acquisition import rules
from datetime import datetime as dt
import settings, ytsearcher
import discord, typing


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
async def admin(ctx):
    print(f'({ctx.message.author.name}) asked for command !admin')
    if ctx.message.author.id == quark.owner_id:
        await ctx.send(f'What will it be my dear friend **{qenv.owner_name}**?')
    else:
        await ctx.send(f'This command is restricted for exclusive members only.')

@quark.command()
async def yt(ctx, search_term: str):
    print(f'{ctx.message.author.name} asked for command !yt')
    if ctx.message.author.id == quark.owner_id:
        yt = ytsearcher.YoutubeSearch()
        video_id = yt.search(search_term)
        await ctx.send(f'Youtube query with search term *{search_term}*. First hit was this:\nhttps://youtu.be/{video_id}')
    else:
        await ctx.send(f'This command is restricted for exclusive members only.')

@quark.command()
async def played(ctx, user: typing.Optional[str] = None,server: typing.Optional[str] = None):
    user = None if user in ['all', 'All', 'kaikki', '*', 'everyone'] else user
    current_guild = quark.get_guild(ctx.message.guild.id) if server is None else server
    print(
        f'User {ctx.message.author.name} asked for played information for *{current_guild}*')
    totals_dict = qm.calculate_all_activities(member_name=user, current_guild=current_guild)
    header = 'P' if user is None else str(user)+'`s p'
    message = ''
    for key, value in totals_dict.items():
        time_type = ' minutes' if value < 180 else ' hours'
        value = value if value < 180 else value/60
        message += f' {key} ::: {round(value,2)}{time_type}\n'
    await ctx.send(f'** {header}layed 📈 from past week tracked from server _{current_guild}_ !**:\n```{message}```')

@quark.command()
async def bar(ctx, user: typing.Optional[str] = None, server: typing.Optional[str] = None,):
    user = None if user in ['all', 'All', 'kaikki', '*', 'everyone'] else user
    current_guild = quark.get_guild(ctx.message.guild.id) if server is None else server
    print(f'User {ctx.message.author.name} asked Rom for bar chart intel about *{current_guild}*')
    print(f'Guild type: {type(current_guild)}')
    if ctx.message.author.id == quark.owner_id:   
        totals = qm.calculate_all_activities(
            member_name=user, current_guild=current_guild)
        barchart_file = draw_horizontal_barchart(
            totals, current_guild=current_guild, member=user, bar_colors=qenv.bar_colors)
        await ctx.send(f'**Here\'s the latest 📊 chart from the past week!**')
        await ctx.send(file=discord.File(barchart_file))
        cleanup_file(barchart_file)
    else:
        await ctx.send(f'This command is restricted for exclusive members only.')
        print(f'User {ctx.message.author.name} was denied the right to use !bar command')

@quark.command()
async def p2(ctx, power: int):
    if power < 1024 and power > 0:
        await ctx.send(f'{power}² equals to: **{2**power}**')
    else: 
        await ctx.send(f"You ask me what is {power}²? I'm not a Star Fleet science officer! I can\'t give answers to such things!")

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
