import discord

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import pandas as pd
import binascii

# Use a service account
cred = credentials.Certificate('sbhacks-viii-site-firebase-adminsdk-private-key.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

hackers_ref = db.collection(u'hackers')
docs = hackers_ref.stream()

# get accepted hackers
hacker_info = [(doc.id, doc.to_dict()) for doc in docs]
hackers = [hacker for hacker in hacker_info if hacker[1]['rating'] == '10']


client = discord.Client()

@client.event
async def on_ready():
    print("LOGGED IN. READY.")

@client.event
async def on_message(message):
    # ignore if message is coming from self
    if message.author == client.user:
        return

    # ignore if message is not a dm
    if message.channel.type != discord.ChannelType.private:
        return

    email, code, role = [(s[0].strip(), s[1].strip(), s[2].strip()) for s in message.split(',')]
    print(f'received input {email}, {code}, {role}')

    if role == 'hacker':
        


    

client.run('insert token here')