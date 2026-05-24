#!/usr/bin/env python3
import requests
import os
import sys
import random
from datetime import datetime, timedelta
import pytz
import time  # Import time for sleep function

TEAM_ID = "darkonteams"

# Token aus ENV
API_TOKEN = os.getenv("KEY")
if not API_TOKEN:
    sys.exit("Error: API token not found. Please set KEY environment variable.")

# Turnieroptionen mit klaren Namen
OPTIONS = [

    {"name": "10 DOLLARS SWISS QUALIFIER",                "clock": {"limit": 180,  "increment": 0},  "nbRounds": 13},#3+0
    {"name": "10 DOLLARS SWISS QUALIFIER",                "clock": {"limit": 180,  "increment": 2},  "nbRounds": 11},#3+2
    {"name": "10 DOLLARS SWISS QUALIFIER",                "clock": {"limit": 300,  "increment": 3},  "nbRounds": 9},#5+3
    {"name": "10 DOLLARS SWISS QUALIFIER",                "clock": {"limit": 600,  "increment": 0},  "nbRounds": 9}, #10+0
    {"name": "10 DOLLARS SWISS QUALIFIER",                "clock": {"limit": 600,  "increment": 5},  "nbRounds": 7}, #10+5
    {"name": "10 DOLLARS SWISS QUALIFIER",                "clock": {"limit": 1800, "increment": 0},  "nbRounds": 5}, #30+0
   
]

def utc_millis_for_hour(hour):
    utc = pytz.utc
    now = datetime.now(utc)
    tomorrow = now + timedelta(days=1)
    start = datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour, 45, tzinfo=utc)
    return int(start.timestamp() * 1000), start

def read_description():
    path = os.path.join(os.path.dirname(__file__), "description.txt")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Welcome to our Swiss tournament!"

def create_swiss():
    for hour in range(24):
        option = random.choice(OPTIONS)
        startDate, start_dt = utc_millis_for_hour(hour)
        payload = {
            "name": f"{option['name']} ",
            "clock.limit": option["clock"]["limit"],
            "clock.increment": option["clock"]["increment"],
            "nbRounds": option["nbRounds"],
            "rated": "true",
            "description": read_description(),
            "startsAt": startDate,
            "conditions.playYourGames": "true"
        }
        url = f"https://lichess.org/api/swiss/new/{TEAM_ID}"
        headers = {"Authorization": f"Bearer {API_TOKEN}"}

        print(f"➡ Creating: {payload['name']} "
              f"({payload['clock.limit']//60}+{payload['clock.increment']}, "
              f"{payload['nbRounds']}R, Start {start_dt} UTC)")

        r = requests.post(url, data=payload, headers=headers)

        if r.status_code == 200:
            data = r.json()
            print("✅ Tournament created!")
            print("URL:", f"https://lichess.org/swiss/{data.get('id')}")
        else:
            print("❌ Error:", r.status_code, r.text)

        time.sleep(1)  # Wait 2 seconds between requests to avoid simultaneous creation

if __name__ == "__main__":
    create_swiss()
