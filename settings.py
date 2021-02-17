from dotenv import dotenv_values
from pathlib import Path


class Qenvs:
    env_path = Path('.') / '.env'
    envs = dotenv_values(env_path)

    def __init__(self):
        self.token = self.envs['DISCORD_TOKEN']
        self.desc = self.envs['BOT_DESC']
        self.google_api_key = self.envs['GOOGLE_API_KEY']
