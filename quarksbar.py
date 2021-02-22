from discord.ext import tasks, commands
from influxdb import DataFrameClient
from datetime import datetime, timezone
from settings import Qenvs
import discord
import pandas as pd


interval = Qenvs().monitor_interval

"""
Rom works at Quarks bar and keeps his ferengi ears
open for business proposals. Rom's task is to monitor
member activities and file them in ledger (influxdb).
"""


class Rom(commands.Cog):
    def __init__(self, quark, bot_id, infdb):
        self.index = 0
        self.quark = quark
        self.quarks_id = bot_id

        self.monitor.start()
        self.infdb = infdb
        self.influxdb_client = DataFrameClient(
            infdb.get('host'), infdb.get('port'), infdb.get('user'), infdb.get('pass'), infdb.get('db'))

    def cog_unload(self):
        self.monitor.cancel()

    @tasks.loop(seconds=interval)
    async def monitor(self):
        for guild in self.quark.guilds:
            if guild.name in self.monitored_servers:
                for member in guild.members:
                    if member.id != int(self.quarks_id):
                        custom_status = True if isinstance(
                            member.activity, discord.activity.CustomActivity) else False
                        if custom_status is False:
                            activity = member.activity
                            activity = member.activity.name.replace(
                                "'", "`") if member.activity else None
                        rfc3339 = datetime.now(timezone.utc).astimezone()
                        data = {'member_name': member.name, 'member_id': str(member.id),
                                'member_activity': activity, 'member_server': guild.name, 'rfc3339': str(rfc3339)}
                        df = pd.DataFrame(
                            data, index=[rfc3339])
                        # print(df)
                        self.store_to_db(df, guild.name)
        self.index += 1

    @ monitor.before_loop
    async def before_monitor(self):
        print(f'Rom is waiting for bar to open...')
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
        q = Qenvs()
        guilds = [
            s.name for s in self.quark.guilds if s.name not in q.do_not_monitor_these_servers]
        print(
            f"Bar is open and Rom is monitoring members at following servers: {', '.join(guilds)}")
        return guilds
