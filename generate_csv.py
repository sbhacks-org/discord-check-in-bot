"""
generates csv of format
name, hacker_info
ex row: john smith, 12938378

hacker_info will be continually changed based on our needs
expected values are crc, email
"""

from db import *
from entry import read_entries
import pandas as pd


def generate_apps_csv(apps):
    # writes a list of applications to results.csv
    apps = filter_accepted(apps)  # filter for accepted apps

    # get relevant info
    names = list(map(lambda app: app["fname"] + " " + app["lname"], apps.values()))
    emails = list(map(lambda app: app["emailAddress"], apps.values()))
    codes = list(apps.keys())

    # formatting
    df = pd.DataFrame({"name": names, "email": emails, "check-in code": codes})
    df.to_csv("data/results.csv")
    print(df)


def generate_entry_csv(entries):
    # writes a list of manual entries to entries.csv
    names = list(map(lambda entry: entry["name"], entries.values()))
    roles = list(map(lambda entry: entry["role"], entries.values()))
    codes = list(entries.keys())

    # formatting
    df = pd.DataFrame({"name": names, "role": roles, "check-in code": codes})
    df.to_csv("data/entries.csv")
    print(df)


if __name__ == "__main__":
    db = connect_to_firestore()
    apps = fetch_applications(db)
    generate_apps_csv(apps)

    entries = read_entries()
    generate_entry_csv(entries)
