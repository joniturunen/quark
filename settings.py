from dotenv import dotenv_values
from pathlib import Path


class Qenvs:
    env_path = Path('.') / '.env'
    envs = dotenv_values(env_path)

    def __init__(self, ):
        self.token = self.envs['DISCORD_TOKEN']
        self.server = self.envs['DISCORD_SERVER']
        self.filters = self.envs['ACTIVITY_FILTERS']
        self.desc = self.envs['BOT_DESC']
        self.google_api_key = self.envs['GOOGLE_API_KEY']
        self.owner = int(self.envs['BOT_OWNER_ID'])
        self.owner_name = self.envs['BOT_OWNER_NAME']
        self.bot_id = int(self.envs['BOT_ID'])
        self.influxdb_host = self.envs['INFLUXDB_HOST']
        self.influxdb_port = int(self.envs['INFLUXDB_PORT'])
        self.influxdb_user = self.envs['INFLUXDB_USER']
        self.influxdb_pass = self.envs['INFLUXDB_PASS']
        self.influxdb_name = self.envs['INFLUXDB_NAME']
        self.monitor_interval = int(
            self.envs['MONITORING_INTERVAL_IN_SECONDS'])


if __name__ == '__main__':
    try:
        q = Qenvs()
        print(q.envs)
    except:
        print(f'Check that you have .env!')
