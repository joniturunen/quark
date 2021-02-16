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
        if ' ' in message.content:
            rule_number = int(message.content.split(" ")[1])
            await message.channel.send('**' + getRuleOfAcquisition(rule_number)["rule"] + '**\n> *Rule of acquisition number* ***' + str(rule_number) + '***')
        else:
            rand = random.randint(1, 126)
            await message.channel.send('**' + getRuleOfAcquisition(rand)["rule"] + '**\n> *Rule of acquisition number* ***' + str(rand) + '***')

    if message.content.startswith(quarkCommands["hello"]):
        await message.channel.send('I think I figured out why Humans don\'t like Ferengi.\nThe way I see it, Humans used to be a lot like Ferengi: greedy, acquisitive, interested only in profit. We\'re a constant reminder of a part of your past you\'d like to forget.\nHumans used to be a lot worse than the Ferengi: slavery, concentration camps, interstellar wars. We have nothing in our past that approaches that kind of barbarism. You see? We\'re nothing like you... we\'re better.')

if __name__ == '__main__':
    client.run(TOKEN)

