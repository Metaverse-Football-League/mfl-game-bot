import asyncio
import os
from typing import Any

import discord
from discord.ext import commands
from discord.interactions import Interaction
from discord.ui import Select, View, Item, Button
from dotenv import load_dotenv
import names
import asyncpg
from random import randint
from discord.utils import get
import requests
import json
import time

load_dotenv(dotenv_path="config")

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=intents)

#### Files
## Players
# DisplayName, OVR, Position, Owner
f_players = "players.csv"
## Teams
# Name, user_id, deleted
f_teams = "teams.csv"


########################################################################################################
## START OF PROCESS ##
########################################################################################################

async def create_player(id):
    with open(f_players, "a") as pfile:
        i = 1
        while i < 5:
            displayName = names.get_full_name(gender='male')
            ovr = randint(55, 65)
            if i == 1:
                position = "gk"
            elif i == 2:
                position = "def"
            elif i == 3:
                position = "mid"
            elif i == 4:
                position = "for"
            owner = id
            pfile.write(displayName + "," + str(ovr) + "," + position + "," + str(owner) + ",\n")
            i += 1


async def generate_player(i):
    displayName = names.get_full_name(gender='male')
    ovr = randint(60, 70)
    if i == 1:
        position = "gk"
    elif i == 2:
        position = "def"
    elif i == 3:
        position = "mid"
    elif i == 4:
        position = "for"
    owner = id
    new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + ",\n"
    return (new_line)


async def replace_player(id, num):
    pfile = open(f_players, "r+")
    i = num
    c = 0
    playerfile = pfile.readlines()
    playerlist = []
    for line in playerfile:
        if id in line:
            c += 1
            if c == i:
                displayName = names.get_full_name(gender='male')
                ovr = randint(55, 65)
                if i == 1:
                    position = "gk"
                elif i == 2:
                    position = "def"
                elif i == 3:
                    position = "mid"
                elif i == 4:
                    position = "for"
                owner = id
                new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + ",\n"
                replace = line.replace(line, new_line)
                line = replace
                if "," not in line:
                    line = ",,,,\n"
        playerlist.append(line)
    pfile.truncate(0)
    pfile.writelines(playerlist)
    pfile.close()


async def scout_player(id, num, name, ovr, pos):
    pfile = open(f_players, "r+")
    c = 0
    playerfile = pfile.readlines()
    playerlist = []
    i = int(num)
    print(i)
    for line in playerfile:
        print(line)
        try:
            if str(id) == str(line.split(",")[3]):
                c += 1
                if c == i:
                    displayName = name
                    ovr = ovr
                    position = pos
                    owner = id
                    new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + ",\n"
                    replace = line.replace(line, new_line)
                    line = replace
                    if "," not in line:
                        line = ",,,,\n"

        except:
            continue
        playerlist.append(line)
    pfile.truncate(0)
    pfile.writelines(playerlist)
    pfile.close()


async def view_team(id):
    with open(f_teams, "r") as tfile:
        teamfile = tfile.readlines()

        for line in teamfile:
            try:
                if id == str(line.split(",")[1]):
                    return line
            except:
                continue


async def view_players(id):
    with open(f_players, "r+") as pfile:
        playerfile = pfile.readlines()
        playerlist = []
        for line in playerfile:
            if id in line:
                playerlist.append(line)
        return playerlist


async def simulate(id):
    t_info = await view_team(id)
    p_info = await view_players(id)
    home_info = []
    away_info = []
    team_name_home = t_info.split(",")[0]
    team_name_away = "MFL Team"
    home_p1 = p_info[0]
    home_p2 = p_info[1]
    home_p3 = p_info[2]
    home_p4 = p_info[3]
    home_ovr = (int(home_p1.split(',')[1]) + int(home_p2.split(',')[1]) + int(home_p3.split(',')[1]) + int(
        home_p4.split(',')[1])) / 4
    away_ovr = 70
    score_home = 0
    score_away = 0

    i = 0
    print(round(home_ovr))
    defchance = 1000
    homechance = 995
    awaychance = 995
    if home_ovr - away_ovr > 0:
        homebonus = home_ovr - away_ovr
        awaybonus = 0
    else:
        awaybonus = away_ovr - home_ovr
        homebonus = 0

    while i < 95:
        i += 1
        x = randint(1, 1000)
        if x > homechance:
            score_home += 1
            homechance = defchance
        elif x < 1000 - awaychance:
            print(x)
            score_away += 1
            awaychance = defchance

        homechance = homechance - homebonus
        awaychance = awaychance - awaybonus

    home_info.append(team_name_home)
    away_info.append(team_name_away)
    home_info.append(score_home)
    away_info.append(score_away)

    matchinfo = []
    matchinfo.append(home_info)
    matchinfo.append(away_info)

    return matchinfo


#### BOT IS READY ####
@bot.event
async def on_ready():
    print("Bot Ready")


#### CREATE TEAM ####
@bot.command(name='create')
async def create(ctx, name):
    if ctx.channel.id == 983723647002882058:
        teamname = name
        with open(f_teams, "r+") as tfile:
            user_id = str(ctx.message.author.id)
            print(tfile.read)
            if user_id in tfile.read():
                await ctx.send("Sorry, you already have a team !")
            else:
                tfile.write(teamname + "," + user_id + ",no,\n")
                await create_player(ctx.message.author.id)
                await ctx.send("Team " + teamname + " created !")


@bot.command(name='viewteam')
async def viewteam(ctx):
    if ctx.channel.id == 983723647002882058:
        user_id = str(ctx.message.author.id)
        t_info = await view_team(user_id)
        print(t_info)

        if t_info is None or t_info == "Error":
            await ctx.send("You have no team !")
        else:
            p_info = await view_players(user_id)
            team_name = t_info.split(",")[0]
            p1name = p_info[0].split(",")[0]
            p1ovr = p_info[0].split(",")[1]
            p1pos = p_info[0].split(",")[2]
            p2name = p_info[1].split(",")[0]
            p2ovr = p_info[1].split(",")[1]
            p2pos = p_info[1].split(",")[2]
            p3name = p_info[2].split(",")[0]
            p3ovr = p_info[2].split(",")[1]
            p3pos = p_info[2].split(",")[2]
            p4name = p_info[3].split(",")[0]
            p4ovr = p_info[3].split(",")[1]
            p4pos = p_info[3].split(",")[2]

            # embedbattle.set_thumbnail(url="https://i.ibb.co/Wk063wT/fight.png")

            i = 0
            while i < 4:
                default_color = 0x00ff00
                embedteam = discord.Embed(
                    title=p_info[i].split(",")[0], color=default_color)
                embedteam.add_field(name="NUM", value=i + 1, inline=True)
                embedteam.add_field(name="GEN", value=p_info[i].split(",")[1], inline=True)
                embedteam.add_field(name="POS", value=p_info[i].split(",")[2].upper(), inline=True)
                await ctx.send(embed=embedteam)
                i += 1


async def viewteam2(id):
    user_id = str(id)
    t_info = await view_team(user_id)
    print(t_info)

    if t_info is None or t_info == "Error":
        return "You have no team !"
    else:
        p_info = await view_players(user_id)
        team_name = t_info.split(",")[0]

        # embedbattle.set_thumbnail(url="https://i.ibb.co/Wk063wT/fight.png")

        i = 0
        default_color = 0x00ff00

        embedteam = discord.Embed(
            title=t_info.split(",")[0], description="Below your players list", color=default_color)

        embeddescription = ""

        while i < 4:
            num = i + 1
            name = p_info[i].split(",")[0]
            ovr = p_info[i].split(",")[1]
            pos = p_info[i].split(",")[2].upper()

            if pos == "GK":
                embeddescription = embeddescription + "`" +str(num) + " - " + pos + "  " + ovr + "` *" + name+"*\n"
            else:
                embeddescription = embeddescription + "`" + str(num) + " - " + pos + " " + ovr + "` *" + name+"*\n"

            i += 1
        embedteam.add_field(name="Players", value=embeddescription)

        return embedteam


@bot.command(name='change')
async def change(ctx, number):
    if ctx.channel.id == 983723647002882058:
        user_id = str(ctx.message.author.id)
        await replace_player(user_id, int(number))

        p_info = await view_players(user_id)

        i = int(number) - 1
        default_color = 0xffff00
        embedteam = discord.Embed(
            title=p_info[i].split(",")[0], color=default_color)
        embedteam.add_field(name="NUM", value=i + 1, inline=True)
        embedteam.add_field(name="GEN", value=p_info[i].split(",")[1], inline=True)
        embedteam.add_field(name="POS", value=p_info[i].split(",")[2].upper(), inline=True)
        await ctx.send(embed=embedteam)


@bot.command(name='scout')
async def scout(ctx):
    if ctx.channel.id == 983723647002882058:

        user_id = str(ctx.message.author.id)
        number = randint(1, 4)
        p_info = await generate_player(number)
        name = p_info.split(",")[0]
        ovr = p_info.split(",")[1]
        pos = p_info.split(",")[2].upper()

        i = int(number)
        default_color = 0xffff00
        embedteam = discord.Embed(
            title=name, color=default_color)
        embedteam.add_field(name="NUM", value=i + 1, inline=True)
        embedteam.add_field(name="GEN", value=ovr, inline=True)
        embedteam.add_field(name="POS", value=pos, inline=True)

        embedteam2 = discord.Embed(
            title=name, description="You find a new player !", color=default_color)
        if pos == "GK":
            embeddescription = "`" + str(i) + " - " + pos + "  " + ovr + "` *" + name + "*\n"
        else:
            embeddescription = "`" + str(i) + " - " + pos + " " + ovr + "` *" + name + "*\n"

        embedteam2.add_field(name="Players", value=embeddescription)

        wantplayer = await ctx.send(embed=embedteam2)

        await wantplayer.add_reaction("✅")
        await wantplayer.add_reaction("❌")

        def check(reaction, user):
            return str(reaction.emoji) == "✅" and user == ctx.message.author

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            await scout_player(user_id, int(i) + 1, name, ovr, pos)
            await ctx.send(f"Congratulations {user.name}, {name} joined your team!")
        except asyncio.TimeoutError:
            await wantplayer.delete()


@bot.command(name='scout2')
async def scout2(id):
    user_id = str(id)
    number = randint(1, 4)
    p_info = await generate_player(number)
    name = p_info.split(",")[0]
    ovr = p_info.split(",")[1]
    pos = p_info.split(",")[2].upper()

    playerinfo = []
    playerinfo.append(number)
    playerinfo.append(name)
    playerinfo.append(ovr)
    playerinfo.append(pos)

    i = int(number)
    default_color = 0xffff00
    embedplayer = discord.Embed(
        title=name, color=default_color)
    embedplayer.add_field(name="NUM", value=i + 1, inline=True)
    embedplayer.add_field(name="GEN", value=ovr, inline=True)
    embedplayer.add_field(name="POS", value=pos, inline=True)

    embedplayer2 = discord.Embed(
        title=name, description="You find a new player !", color=default_color)
    if pos == "GK":
        embeddescription = "` " + str(i) + " - " + pos + "  " + ovr + " ` *" + name + "*\n"
    else:
        embeddescription = "` " + str(i) + " - " + pos + " " + ovr + " ` *" + name + "*\n"

    embedplayer2.add_field(name="Players", value=embeddescription)

    return embedplayer2

    # wantplayer = await ctx.send(embed=embedteam)
    # await wantplayer.add_reaction("✅")
    # await wantplayer.add_reaction("❌")

    # def check(reaction, user):
    #    return str(reaction.emoji) == "✅" and user == ctx.message.author
    # try:
    #    reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
    #    await scout_player(user_id, int(i)+1, name, ovr, pos)
    #    await ctx.send(f"Congratulations {user.name}, {name} joined your team!")
    # except asyncio.TimeoutError:
    #    await wantplayer.delete()


#### SIMULATE MATCHES ####

@bot.command(name='play')
async def play(ctx):
    if ctx.channel.id == 983723647002882058:
        user_id = str(ctx.message.author.id)
        matchinfos = await simulate(user_id)
        home_info = matchinfos[0]
        away_info = matchinfos[1]

        default_color = 0xffff00
        embedscore = discord.Embed(
            title='Match Day', color=default_color)
        # embedbattle.set_thumbnail(url="https://i.ibb.co/Wk063wT/fight.png")
        embedscore.add_field(name=home_info[0], value=home_info[1], inline=True)
        embedscore.add_field(name=away_info[0], value=away_info[1], inline=True)
        await ctx.send(embed=embedscore)


async def play2(id):
    user_id = str(id)
    matchinfos = await simulate(user_id)
    home_info = matchinfos[0]
    away_info = matchinfos[1]

    default_color = 0xffff00
    embedscore = discord.Embed(
        title='Match Day', color=default_color)
    # embedbattle.set_thumbnail(url="https://i.ibb.co/Wk063wT/fight.png")
    embedscore.add_field(name=home_info[0], value=home_info[1], inline=True)
    embedscore.add_field(name=away_info[0], value=away_info[1], inline=True)
    return embedscore


#### Menu display
class MenuSelect(Select):
    async def callback(self, interaction: Interaction) -> Any:
        defselect = MenuSelect(placeholder="Make a choice !",
                               custom_id=str(self.custom_id),
                               options=[
                                   discord.SelectOption(
                                       label="View",
                                       value="view",
                                       emoji="❌",
                                       description="Show your players"),
                                   discord.SelectOption(
                                       label="Scout",
                                       value="scout",
                                       emoji="❌",
                                       description="Scouting"),
                                   discord.SelectOption(
                                       label="Play",
                                       value="play",
                                       emoji="❌",
                                       description="Play a match")
                               ])
        defview = View()
        defview.add_item(defselect)
        if self.values[0] == "view":
            embedteam = await viewteam2(self.custom_id)
            await interaction.response.send_message(f"You chose: {self.values} {self.custom_id}")
            select = MenuSelect(placeholder="Make a choice !",
                                custom_id=str(self.custom_id),
                                options=[
                                    discord.SelectOption(
                                        label="View",
                                        value="view",
                                        emoji="❌",
                                        description="Show your players"),
                                    discord.SelectOption(
                                        label="Return",
                                        value="return",
                                        emoji="❌",
                                        description="return")
                                ])
            view = View()
            view.add_item(select)
            await interaction.followup.send(embed=embedteam, view=view)

        elif self.values[0] == "play":
            embedscore = await play2(self.custom_id)
            # await interaction.response.send_message(f"You chose: {self.values} {self.custom_id}")

            # await interaction.followup.send(embed=embedscore, view=defview)
            await interaction.edit_original_message(embed=embedscore, view=defview)


@bot.command(name='game2')
async def game(ctx):
    if ctx.channel.id == 983723647002882058:
        user_id = str(ctx.message.author.id)
        select = Select(placeholder="Make a choice !",
                        custom_id=str(user_id),
                        options=[
                            discord.SelectOption(
                                label="View",
                                value="view",
                                emoji="❌",
                                description="Show your players"),
                            discord.SelectOption(
                                label="Scout",
                                value="scout",
                                emoji="❌",
                                description="Scouting"),
                            discord.SelectOption(
                                label="Play",
                                value="play",
                                emoji="❌",
                                description="Play a match")
                        ])
        view = View()
        view.add_item(select)

        default_color = 0xffff00
        embeddef = discord.Embed(
            title='Match Day', color=default_color)
        embeddef.add_field(name="Team", value="Infos Team", inline=True)

        showmenu = await ctx.send("Lets play !", view=view, embed=embeddef)

        ########### CALL BACK
        async def my_callback(interaction):

            if select.values[0] == "play":
                print("choice play")
                embedscore = await play2(select.custom_id)
                # await showmenu.edit(embed=embedscore, view=view)
                await interaction.edit_original_message(view=view, embed=embedscore)

        select.callback = my_callback


@bot.command(name='game')
async def game(ctx):
    if ctx.channel.id == 983723647002882058:
        user_id = str(ctx.message.author.id)
        user_name = str(ctx.message.author)
        default_color = 0x00ff00
        embedmenu = discord.Embed(
            title='Discord Football Game', color=default_color)
        embedmenu.add_field(name="Hello", value="Want play ?", inline=True)

        button_play = Button(label="Play", style=discord.ButtonStyle.green, custom_id="play", emoji="⚽")
        button_scout = Button(label="Scout", style=discord.ButtonStyle.green, custom_id="scout", emoji="👨")
        button_team = Button(label="Team", style=discord.ButtonStyle.green, custom_id="team", emoji="👥")

        button_recruit = Button(label="Recruit", style=discord.ButtonStyle.green, custom_id="recruit", emoji="✅")
        button_letleave = Button(label="Quit", style=discord.ButtonStyle.grey, custom_id="letleave", emoji="❌")

        view = View()
        view.add_item(button_team)
        view.add_item(button_scout)
        view.add_item(button_play)

        viewscout = View()
        viewscout.add_item(button_team)
        viewscout.add_item(button_recruit)
        viewscout.add_item(button_letleave)

        async def button_play_callback(interaction):
            print(user_name)
            if str(interaction.user) == user_name:
                embedscore = await play2(user_id)
                await showmenu.edit(content="PLAY !", view=view, embed=embedscore)
                await interaction.response.defer(ephemeral=True)

        async def button_team_callback(interaction):
            embedteam = await viewteam2(user_id)
            await showmenu.edit(content="TEAM !", view=view, embed=embedteam)
            await interaction.response.defer(ephemeral=True)

        async def button_scout_callback(interaction):
            embedplayer = await scout2(user_id)
            await showmenu.edit(content="SCOUT !", view=viewscout, embed=embedplayer)
            await interaction.response.defer(ephemeral=True)

        async def button_recruit_callback(interaction):
            playerscheck = interaction.message.embeds[0].fields
            playersinfos = playerscheck[0].value.split(" ")
            num = playersinfos[1]
            if num == "1":
                pos = playersinfos[3]
                ovr = playersinfos[5]
                name = playersinfos[7]+" "+playersinfos[8]
            else:
                pos = playersinfos[3]
                ovr = playersinfos[4]
                name = playersinfos[6]+" "+playersinfos[7]

            name = name.replace("*","")
            print(name)
            await scout_player(user_id, num, name, ovr, pos)
            embedteam = await viewteam2(user_id)

            await showmenu.edit(content="A new player joined you team", view=view, embed=embedteam)
            await interaction.response.defer(ephemeral=True)

        async def button_letleave_callback(interaction):
            await showmenu.edit(content="PLAY !", view=view, embed=embedmenu)
            await interaction.response.defer(ephemeral=True)

        button_play.callback = button_play_callback
        button_team.callback = button_team_callback
        button_scout.callback = button_scout_callback
        button_recruit.callback = button_recruit_callback
        button_letleave.callback = button_letleave_callback

        showmenu = await ctx.send("Welcome !", view=view, embed=embedmenu)
        await showmenu.delete(delay=3600.0)


#### BOT TOKEN ########################
bot.run("OTgxNTI0NDI1NjIxMDA4NDE1.GCnt7d.0fY5touBIf9HOqtMJlHprQOZXIRYudbLFaubIY")
