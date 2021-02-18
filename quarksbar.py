from discord.ext import tasks, commands
import time
import pandas as pd


class Rom(commands.Cog):
    def __init__(self, quark, bot_id, monitored_server):
        self.index = 0
        self.quark = quark
        self.quarks_id = bot_id
        self.srv = monitored_server
        self.monitor.start()

    def cog_unload(self):
        self.monitor.cancel()

    @tasks.loop(seconds=5.0)
    async def monitor(self):
        # print(self.index)
        for guild in self.quark.guilds:
            if str(guild) == self.srv:
                for member in guild.members:
                    if member.id != int(self.quarks_id):
                        ts = pd.Timestamp(time.time(), unit='s')
                        print(
                            f'{ts}:: Rom monitored member {member} (ID:{member.id}) doing {member.activity} at **{self.srv}**')
        self.index += 1

    @monitor.before_loop
    async def before_monitor(self):
        print('Rom is waiting for Quark...')
        await self.quark.wait_until_ready()
