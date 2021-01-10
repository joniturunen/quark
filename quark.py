import discord
import os
import random
from dotenv import dotenv_values
from pathlib import Path
from triggers import quarkCommands
from rulesOfAcquisition import getRuleOfAcquisition

env_path = Path('.') / '.env'
envs = dotenv_values(env_path)
TOKEN = envs['DISCORD_TOKEN']
CHANNELS = (envs['DISCORD_CHANNELS']).split(',')
r = random.randint(1, 126)

print(
    f'Channels: {CHANNELS}\nDiscord token: {TOKEN[:7] + (len(TOKEN)-7)*"*"}\nTesting rule {r}: {getRuleOfAcquisition(r)["rule"]}\nTrigger: {quarkCommands}')

client = discord.Client()


@client.event
async def on_ready():
    print('Quark is logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(quarkCommands["rule"]):
        rand = random.randint(1, 126)
        await message.channel.send(getRuleOfAcquisition(rand)["rule"] + '\nRule of acquisition #' + str(rand))

    if message.content.startswith(quarkCommands["hello"]):
        await message.channel.send('Well hello there, what can I get you?\nJust kidding I dont get anything.')

if __name__ == '__main__':
    client.run(TOKEN)
