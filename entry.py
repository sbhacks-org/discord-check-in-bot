"""
Read in manually-added entries for judges, mentors, etc.
"""

import json
from db import generate_code
import pandas as pd


def read_entries():
    # read from manual entries:
    entries = {}
    with open("data/entries.json") as entry_file:
        entry_roles = json.load(entry_file)
        for role in entry_roles:
            for name in entry_roles[role]:
                entries[generate_code(name + "#" + role)] = {
                    "name": name,
                    "role": role,
                }
    return entries
