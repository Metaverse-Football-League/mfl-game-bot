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
import players

## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = "teams.csv"

async def get(id):
    print("called")
    # Find team which owned by called player
    with open(f_teams, "r") as tfile:
        teamfile = tfile.readlines()

        for line in teamfile:
            try:
                if id == str(line.split(",")[1]):
                    return line
            except:
                continue

async def get_All(id):
    user_id = str(id)
    t_info = await get(user_id)

    if t_info is None or t_info == "Error":
        return "You have no team !"
    else:
        p_info = await players.get(user_id)
        team_name = t_info.split(",")[0]

        i = 0
        default_color = 0x00ff00

        embedteam = discord.Embed(
            title=team_name, description="Below your squad", color=default_color)

        embeddescription = ""

        while i <= 11:
            if i == 0:
                i += 1

            name = p_info[i].split(",")[0]
            ovr = p_info[i].split(",")[1]
            pos = p_info[i].split(",")[2].upper()
            nat = p_info[i].split(",")[4]
            nft = p_info[i].split(",")[5]
            rarity = p_info[i].split(",")[6]
            rarity_flag = "⚫"
            if nft == "1":
                if rarity == "common":
                    rarity_flag = "⚪"
                elif rarity == "uncommon":
                    rarity_flag = "🟢"
                elif rarity == "rare":
                    rarity_flag = "🔵"
                elif rarity == "legend":
                    rarity_flag = "🟣"

            if len(pos) == 3:
                embeddescription = embeddescription + ":flag_" + nat + ":`" + pos + " " + ovr + "`" + rarity_flag + " *" + name + "*\n"
            else:
                embeddescription = embeddescription + ":flag_" + nat + ":`" + pos + "  " + ovr + "`" + rarity_flag + " *" + name + "*\n"
            i += 1

        man_name = p_info[0].split(",")[0]
        embedmanager = "*" + man_name + "*"
        embedteam.add_field(name="Players", value=embeddescription)
        embedteam.add_field(name="Coach", value=embedmanager, inline=False)

        return embedteam

