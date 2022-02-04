"""
Connects to hacker application database and provides functions for downloading data.
"""

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import binascii


def generate_code(key):
    return f'{binascii.crc32(key.encode("utf8")):08x}'


def connect_to_firestore():
    # connects to and returns a reference to the database client
    cred = credentials.Certificate(
        "sbhacks-viii-site-firebase-adminsdk-private-key.json"
    )
    firebase_admin.initialize_app(cred)
    return firestore.client()


def fetch_applications(db):
    # returns a dict of applications
    docs = list(db.collection("hackers").stream())
    apps = dict(map(lambda doc: (generate_code(doc.id), doc.to_dict()), docs))
    assert len(docs) == len(apps)
    return apps

def fetch_applications2(db):
    # returns a dict of applications
    docs = list(db.collection("hackers").stream())
    apps = dict(map(lambda doc: (generate_code(doc.id), (doc.to_dict(), doc.id)), docs))
    assert len(docs) == len(apps)
    return apps


def is_accepted(app):
    # returns if the application is accepted
    return app["rating"] == "10"

def is_nonpriority(app):
    # returns if the application is nonpriority
    return "nonPriority" in app and app["nonPriority"]


def filter_accepted(apps):
    # filters the dict of applications by accepted
    # return dict(filter(lambda item: is_accepted(item[1]) and is_nonpriority(item[1]), apps.items()))
    return dict(filter(lambda item: is_accepted(item[1]), apps.items()))


def get_full_name(app):
    return app["fname"] + " " + app["lname"]
