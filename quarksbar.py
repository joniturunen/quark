from discord.ext import tasks, commands
from influxdb import DataFrameClient
from datetime import datetime, timezone
import settings
from qintel import QuarksMonitors
import discord
import pandas as pd
from barchart import draw_horizontal_barchart, cleanup_file

"""
Rom works at Quarks bar and keeps his ferengi ears
open for business proposals. Rom's task is to monitor
member activities and file them in ledger (influxdb).
"""
qenv = settings.Qenvs()
qm = QuarksMonitors(infdb=qenv.influx_info)

class Rom(commands.Cog):
    def __init__(self, quark, bot_id, infdb):
        self.monitor_index = 0
        self.tasklist_index = 0
        self.quark = quark
        self.quarks_id = bot_id
        self.tasklist_last_run = datetime(2021,12,24)

        self.monitor.start()
        self.tasklist.start()

        self.infdb = infdb
        self.influxdb_client = DataFrameClient(
            infdb.get('host'), infdb.get('port'), infdb.get('user'), infdb.get('pass'), infdb.get('db'))

    def cog_unload(self):
        self.monitor.cancel()
        self.tasklist.cancel()

    @tasks.loop(seconds=qenv.tasking_interval)
    async def tasklist(self):
        now = datetime.now()
        if now.isoweekday() is qenv.tasklist_weekday:
            if now.hour in range(qenv.tasklist_hour,qenv.tasklist_hour+2):
                delta = now - self.tasklist_last_run
                if delta.days > 1:
                    totals = qm.calculate_all_activities(member_name=None, current_guild=self.query_guild)
                    print(f'Announcing last weeks stats for the guild: {self.query_guild} at channel {self.home_channel}')
                    barchart_file = draw_horizontal_barchart(totals, current_guild=self.query_guild, member=None, bar_colors=qenv.bar_colors)
                    await self.home_channel.send(f'**Here\'s the latest played 📊 chart from the past week!**')
                    await self.home_channel.send(file=discord.File(barchart_file))
                    self.tasklist_last_run = now
                    print(f'set the tasklist_last_run to: {self.tasklist_last_run}')
        self.tasklist_index += 1

    @tasklist.before_loop
    async def before_tasklist(self):
        print('Tasklist is waiting at the bar...')
        await self.quark.wait_until_ready()
        # These need to wait for Quark to be ready until set
        self.home_channel = self.quark.get_channel(qenv.report_to_channel)
        self.home_guild = self.quark.get_guild(qenv.report_to_guild)
        # Define here what guild stats should be used for automatic bar charts
        self.query_guild = self.quark.get_guild(qenv.tasklist_monitored_guild)
        print(f'Tasklist is set to report to channel: \'{self.home_channel}\' at {self.home_guild}.')

    @tasks.loop(seconds=qenv.monitor_interval)
    async def monitor(self):
        print(f'{datetime.now()} :: Monitoring game activities in: {self.monitored_servers}')
        for guild in self.quark.guilds:
            if guild.name in self.monitored_servers:
                for member in guild.members:
                    # todo: Add a if role not bot or not in users
                    if member.id != int(self.quarks_id):
                        custom_status = True if isinstance(
                            member.activity, discord.activity.CustomActivity) else False
                        if custom_status is False:
                            activity = member.activity
                            activity = member.activity.name.replace(
                                "'", "`").replace("®", "") if member.activity else None
                        rfc3339 = datetime.now(timezone.utc).astimezone()
                        data = {'member_name': member.name, 'member_id': str(member.id),
                                'member_activity': activity, 'member_server': guild.name, 'rfc3339': str(rfc3339)}
                        df = pd.DataFrame(
                            data, index=[rfc3339])
                        if activity is not None:
                            self.store_to_db(df, guild.name)
        self.monitor_index += 1
        

    @monitor.before_loop
    async def before_monitor(self):
        print(f'Rom is waiting for Quark to open the bar...')
        await self.quark.wait_until_ready()
        self.monitored_servers = self.check_what_servers_to_monitor()

    def store_to_db(self, df, current_server):
        try:
            self.influxdb_client.write_points(
                df, measurement=current_server, database=self.infdb.get('db'), protocol='line')
        except:
            print(
                f'Error happened while trying to write_points() with the df: \n{df}')
            self.cog_unload()
            exit(1)

    def check_what_servers_to_monitor(self):
        # Here we form a new list based on list of classes that
        # represent servers the bot can see. We filter out the ones
        # listed in environment variables that we wish not to monitor
        print(f'Check check check')
        guilds = [
            s.name for s in self.quark.guilds if s.name not in qenv.do_not_monitor_these_servers]
        print(f"Bar is open and Rom is monitoring members at following servers: {', '.join(guilds)}")
        return guilds

