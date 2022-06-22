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
f_goals = "goals.csv"

########################################################################################################
## START OF PROCESS ##
########################################################################################################

async def create_player(id, manager):
    with open(f_players, "a") as pfile:
        i = 1
        if int(id) > 1000000:
            manager = manager
            m_ovr = 50
        else:
            manager = "BOT"
            m_ovr = randint(70, 90)

        m_pos = "COACH"
        m_owner = id
        pfile.write(manager + "," + str(m_ovr) + "," + m_pos + "," + str(m_owner) + ",\n")
        while i <= 11:
            if int(id) < 1000000:
                ovr = randint(65, 82)
            else:
                ovr = randint(55, 65)
            displayName = names.get_full_name(gender='male')
            if i == 1:
                position = "gk"
            elif i == 2:
                position = "lb"
            elif i == 3:
                position = "cb"
            elif i == 4:
                position = "cb"
            elif i == 5:
                position = "rb"
            elif i == 6:
                position = "cm"
            elif i == 7:
                position = "cm"
            elif i == 8:
                position = "am"
            elif i == 9:
                position = "lw"
            elif i == 10:
                position = "rw"
            elif i == 11:
                position = "st"
            owner = id
            pfile.write(displayName + "," + str(ovr) + "," + position + "," + str(owner) + ",\n")
            i += 1


async def generate_player(i):
    displayName = names.get_full_name(gender='male')
    rare = randint(0, 100)
    nationalities = ["gb", "us", "au", "fr", "ca", "es", "cu", "mx"]
    nat = choice(nationalities)

    if rare <= 70:
        ovr = randint(60, 70)
    elif 89 >= rare > 69:
        ovr = randint(70, 80)
    elif 97 >= rare > 89:
        ovr = randint(80, 90)
    elif rare > 97:
        ovr = randint(90, 99)

    if i == 1:
        position = "gk"
    elif i == 2:
        position = "lb"
    elif i == 3:
        position = "cb"
    elif i == 4:
        position = "cb"
    elif i == 5:
        position = "rb"
    elif i == 6:
        position = "cm"
    elif i == 7:
        position = "cm"
    elif i == 8:
        position = "am"
    elif i == 9:
        position = "lw"
    elif i == 10:
        position = "rw"
    elif i == 11:
        position = "st"

    owner = id
    new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + ","+nat+",\n"
    return new_line


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
                    position = "lb"
                elif i == 3:
                    position = "cb"
                elif i == 4:
                    position = "cb"
                elif i == 5:
                    position = "rb"
                elif i == 6:
                    position = "cm"
                elif i == 7:
                    position = "cm"
                elif i == 8:
                    position = "am"
                elif i == 9:
                    position = "lw"
                elif i == 10:
                    position = "rw"
                elif i == 11:
                    position = "st"
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


async def scout_player(id, num, name, ovr, pos, nat):
    #nationalities = ["gb", "us", "au", "fr", "ca", "es", "cu", "mx"]
    nat = nat
    pfile = open(f_players, "r+")
    c = 0
    playerfile = pfile.readlines()
    playerlist = []
    i = int(num) + 1
    for line in playerfile:
        try:
            if str(id) == str(line.split(",")[3]):
                c += 1
                if c == i:
                    displayName = name
                    ovr = ovr
                    position = pos
                    owner = id
                    new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + ","+nat+",\n"
                    replace = line.replace(line, new_line)
                    line = replace
                    if "," not in line:
                        line = ",,,,\n"

        except:
            continue
        playerlist.append(line)
    pfile.seek(0)
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

async def simulate2(id, vs):
    t_info = await view_team(id)
    p_info = await view_players(id)

    ### Away team stats
    try:
        t_vs_info = await view_team(vs)
        p_vs_info = await view_players(vs)
        team_name_away = t_vs_info.split(",")[0]
        away_man = p_vs_info[0]
        away_p1 = p_vs_info[1]
        away_p2 = p_vs_info[2]
        away_p3 = p_vs_info[3]
        away_p4 = p_vs_info[4]
        away_p5 = p_vs_info[5]
        away_p6 = p_vs_info[6]
        away_p7 = p_vs_info[7]
        away_p8 = p_vs_info[8]
        away_p9 = p_vs_info[9]
        away_p10 = p_vs_info[10]
        away_p11 = p_vs_info[11]
        away_ovr = (int(away_p1.split(',')[1]) + int(away_p2.split(',')[1]) + int(away_p3.split(',')[1]) + int(
            away_p4.split(',')[1]) + int(away_p5.split(',')[1]) + int(away_p6.split(',')[1]) + int(
            away_p7.split(',')[1]) + int(away_p8.split(',')[1]) + int(away_p9.split(',')[1]) + int(
            away_p10.split(',')[1]) + int(away_p11.split(',')[1])) / 11

    except:
        team_name_away = "MFL Team"
        away_ovr = randint(65, 72)

    ### Home team stats
    team_name_home = t_info.split(",")[0]
    home_man = p_info[0]
    home_p1 = p_info[1]
    home_p2 = p_info[2]
    home_p3 = p_info[3]
    home_p4 = p_info[4]
    home_p5 = p_info[5]
    home_p6 = p_info[6]
    home_p7 = p_info[7]
    home_p8 = p_info[8]
    home_p9 = p_info[9]
    home_p10 = p_info[10]
    home_p11 = p_info[11]
    home_ovr = (int(home_p1.split(',')[1]) + int(home_p2.split(',')[1]) + int(home_p3.split(',')[1]) + int(
        home_p4.split(',')[1]) + int(home_p5.split(',')[1]) + int(home_p6.split(',')[1]) + int(
        home_p7.split(',')[1]) + int(home_p8.split(',')[1]) + int(home_p9.split(',')[1]) + int(
        home_p10.split(',')[1]) + int(home_p11.split(',')[1])) / 11

    ### Matchs initialisation
    home_info = []
    away_info = []
    commentary = []

    home_bonus = round(home_ovr - away_ovr)
    away_bonus = round(away_ovr - home_ovr)
    bonus = abs(home_bonus)

    note = randint(1, 100)
    if note <= 10:
        note = 1
    elif 10 < note <= 30:
        note = 2
    elif 30 < note <= 70:
        note = 3
    elif 70 < note <= 90:
        note = 4
    elif 90 < note:
        note = 5

    if bonus == 0:
        bonus = 1
    ratio = round(50 + 2*home_bonus)

    nb_actions = 4 * note + randint(1, bonus)

    score_home = 0
    score_away = 0
    minutes = randint(92, 96)

    i = 0

    ### Lists of events (minutes, score_home, score_away)
    matchevents = []
    home_scorers = []
    away_scorers = []
    home_scorers.append("\u200b")
    away_scorers.append("\u200b")
    commentary.append("The match begins !")

    while i < minutes:
        i += 1
        x = randint(1, minutes)
        hvalue = home_scorers[i - 1]
        avalue = away_scorers[i - 1]

        def whoscore(team):
            what = randint(1,20)
            if what > 17:
                what = "Goal"
            else:
                what = "No Goal"

            whonumber = randint(1, 100)
            if team == "home":
                if whonumber < 1:
                    who = home_p1
                elif 1 < whonumber < 7:
                    who = home_p2
                elif 7 < whonumber < 15:
                    who = home_p3
                elif 15 < whonumber < 23:
                    who = home_p4
                elif 23 < whonumber < 29:
                    who = home_p5
                elif 29 < whonumber < 36:
                    who = home_p6
                elif 36 < whonumber < 43:
                    who = home_p7
                elif 43 < whonumber < 55:
                    who = home_p8
                elif 55 < whonumber < 68:
                    who = home_p9
                elif 68 < whonumber < 81:
                    who = home_p10
                else:
                    who = home_p11
            if team == "away":
                if whonumber < 1:
                    who = away_p1
                elif 1 < whonumber < 7:
                    who = away_p2
                elif 7 < whonumber < 15:
                    who = away_p3
                elif 15 < whonumber < 23:
                    who = away_p4
                elif 23 < whonumber < 29:
                    who = away_p5
                elif 29 < whonumber < 36:
                    who = away_p6
                elif 36 < whonumber < 43:
                    who = away_p7
                elif 43 < whonumber < 55:
                    who = away_p8
                elif 55 < whonumber < 68:
                    who = away_p9
                elif 68 < whonumber < 81:
                    who = away_p10
                else:
                    who = away_p11

            return who.split(",")[0], what, team

        def register_goals(player, team):
            pfile = open("goals.csv", "r+")
            playerfile = pfile.readlines()
            playerlist = []
            status = 0

            for line in playerfile:

                fplayer = line.split(",")[1]
                fteam = line.split(",")[2]

                if (fplayer == player) and (fteam == team):
                    print(fplayer + " : " + player)
                    fgoals = int(line.split(",")[0])
                    newgoals = fgoals + 1
                    print(newgoals)
                    new_line = str(newgoals)+","+player + "," + team + ",\n"
                    replace = line.replace(line, new_line)
                    line = replace
                    if "," not in line:
                        line = ",,,,\n"
                    status = 1

                playerlist.append(line)

            if status == 0:
                newgoals = 1
                pfile.write(str(newgoals) + "," + player + "," + team + ",\n")
            else:
                pfile.seek(0)
                pfile.truncate(0)
                pfile.writelines(playerlist)
            pfile.close()

        ### Déclenchement actions
        if x < nb_actions:
            who_attack = randint(1,100)
            if who_attack > ratio:
                who, what, team = whoscore("away")
            else:
                who, what, team = whoscore("home")

            if what == "Goal":

                if team == "home":
                    score_home += 1
                    hvalue = hvalue + "," + who
                    commentary.append("What a goal for " +team_name_home+" by "+who)
                    register_goals(who, team_name_home)
                else:
                    score_away += 1
                    avalue = avalue + "," + who
                    commentary.append("What a goal for " +team_name_away+" by "+who)
                    register_goals(who, team_name_away)

            else:
                if team == "home":
                    commentary.append("Beautiful action for " + team_name_home + " but " + who + " missed the shoot")
                else:
                    commentary.append("Beautiful action for " + team_name_away + " but " + who + " missed the shoot")

        else:
            commentary.append("---")

        home_scorers.append(hvalue)
        away_scorers.append(avalue)

        matchevents.append(str(i) + "," + str(score_home) + "," + str(score_away))

    home_info.append(team_name_home)
    away_info.append(team_name_away)
    home_info.append(score_home)
    away_info.append(score_away)

    matchinfo = []
    matchinfo.append(home_info)
    matchinfo.append(away_info)
    matchinfo.append(minutes)

    ### Note review
    if (int(score_away + score_home) <= 1) and (note > 1):
        note = note - 1
    elif int(score_away + score_home) > 3 and (note < 3):
        note = note + 1
    elif (int(score_away + score_home) <= 2) and (note > 3):
        note = note - 1
    matchinfo.append(note)
    ### Commentary review
    if commentary[minutes] == "---":
        if score_home > score_away:
            commentary[minutes] = "At home, **"+team_name_home+"** wins the game against "+team_name_away+"."
        elif score_home < score_away:
            commentary[minutes] = "**"+team_name_away+"** makes a great match and overcomes "+team_name_home+"."
        else:
            commentary[minutes] = "What a game !\n But "+team_name_home+" and "+team_name_away+" "+"could not tell the difference"
    matchinfo.append(commentary)

    return matchinfo, matchevents, home_scorers, away_scorers


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
            if int(user_id) > 1000000:
                user = bot.get_user(int(user_id))
                username = user.name
            else:
                username = "BOT"
            team_id = user_id
            if user_id in tfile.read():
                if user_id == "593086239024873483":
                    team_id = str(randint(1, 999999))
                    tfile.write(teamname + "," + team_id + ",no,\n")
                    await create_player(team_id, username)
                    await ctx.send("Team " + teamname + " created !")
                else:
                    await ctx.send("Sorry, you already have a team !")
            else:
                tfile.write(teamname + "," + team_id + ",no,\n")
                await create_player(team_id, username)
                await ctx.send("Team " + teamname + " created !")


async def viewteam(id):
    user_id = str(id)
    t_info = await view_team(user_id)

    if t_info is None or t_info == "Error":
        return "You have no team !"
    else:
        p_info = await view_players(user_id)
        team_name = t_info.split(",")[0]

        # embedbattle.set_thumbnail(url="https://i.ibb.co/Wk063wT/fight.png")

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
            embeddescription = embeddescription + ":flag_"+nat+":`" + pos + "  " + ovr + "` *" + name + "*\n"
            i += 1

        man_name = p_info[0].split(",")[0]
        embedmanager = "*" + man_name + "*"
        embedteam.add_field(name="Players", value=embeddescription)
        embedteam.add_field(name="Coach", value=embedmanager, inline=False)

        return embedteam

async def viewleads(id):
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
                embedname = embedname + name+"\n"
                embedteam = embedteam + team+"\n"
                embedscore = embedscore + str(number)+"\n"
                indice += 1

        if embedname == "":
            embedname = "\u200b"
        if embedscore == "":
            embedscore = "\u200b"
        if embedteam == "":
            embedteam = "\u200b"
            
        default_color = 0x00ff00
        embedlead = discord.Embed(
            title="Leaderboards", description="Best players", color=default_color)
        embedlead.add_field(name="Player", value=embedname)
        embedlead.add_field(name="Team", value=embedteam)
        embedlead.add_field(name="Goals", value=embedscore)

        return embedlead

async def viewevents(id):
    with open("events.csv", "r") as tevents:
        eventfile = tevents.readlines()
        default_color = 0x00ff00
        embedevent = discord.Embed(
            title="Events", description="Below the list of current events", color=default_color)

        for event in eventfile:
            eventname = event.split(",")[0]
            eventdesc = event.split(",")[1]
            eventstatus = event.split(",")[2]

            if int(eventstatus) > 1:
                continue

            embedevent.add_field(name=eventname, value=eventdesc)

        return embedevent

async def findteam(id):
    with open(f_teams, "r") as tfile:
        teamfile = tfile.readlines()
        teamlist = []
        genopponent = sample(range(0, len(teamfile)), 5)
        selected = 0

        for x in genopponent:
            if selected < 3:
                try:
                    teamid = str(teamfile[x].split(",")[1])
                    if id == teamid:
                        continue
                    if int(teamid) > 1000000:
                        user = bot.get_user(int(teamid))
                        username = user.name
                    else:
                        username = "BOT"
                    name = str(teamfile[x].split(",")[0])
                    teamlist.append(name + "," + teamid + "," + username)
                    selected += 1
                except:
                    continue

        default_color = 0x00ff00

        embedteam = discord.Embed(
            title="Match Settings", description="Choose your opponent", color=default_color)

        embedopponents = "`" + teamlist[0].split(",")[0] + "` *" + teamlist[0].split(",")[2] + "*\n"
        embedopponents = embedopponents + "`" + teamlist[1].split(",")[0] + "` *" + teamlist[1].split(",")[2] + "*\n"
        embedteam.add_field(name="Opponents", value=embedopponents)

        return embedteam, teamlist


@bot.command(name='view')
async def change(ctx, user: discord.User):
    if ctx.channel.id == 983723647002882058:
        embedteam = await viewteam(str(user.id))
        await ctx.send(embed=embedteam)


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


async def scout(id):
    user_id = str(id)
    p_info = await view_players(user_id)

    number = randint(1, 11)
    newp_info = await generate_player(number)
    name = newp_info.split(",")[0]
    ovr = newp_info.split(",")[1]
    pos = newp_info.split(",")[2].upper()
    nat = newp_info.split(",")[4]

    ## Case of similar posts

    if number in (3, 4):
        ovr3 = p_info[3].split(",")[1]
        ovr4 = p_info[4].split(",")[1]
        if ovr3 < ovr4:
            old_name = p_info[3].split(",")[0]
            old_ovr = p_info[3].split(",")[1]
            old_pos = p_info[3].split(",")[2].upper()
            old_nat = p_info[3].split(",")[4]
            number = 3
        else:
            old_name = p_info[4].split(",")[0]
            old_ovr = p_info[4].split(",")[1]
            old_pos = p_info[4].split(",")[2].upper()
            old_nat = p_info[4].split(",")[4]
            number = 4
    elif number in (6, 7):
        ovr6 = p_info[6].split(",")[1]
        ovr7 = p_info[7].split(",")[1]
        if ovr6 < ovr7:
            old_name = p_info[6].split(",")[0]
            old_ovr = p_info[6].split(",")[1]
            old_pos = p_info[6].split(",")[2].upper()
            old_nat = p_info[6].split(",")[4]
            number = 6
        else:
            old_name = p_info[7].split(",")[0]
            old_ovr = p_info[7].split(",")[1]
            old_pos = p_info[7].split(",")[2].upper()
            old_nat = p_info[7].split(",")[4]
            number = 7
    else:
        old_name = p_info[number].split(",")[0]
        old_ovr = p_info[number].split(",")[1]
        old_pos = p_info[number].split(",")[2].upper()
        old_nat = p_info[number].split(",")[4]

    playerinfo = []
    playerinfo.append(number)
    playerinfo.append(name)
    playerinfo.append(ovr)
    playerinfo.append(pos)
    playerinfo.append(nat)

    i = int(number)
    default_color = 0xffff00

    embedplayer = discord.Embed(
        title=name, description="You find a new player !", color=default_color)
    embeddescription = ":flag_"+nat+":`" + str(i) + " - " + pos + " " + ovr + "` *" + name + "*\n"
    oldplayer = ":flag_"+old_nat+":`" + str(i) + " - " + old_pos + " " + old_ovr + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer


#### SIMULATE MATCHES ####
async def play(id, vs):
    user_id = str(id)
    matchinfos, matchsevents, home_scorers, away_scorers = await simulate2(user_id, vs)
    home_info = matchinfos[0]
    away_info = matchinfos[1]
    home_name = home_info[0]
    away_name = away_info[0]
    commentary = matchinfos[4]

    description_start = "Welcome to the match !\nToday, "+home_name+" will face "+away_name+".\n\nThe teams enter the " \
                                                                                      "field... let's go! "
    description_default = "Welcome to the match !\nToday, "+home_name+" will face "+away_name+".\n"

    note = matchinfos[3]
    if note == 1:
        note = "⭐"
    elif note == 2:
        note = "⭐⭐"
    elif note == 3:
        note = "⭐⭐⭐"
    elif note == 4:
        note = "⭐⭐⭐⭐"
    elif note == 5:
        note = "⭐⭐⭐⭐⭐"

    default_color = 0xffff00
    embedlist = []

    for x in matchsevents:

        minutes = x.split(",")[0]
        if int(minutes) == 1:
            description = description_start
        elif int(minutes) == len(matchsevents):
            description = "The referee whistles the end of the game !"
        else:
            description = description_default

        home_score = x.split(",")[1]
        away_score = x.split(",")[2]
        embedscore = discord.Embed(
            title='Match Day', color=default_color, description=description)
        embedscore.add_field(name="MIN", value=minutes + "'", inline=True)
        embedscore.add_field(name=home_name, value=home_score, inline=True)
        embedscore.add_field(name=away_name, value=away_score, inline=True)
        embedscore.add_field(name="\u200b", value="**Goals**", inline=True)

        hgoals = home_scorers[int(minutes)].split(',')
        agoals = away_scorers[int(minutes)].split(',')
        nogoal = "\u200b"
        hvalue = nogoal
        avalue = nogoal

        if len(hgoals) > 1:
            for x in hgoals:
                if x == nogoal:
                    continue
                hvalue += x + "\n"

        if len(agoals) > 1:
            for x in agoals:
                if x == nogoal:
                    continue
                avalue += x + "\n"

        embedscore.add_field(name="\u200b", value=hvalue, inline=True)
        embedscore.add_field(name="\u200b", value=avalue, inline=True)
        embedscore.add_field(name="Commentary", value=commentary[int(minutes)], inline=False)
        embedscore.add_field(name="Match Note", value=note, inline=False)

        embedlist.append(embedscore)
    return embedlist


#### Menu display
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
        button_letleave = Button(label="Return", style=discord.ButtonStyle.grey, custom_id="letleave", emoji="❌")
        button_finishmatch = Button(label="Skip", style=discord.ButtonStyle.blurple, custom_id="finishmatch")
        button_leaderboard = Button(label="Leaderboard", style=discord.ButtonStyle.grey, row=1, custom_id="leaderboard", emoji="🏆")
        button_events = Button(label="Events", style=discord.ButtonStyle.blurple, row=1, custom_id="events", emoji="⭐")

        view = View()
        view.add_item(button_team)
        view.add_item(button_scout)
        view.add_item(button_play)
        view.add_item(button_events)
        view.add_item(button_leaderboard)

        viewscout = View()
        viewscout.add_item(button_team)
        viewscout.add_item(button_recruit)
        viewscout.add_item(button_letleave)

        viewmatch = View()
        viewmatch.add_item(button_finishmatch)
        viewmatch.add_item(button_team)
        skip = 0

        async def button_play_callback(interaction):
            if str(interaction.user) == user_name:
                embedteam, teamlist = await findteam(user_id)

                viewopponents = View()

                id_random = str(teamlist[2].split(",")[1])
                button_random = Button(label="vs Random", style=discord.ButtonStyle.grey, custom_id=id_random,
                                       emoji="⚽")
                viewopponents.add_item(button_random)

                i = 1
                for x in teamlist:
                    name = x.split(",")[0]
                    vs_id = x.split(",")[1]
                    if i == 1:
                        button_vs1 = Button(label=name, style=discord.ButtonStyle.green, custom_id=str(vs_id))
                        viewopponents.add_item(button_vs1)
                    elif i == 2:
                        button_vs2 = Button(label=name, style=discord.ButtonStyle.green, custom_id=str(vs_id))
                        viewopponents.add_item(button_vs2)
                    i += 1

                viewopponents.add_item(button_team)

                await showmenu.edit(view=viewopponents, embed=embedteam)
                await interaction.response.defer(ephemeral=True)

                async def button_vs_callback(interaction):
                    if str(interaction.user) == user_name:
                        global skip
                        skip = 0

                        vs = interaction.data['custom_id']
                        embedlist = await play(user_id, vs)

                        async def button_finishmatch_callback(interaction):
                            global skip

                            if str(interaction.user) == user_name:
                                skip = 1
                                await showmenu.edit(view=viewmatch, embed=embedlist[-1])
                                await interaction.response.defer(ephemeral=False)

                        for x in embedlist:

                            button_finishmatch.callback = button_finishmatch_callback
                            if skip == 1:
                                break

                            await showmenu.edit(view=viewmatch, embed=x)
                            await asyncio.sleep(1)

                            try:
                                await interaction.response.defer(ephemeral=False)
                            except discord.InteractionResponded:
                                continue

                button_random.callback = button_vs_callback
                button_vs1.callback = button_vs_callback
                button_vs2.callback = button_vs_callback

        async def button_team_callback(interaction):
            if str(interaction.user) == user_name:
                embedteam = await viewteam(user_id)
                await showmenu.edit(view=view, embed=embedteam)
                await interaction.response.defer(ephemeral=True)

        async def button_scout_callback(interaction):
            if str(interaction.user) == user_name:
                embedplayer = await scout(user_id)
                await showmenu.edit(view=viewscout, embed=embedplayer)
                await interaction.response.defer(ephemeral=True)

        async def button_leaderboard_callback(interaction):
            if str(interaction.user) == user_name:
                embedlead = await viewleads(user_id)
                await showmenu.edit(view=view, embed=embedlead)
                await interaction.response.defer(ephemeral=True)

        async def button_events_callback(interaction):
            if str(interaction.user) == user_name:
                embedevents = await viewevents(user_id)
                await showmenu.edit(view=view, embed=embedevents)
                await interaction.response.defer(ephemeral=True)

        async def button_recruit_callback(interaction):
            if str(interaction.user) == user_name:
                playerscheck = interaction.message.embeds[0].fields
                playersinfos = playerscheck[0].value.split(" ")
                nat = playersinfos[0].split("`")[0].split("_")[1].replace(":","")
                num = playersinfos[0].split("`")[1]

                pos = playersinfos[2]
                ovr = playersinfos[3].replace("`", "")
                name = playersinfos[4] + " " + playersinfos[5]

                name = name.replace("*", "")
                await scout_player(user_id, num, name, ovr, pos, nat)
                embedteam = await viewteam(user_id)

                await showmenu.edit(view=view, embed=embedteam)
                await interaction.response.defer(ephemeral=True)

        async def button_letleave_callback(interaction):
            if str(interaction.user) == user_name:
                await showmenu.edit(view=view, embed=embedmenu)
                await interaction.response.defer(ephemeral=True)

        button_play.callback = button_play_callback
        button_events.callback = button_events_callback
        button_leaderboard.callback = button_leaderboard_callback
        button_team.callback = button_team_callback
        button_scout.callback = button_scout_callback
        button_recruit.callback = button_recruit_callback
        button_letleave.callback = button_letleave_callback

        showmenu = await ctx.send("\u200b", view=view, embed=embedmenu)
        await showmenu.delete(delay=3600.0)


#### BOT TOKEN ########################
bot.run("OTgxNTI0NDI1NjIxMDA4NDE1.GCnt7d.0fY5touBIf9HOqtMJlHprQOZXIRYudbLFaubIY")
