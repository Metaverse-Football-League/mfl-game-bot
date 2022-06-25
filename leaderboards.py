import asyncio
import discord
from discord.ext import commands
from discord.ui import Select, View, Item, Button
from dotenv import load_dotenv
import names
import asyncpg
from random import randint, random, sample, choice
import requests
import json
import matchengine
import nfts
import players
import teams

async def get(i):
    f_goals = "goals.csv"

    if "event_" in i:
        f_goals = "goals_"+i+".csv"
        print(f_goals)

    with open(f_goals, "r") as tgoals:
        goalfile = tgoals.readlines()
        goalfile.sort(reverse=True, key=lambda x: int(x.split(",")[0]))
        goallist = []
        embedname = ""
        embedteam = ""
        embedscore = ""
        indice = 1

        for goal in goalfile:
            if indice <= 10:
                name = goal.split(",")[1]
                team = goal.split(",")[2]
                number = goal.split(",")[0]
                goallist.append(goal)
                embedname = embedname + name + "\n"
                embedteam = embedteam + team + "\n"
                embedscore = embedscore + str(number) + "\n"
                indice += 1

        if embedname == "":
            embedname = "\u200b"
        if embedscore == "":
            embedscore = "\u200b"
        if embedteam == "":
            embedteam = "\u200b"

        default_color = 0x00ff00

        if "event_" in i:
            name = i.split("_")[1].upper()
            embedlead = discord.Embed(
                title="Leaderboards", description="Best players for the **"+name+"** event", color=default_color)
        else:
            embedlead = discord.Embed(
                title="Leaderboards", description="Best players", color=default_color)
        embedlead.add_field(name="Player", value=embedname)
        embedlead.add_field(name="Team", value=embedteam)
        embedlead.add_field(name="Goals", value=embedscore)

        return embedlead