from discord.ext import tasks, commands
from influxdb import DataFrameClient
from datetime import datetime, timezone
from settings import Qenvs
import discord
import pandas as pd


interval = Qenvs().monitor_interval


class Rom(commands.Cog):
    def __init__(self, quark, bot_id, monitored_server, infdb):
        self.index = 0
        self.quark = quark
        self.quarks_id = bot_id
        self.srv = monitored_server
        self.monitor.start()
        self.infdb = infdb
        self.influxdb_client = DataFrameClient(
            infdb.get('host'), infdb.get('port'), infdb.get('user'), infdb.get('pass'), infdb.get('db'))

    def cog_unload(self):
        self.monitor.cancel()

    @tasks.loop(seconds=interval)
    async def monitor(self):
        for guild in self.quark.guilds:
            if str(guild) == self.srv:
                for member in guild.members:
                    if member.id != int(self.quarks_id):
                        custom_status = True if isinstance(
                            member.activity, discord.activity.CustomActivity) else False
                        activity = member.activity if custom_status is not True else None
                        activity = member.activity.name.replace(
                            "'", "`") if member.activity else None
                        rfc3339 = datetime.now(timezone.utc).astimezone()
                        data = {'member_name': member.name, 'member_id': str(member.id),
                                'member_activity': activity, 'member_server': self.srv, 'rfc3339': str(rfc3339)}
                        df = pd.DataFrame(
                            data, index=[rfc3339])
                        # print(df)
                        self.store_to_db(df, self.srv)
        self.index += 1

    @monitor.before_loop
    async def before_monitor(self):
        print('Rom is waiting for Quark...')
        await self.quark.wait_until_ready()

    def store_to_db(self, df, server):
        try:
            self.influxdb_client.write_points(
                df, measurement=server, database=self.infdb.get('db'), protocol='line')
        except:
            print(
                f'Error happened while trying to write_points() with the df: \n{df}')
            self.cog_unload()
            exit(1)