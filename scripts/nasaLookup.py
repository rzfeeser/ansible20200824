#!/usr/bin/python3

import requests

astros = requests.get("http://api.open-notify.org/astros.json")
issriders = astros.json()

for astro in astros.json()["people"]:
    print(astro['name'].split()[-1])

