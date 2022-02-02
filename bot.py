# bot.py
# Reference: https://realpython.com/how-to-make-a-discord-bot-python/

import os, re, sys

import discord
from dotenv import load_dotenv

from db import *

db = connect_to_firestore()

from entry import read_entries

entries = read_entries()  # get manual entries for judges, etc.

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

intents = discord.Intents.all()
client = discord.Client(intents=intents)
guild = None
roles = {
    "hacker": None,
    "judge": None,
    "sponsor": None,
    "mentor": None,
}


@client.event
async def on_ready():
    # Locate the server for SB Hacks VIII:
    global guild, roles
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name} (id: {guild.id})",
        file=sys.stderr,
    )

    for role in guild.roles:
        if role.name in roles:
            roles[role.name] = role


code_pattern = re.compile("^[0-9a-f]{8}$")


@client.event
async def on_message(message):
    global apps

    # ignore if the message is coming from us:
    if message.author == client.user:
        return

    # only respond if the message is a DM:
    if message.channel.type != discord.ChannelType.private:
        return

    # make sure member is part of the guild:
    member = guild.get_member(message.author.id)
    if member is None:
        return

    print(
        f"Received message from {message.author.id} ({message.author.name}).",
        file=sys.stderr,
    )

    # if message is not a valid code:
    if code_pattern.match(message.content.lower().strip()) is None:
        await message.channel.send(
            "That does not appear to be a valid check-in code. Please send the eight-digit code you received in your acceptance email."
        )
        return

    code = message.content.lower().strip()
    if code in apps:
        # if the code is in apps, give them a hacker role, and set their username
        full_name = get_full_name(apps[code][0])
        await member.add_roles(roles["hacker"])
        await member.edit(nick=full_name)
        
        # TODO: update the db entry to include that they checked in
        db.collection('hackers').document(apps[code][1]).update({
            'check-in': True,
            'discord_name': message.author.id,
        })

        print(
            f'User {message.author.id}, aka "{full_name}" ({message.author.name}) checked in successfully.',
            file=sys.stderr,
        )
        await message.channel.send("Thank you for checking in!")
    elif code in entries:
        await member.add_roles(roles[entries[code]["role"]])
        await member.edit(nick=entries[code]["name"])
        print(
            f"User {message.author.id}, aka \"{entries[code]['name']}\" ({message.author.name}) checked in successfully.",
            file=sys.stderr,
        )
        await message.channel.send("Thank you for checking in!")
    else:
        await message.channel.send(
            "That is not a valid check-in code. Please send the eight-digit code you received in your acceptance email."
        )
        return


from timer import RepeatedTimer


def reconnect():
    global db, apps
    print("Reconnecting to database.")
    apps = fetch_applications2(db)  # need to update regularly


timer = RepeatedTimer(1000, reconnect)
try:
    client.run(TOKEN)
finally:
    timer.stop()
