"""
generates csv of format
name, hacker_info
ex row: john smith, 12938378

hacker_info will be continually changed based on our needs
expected values are crc, email
"""

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
hacker_info = [hacker for hacker in hacker_info if hacker[1]['rating'] == '10']

# get relevant info
names = [hacker[1]['fname'] + ' ' + hacker[1]['lname'] for hacker in hacker_info]
emails = [hacker[1]['emailAddress'] for hacker in hacker_info]
crc_codes = [binascii.crc32(hacker[0].encode('utf8')) for hacker in hacker_info]

# formatting
d = {
    'name': names,
    'email': emails,
    'check-in code': crc_codes
}

df = pd.DataFrame(d)
df.to_csv('results.csv')

print(df)
