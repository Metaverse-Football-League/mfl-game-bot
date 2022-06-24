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

### Prerequisites
# Discord2 Python library (py-cord)
# asyncio library
# names library to generate random names

### Files
## Players (DisplayName, OVR, Position, Owner, nationality, nft, rarity)
f_players = "players.csv"
## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = "teams.csv"
## Goal scorers (number, name, team)
f_goals = "goals.csv"
## Event (name, desc, status)
f_events = "events.csv"

load_dotenv(dotenv_path="config")
intents = discord.Intents.all()

### Set prefix
#bot = commands.Bot(command_prefix="!", intents=intents)
bot = discord.Bot()

########################################################################################################
## START OF PROCESS ##
########################################################################################################


async def create_player(id, manager):
    with open(f_players, "a") as pfile:
        i = 1

        # ID > 100000 -> team created by a Discord user
        if int(id) > 1000000:
            manager = manager
            m_ovr = 50
        else:
            manager = "BOT"
            m_ovr = randint(70, 90)

        m_pos = "COACH"
        m_owner = id
        nationalities = ["gb", "us", "au", "fr", "ca", "es", "cu", "mx"]
        nat = choice(nationalities)
        nft = "0"
        rarity = "no"
        pfile.write(manager + "," + str(m_ovr) + "," + m_pos + "," + str(m_owner) + "," + nat + "," + nft + "," + rarity + "\n")

        while i <= 11:
            # To create better bot teams than players teams
            if int(id) < 1000000:
                ovr = randint(65, 82)
            else:
                # Value for players generate by Discord User creation team (Issue #2)
                ovr = randint(25, 35)

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
            pfile.write(displayName + "," + str(ovr) + "," + position + "," + str(owner) + "," + nat + "," + nft + "," + rarity + ",\n")
            i += 1


async def generate_player(i):
    displayName = names.get_full_name(gender='male')
    rare = randint(0, 100)
    nationalities = ["gb", "us", "au", "fr", "ca", "es", "cu", "mx"]
    nat = choice(nationalities)

    if rare <= 70:
        ovr = randint(27, 32)
    elif 89 >= rare > 69:
        ovr = randint(33, 37)
    elif 97 >= rare > 89:
        ovr = randint(38, 41)
    elif rare > 97:
        ovr = randint(42, 45)

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
    nft = "0"
    rarity = "no"
    new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + "," + nat + "," + nft + "," + rarity + ",\n"
    return new_line


async def scout_player(id, num, name, ovr, pos, nat):
    # nationalities = ["gb", "us", "au", "fr", "ca", "es", "cu", "mx"]
    nat = nat
    nft = "0"
    ovr = int(ovr)
    rarity = "no"
    if ovr >= 85:
        rarity = "legend"
    elif ovr >= 75:
        rarity = "rare"
    elif ovr >= 65:
        rarity = "uncommon"
    elif ovr >= 45:
        rarity = "common"

    if ovr >= 45:
        nft = "1"

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
                    new_line = displayName + "," + str(ovr) + "," + position + "," + str(owner) + "," + nat + "," + nft + "," + rarity + ",\n"
                    replace = line.replace(line, new_line)
                    line = replace
                    if "," not in line:
                        line = ",,,,\n"
        except:
            continue
        playerlist.append(line)
    # Replace entry in player file
    pfile.seek(0)
    pfile.truncate(0)
    pfile.writelines(playerlist)
    pfile.close()


async def view_team(id):
    # Find team which owned by called player
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


async def simulate(id, vs, event):
    # Find player's team information
    t_info = await view_team(id)
    p_info = await view_players(id)
    event = event

    def player_form(teamform):

        i = randint(1, 100)

        dict_form = {
            0: -5,
            1: -3,
            2: -1,
            3: 1,
            4: 3,
            5: 5
        }

        playerform = int(teamform)

        if i < 30:
            playerform -= 1
        if i > 70:
            playerform += 1

        if playerform < 0:
            playerform = 0
        elif playerform > 5:
            playerform = 5

        playerbonus = dict_form[playerform]

        return playerbonus


    ### Away team stats = opponent, if errors : match vs bot team
    try:
        t_vs_info = await view_team(vs)
        p_vs_info = await view_players(vs)
        team_name_away = t_vs_info.split(",")[0]
        team_form_away = t_vs_info.split(",")[3]
        away_man = p_vs_info[0]
        away_p1 = p_vs_info[1]
        away_p1_form = player_form(team_form_away)
        away_p1_ovr = int(away_p1.split(',')[1]) + away_p1_form

        away_p2 = p_vs_info[2]
        away_p2_form = player_form(team_form_away)
        away_p2_ovr = int(away_p2.split(',')[1]) + away_p2_form

        away_p3 = p_vs_info[3]
        away_p3_form = player_form(team_form_away)
        away_p3_ovr = int(away_p3.split(',')[1]) + away_p3_form

        away_p4 = p_vs_info[4]
        away_p4_form = player_form(team_form_away)
        away_p4_ovr = int(away_p4.split(',')[1]) + away_p4_form

        away_p5 = p_vs_info[5]
        away_p5_form = player_form(team_form_away)
        away_p5_ovr = int(away_p5.split(',')[1]) + away_p5_form

        away_p6 = p_vs_info[6]
        away_p6_form = player_form(team_form_away)
        away_p6_ovr = int(away_p6.split(',')[1]) + away_p6_form

        away_p7 = p_vs_info[7]
        away_p7_form = player_form(team_form_away)
        away_p7_ovr = int(away_p7.split(',')[1]) + away_p7_form

        away_p8 = p_vs_info[8]
        away_p8_form = player_form(team_form_away)
        away_p8_ovr = int(away_p8.split(',')[1]) + away_p8_form

        away_p9 = p_vs_info[9]
        away_p9_form = player_form(team_form_away)
        away_p9_ovr = int(away_p9.split(',')[1]) + away_p9_form

        away_p10 = p_vs_info[10]
        away_p10_form = player_form(team_form_away)
        away_p10_ovr = int(away_p10.split(',')[1]) + away_p10_form

        away_p11 = p_vs_info[11]
        away_p11_form = player_form(team_form_away)
        away_p11_ovr = int(away_p11.split(',')[1]) + away_p11_form

        away_ovr = round((away_p1_ovr + away_p2_ovr + away_p3_ovr + away_p4_ovr + away_p5_ovr + away_p6_ovr + away_p7_ovr +
                    away_p8_ovr + away_p9_ovr + away_p10_ovr + away_p11_ovr) / 11)

    except:
        team_name_away = "MFL Team"
        away_ovr = randint(65, 72)

    ### Home team stats
    team_name_home = t_info.split(",")[0]
    team_form_home = t_info.split(",")[3]
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
    home_p1_form = player_form(team_form_home)
    home_p1_ovr = int(home_p1.split(',')[1]) + home_p1_form

    home_p2_form = player_form(team_form_home)
    home_p2_ovr = int(home_p2.split(',')[1]) + home_p2_form

    home_p3_form = player_form(team_form_home)
    home_p3_ovr = int(home_p3.split(',')[1]) + home_p3_form

    home_p4_form = player_form(team_form_home)
    home_p4_ovr = int(home_p4.split(',')[1]) + home_p4_form

    home_p5_form = player_form(team_form_home)
    home_p5_ovr = int(home_p5.split(',')[1]) + home_p5_form

    home_p6_form = player_form(team_form_home)
    home_p6_ovr = int(home_p6.split(',')[1]) + home_p6_form

    home_p7_form = player_form(team_form_home)
    home_p7_ovr = int(home_p7.split(',')[1]) + home_p7_form

    home_p8_form = player_form(team_form_home)
    home_p8_ovr = int(home_p8.split(',')[1]) + home_p8_form

    home_p9_form = player_form(team_form_home)
    home_p9_ovr = int(home_p9.split(',')[1]) + home_p9_form

    home_p10_form = player_form(team_form_home)
    home_p10_ovr = int(home_p10.split(',')[1]) + home_p10_form

    home_p11_form = player_form(team_form_home)
    home_p11_ovr = int(home_p11.split(',')[1]) + home_p11_form

    home_ovr = round((home_p1_ovr + home_p2_ovr + home_p3_ovr + home_p4_ovr + home_p5_ovr + home_p6_ovr + home_p7_ovr +
                home_p8_ovr + home_p9_ovr + home_p10_ovr + home_p11_ovr) / 11)

    ### Matchs initialisation
    home_info = []
    away_info = []
    commentary = []
    score_home = 0
    score_away = 0
    minutes = randint(92, 96)

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

    ## Give a balance between the 2 teams (if same OVR : 1-50 and 51-100 to find who makes the action)
    ratio = round(50 + 2 * home_bonus)

    # % per minute to have an action, in fact it will be nb_actions / minutes
    nb_actions = 4 * note + randint(1, bonus)

    i = 0

    ### Lists of events (minutes, score_home, score_away)
    matchevents = []
    home_scorers = []
    away_scorers = []

    home_scorers.append("\u200b")
    away_scorers.append("\u200b")
    commentary.append("The match begins !")

    def whoscore(team):
        ## Define scoring probabilities
        what = randint(1, 20)
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
        # Update f_goals
        if event == "no":
            pfile = open(f_goals, "r+")
        else:
            pfile = open("goals_"+event+".csv", "r+")

        playerfile = pfile.readlines()
        playerlist = []
        status = 0

        if len(playerfile) > 0:
            for line in playerfile:

                fplayer = line.split(",")[1]
                fteam = line.split(",")[2]

                if (fplayer == player) and (fteam == team):
                    fgoals = int(line.split(",")[0])
                    newgoals = fgoals + 1
                    new_line = str(newgoals) + "," + player + "," + team + ",\n"
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
        else:
            newgoals = 1
            pfile.write(str(newgoals) + "," + player + "," + team + ",\n")

        pfile.close()

    while i < minutes:
        i += 1
        x = randint(1, minutes)
        hvalue = home_scorers[i - 1]
        avalue = away_scorers[i - 1]

        ### Déclenchement actions
        if x < nb_actions:
            who_attack = randint(1, 100)
            if who_attack > ratio:
                who, what, team = whoscore("away")
            else:
                who, what, team = whoscore("home")

            if what == "Goal":

                if team == "home":
                    score_home += 1
                    hvalue = hvalue + "," + who
                    commentary.append("What a goal for " + team_name_home + " by " + who)
                    register_goals(who, team_name_home)
                else:
                    score_away += 1
                    avalue = avalue + "," + who
                    commentary.append("What a goal for " + team_name_away + " by " + who)
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
            commentary[minutes] = "At home, **" + team_name_home + "** wins the game against " + team_name_away + "."
        elif score_home < score_away:
            commentary[minutes] = "**" + team_name_away + "** makes a great match and overcomes " + team_name_home + "."
        else:
            commentary[
                minutes] = "What a game !\n But " + team_name_home + " and " + team_name_away + " " + "could not tell the difference"
    matchinfo.append(commentary)

    return matchinfo, matchevents, home_scorers, away_scorers

async def viewteam(id):
    user_id = str(id)
    t_info = await view_team(user_id)

    if t_info is None or t_info == "Error":
        return "You have no team !"
    else:
        p_info = await view_players(user_id)
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


async def viewleads(i):
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


async def viewevents(i):
    with open(f_events, "r") as tevents:
        eventfile = tevents.readlines()
        eventlist = []

        for event in eventfile:
            eventcode = event.split(",")[0]
            eventname = event.split(",")[1]
            eventdesc = event.split(",")[2]
            eventstatus = event.split(",")[3]
            eventkind = event.split(",")[4]

            if int(eventstatus) > 1:
                continue

            if i == "all":
                eventlist.append(event)
            elif i == eventkind:
                eventlist.append(event)

        return eventlist


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
            title="Match Settings", description="Choose your opponent or play an event", color=default_color)

        embedopponents = "`" + teamlist[0].split(",")[0] + "` *" + teamlist[0].split(",")[2] + "*\n"
        embedopponents = embedopponents + "`" + teamlist[1].split(",")[0] + "` *" + teamlist[1].split(",")[2] + "*\n"
        embedteam.add_field(name="Opponents", value=embedopponents)

        return embedteam, teamlist


async def scout(id):
    user_id = str(id)
    p_info = await view_players(user_id)

    number = randint(1, 11)
    newp_info = await generate_player(number)
    name = newp_info.split(",")[0]
    ovr = newp_info.split(",")[1]
    pos = newp_info.split(",")[2].upper()
    nat = newp_info.split(",")[4]
    rarity = "no"
    rarity_flag = "⚫"
    nft = "0"

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
    embeddescription = ":flag_" + nat + ":`" + str(i) + " - " + pos + " " + ovr + "` " + rarity_flag + " *" + name + "*\n"
    oldplayer = ":flag_" + old_nat + ":`" + str(i) + " - " + old_pos + " " + old_ovr + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer

async def scoutnft(id, name, ovr, pos, nat, rarity):
    user_id = str(id)
    p_info = await view_players(user_id)

    positions = {
        'GK': 1,
        'LB': 2,
        'CB': 3,
        'RB': 5,
        'CDM': 6,
        'CM': 6,
        'CAM': 8,
        'AM': 8,
        'LW': 9,
        'LM': 9,
        'RW': 10,
        'RM': 10,
        'CF': 11,
        'ST': 11,
        'FW': 11
    }

    name = name
    ovr = int(ovr)
    pos = pos
    number = positions[pos]
    nat = nat
    nft = "1"
    rarity = rarity

    if rarity == "common":
        rarity_flag = "⚪"
    elif rarity == "uncommon":
        rarity_flag = "🟢"
    elif rarity == "rare":
        rarity_flag = "🔵"
    elif rarity == "legend":
        rarity_flag = "🟣"

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
    playerinfo.append(nft)
    playerinfo.append(rarity)

    i = int(number)
    default_color = 0xffff00

    embedplayer = discord.Embed(
        title=name, description="You find a new player !", color=default_color)
    embeddescription = ":flag_" + nat + ":`" + str(i) + " - " + pos + " " + str(ovr) + "` " + rarity_flag + " *" + name + "*\n"
    oldplayer = ":flag_" + old_nat + ":`" + str(i) + " - " + old_pos + " " + old_ovr + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer

#### SIMULATE MATCHES ####
async def play(id, vs, events):
    user_id = str(id)
    print(events)
    matchinfos, matchsevents, home_scorers, away_scorers = await simulate(user_id, vs, events)
    home_info = matchinfos[0]
    away_info = matchinfos[1]
    home_name = home_info[0]
    away_name = away_info[0]
    commentary = matchinfos[4]

    description_start = "Welcome to the match !\nToday, " + home_name + " will face " + away_name + ".\n\nThe teams enter the " \
                                                                                                    "field... let's go! "
    description_default = "Welcome to the match !\nToday, " + home_name + " will face " + away_name + ".\n"

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

#### Show NFT players
async def view_nfts(id, indice):

    nations_prefix = {
        'ALGERIA': 'dz',
        'ARGENTINA': 'ar',
        'AUSTRALIA': 'au',
        'AUSTRIA': 'at',
        'BELGIUM': 'be',
        'BRAZIL': 'br',
        'CANADA': 'ca',
        'CAMEROON': 'cm',
        'CHILE': 'cl',
        'COLOMBIA': 'co',
        'COSTA_RICA': 'cr',
        'CROATIA': 'hr',
        'CZECH_REPUBLIC': 'cz',
        'DENMARK': 'dk',
        'ECUADOR': 'ec',
        'ENGLAND': 'gb',
        'EGYPT': 'eg',
        'FRANCE': 'fr',
        'GERMANY': 'de',
        'HUNGARY': 'hu',
        'KOREA_REPUBLIC': 'kr',
        'ITALY': 'it',
        'IRAN': 'ir',
        'JAPAN': 'jp',
        'MEXICO': 'mx',
        'MOROCCO': 'ma',
        'NETHERLANDS': 'nl',
        'NIGERIA': 'ng',
        'NORWAY': 'no',
        'PARAGUAY': 'py',
        'PERU': 'pe',
        'POLAND': 'pl',
        'PORTUGAL': 'pt',
        'UKRAINE': 'ua',
        'REPUBLIC_OF_IRELAND': 'ie',
        'ROMANIA': 'ro',
        'RUSSIA': 'ru',
        'SAUDI_ARABIA': 'sa',
        'SCOTLAND': 'gb',
        'SENEGAL': 'sn',
        'SERBIA': 'rs',
        'SLOVAKIA': 'sk',
        'SPAIN': 'es',
        'SWITZERLAND': 'ch',
        'SWEDEN': 'se',
        'TUNISIA': 'tn',
        'TURKEY': 'tr',
        'UNITED_STATES': 'us',
        'URUGUAY': 'uy',
        'WALES': 'gb'

    }

    host = "https://z519wdyajg.execute-api.us-east-1.amazonaws.com/prod/users/discord/"
    user_id = str(id)
    link = host+user_id+"/players"
    getnft = requests.get(link)
    nfts = getnft.json()

    i = 0

    playerslist = []
    formatlist = []
    embeddesclist = []
    embeddescription = ""

    while i < len(nfts):
        nationality = nfts[i]['metadata']['nationalities'][0]
        try:
            nation = nations_prefix[nationality]
        except:
            nation = nationality
        positions = nfts[i]['metadata']['positions'][0]
        ovr = int(nfts[i]['metadata']['overall'])
        firstName = nfts[i]['metadata']['firstName']
        lastName = nfts[i]['metadata']['lastName']
        displayName = firstName + " " + lastName

        if ovr >= 85:
            rarity = "legend"
        elif ovr >= 75:
            rarity = "rare"
        elif ovr >= 65:
            rarity = "uncommon"
        else:
            rarity = "common"

        embeddescription = embeddescription + ":flag_" + nation + ":`" + positions + "  " + str(ovr) + "`" + rarity + " *" + displayName + "*\n"
        playerslist.append(nation+","+positions+","+str(ovr)+","+displayName+","+rarity)

        i += 1

        if (i % 5 == 0) or (i == len(nfts)):
            formatlist.append(playerslist)
            playerslist = []
            embeddesclist.append(embeddescription)
            embeddescription = ""

    if int(indice) > len(embeddesclist):
        indice = len(embeddesclist) - 1
    elif int(indice) < 0:
        indice = 0

    return formatlist

#### BOT IS READY ####
@bot.event
async def on_ready():
    print("Bot Ready")

### Discord configurations ###
gamechan = [983723647002882058, 989056372198998076]
adminid = "593086239024873483"


#### CREATE TEAM ####
@bot.command(name='create', description='The first step to enter into the game...')
async def create(ctx, name):
    # Usage : !create Team_Name
    if ctx.channel.id in gamechan:
        teamname = name
        with open(f_teams, "r+") as tfile:
            user = ctx.interaction.user
            user_id = str(user.id)
            if user.id > 1000000:
                print(user)
                username = user.name
            else:
                username = "BOT"
            team_id = user_id
            if user_id in tfile.read():
                if user_id == adminid:
                    team_id = str(randint(1, 999999))
                    tfile.write(teamname + "," + team_id + ",no,3,\n")
                    await create_player(team_id, username)
                    await ctx.respond("Team " + teamname + " created !", ephemeral=True)
                else:
                    await ctx.respond("Sorry, you already have a team !", ephemeral=True)
            else:
                tfile.write(teamname + "," + team_id + ",yes,3,\n")
                await create_player(team_id, username)
                await ctx.respond("Team " + teamname + " created !", ephemeral=True)


@bot.command(name='view')
async def change(ctx, user: discord.User):
    print(ctx.channel.id)
    if ctx.channel.id in gamechan:
        embedteam = await viewteam(str(user.id))
        await ctx.respond(embed=embedteam, ephemeral=False)

#### Menu display
@bot.command(name="test")
async def test(ctx):
    await ctx.respond("Test", ephemeral=True)


@bot.command(name='match')
async def match(ctx, user1: discord.User, user2: discord.User):
    if ctx.channel.id in gamechan:
        events = "no"
        match = await play(str(user1.id), str(user2.id), events)
        view = View()
        default_color = 0x00ff00
        embedmenu = discord.Embed(
            title='Discord Football Game', color=default_color)

        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=True)

        for x in match:
            #await showmenu.edit(view=view, embed=x)
            await showmenu.edit_original_message(view=view, embed=x)
            await asyncio.sleep(1)


#### Menu display
@bot.command(name='game', description='Access to the menu, build your team and compete...')
async def game(ctx):
    if ctx.channel.id in gamechan:
        user_id = str(ctx.interaction.user.id)
        user_name = str(ctx.interaction.user)
        default_color = 0x00ff00
        embedmenu = discord.Embed(
            title='Discord Football Game', color=default_color)
        embedmenu.add_field(name="Hello", value="Want play ?", inline=True)

        button_play = Button(label="Play", style=discord.ButtonStyle.green, custom_id="play", emoji="⚽")
        button_scout = Button(label="Scout", style=discord.ButtonStyle.green, custom_id="scout", emoji="👨")
        button_nfts = Button(label="NFT", style=discord.ButtonStyle.blurple, row=2, custom_id="nfts", emoji="🎉")
        button_team = Button(label="Team", style=discord.ButtonStyle.green, custom_id="team", emoji="👥")
        button_recruit = Button(label="Recruit", style=discord.ButtonStyle.green, custom_id="recruit", emoji="✅")
        button_letleave = Button(label="Return", style=discord.ButtonStyle.grey, custom_id="letleave", emoji="❌")
        button_finishmatch = Button(label="Skip", style=discord.ButtonStyle.blurple, custom_id="finishmatch")
        button_leaderboard = Button(label="Leaderboard", style=discord.ButtonStyle.grey, row=1, custom_id="leaderboard",
                                    emoji="🏆")
        button_events = Button(label="Events", style=discord.ButtonStyle.blurple, row=1, custom_id="events", emoji="⭐")

        viewdefault = View()
        viewdefault.add_item(button_team)
        viewdefault.add_item(button_scout)
        viewdefault.add_item(button_play)
        viewdefault.add_item(button_events)
        viewdefault.add_item(button_leaderboard)
        viewdefault.add_item(button_nfts)

        viewmatch = View()
        viewmatch.add_item(button_finishmatch)
        viewmatch.add_item(button_team)

        skip = 0

        async def button_play_callback(interaction):
            if str(interaction.user) == user_name:
                embedteam, teamlist = await findteam(user_id)
                eventlist = await viewevents("vs")

                viewopponents = View()
                i = 1

                if eventlist[0] != "":
                    button_ev1 = None
                    button_ev2 = None
                    button_ev3 = None
                    button_ev4 = None
                    button_ev5 = None

                    for event in eventlist:
                        eventcode = event.split(",")[0]
                        eventname = event.split(",")[1]
                        eventdesc = event.split(",")[2]
                        eventstatus = event.split(",")[3]
                        eventkind = event.split(",")[4]
                        eventopponent = event.split(",")[5]

                        if i == 1:
                            button_ev1 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=eventcode+","+eventopponent)
                            viewopponents.add_item(button_ev1)
                        elif i == 2:
                            button_ev2 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=eventcode+","+eventopponent)
                            viewopponents.add_item(button_ev2)
                        elif i == 3:
                            button_ev3 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=eventcode+","+eventopponent)
                            viewopponents.add_item(button_ev3)
                        elif i == 4:
                            button_ev4 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=eventcode+","+eventopponent)
                            viewopponents.add_item(button_ev4)
                        elif i == 5:
                            button_ev5 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=1, custom_id=eventcode+","+eventopponent)
                            viewopponents.add_item(button_ev5)
                        i += 1



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

                await showmenu.edit_original_message(view=viewopponents, embed=embedteam)
                await interaction.response.defer()

                async def button_vs_callback(interaction):
                    if str(interaction.user) == user_name:
                        global skip
                        skip = 0

                        vs = interaction.data['custom_id']
                        if "event_" in vs:
                            events = vs.split(",")[0]
                            vs = vs.split(",")[1]
                        else:
                            events = "no"

                        embedlist = await play(user_id, vs, events)

                        async def button_finishmatch_callback(interaction):
                            global skip

                            if str(interaction.user) == user_name:
                                skip = 1
                                await showmenu.edit_original_message(view=viewmatch, embed=embedlist[-1])
                                await interaction.response.defer()

                        for x in embedlist:

                            button_finishmatch.callback = button_finishmatch_callback
                            if skip == 1:
                                break

                            await showmenu.edit_original_message(view=viewmatch, embed=x)
                            await asyncio.sleep(1)

                            try:
                                await interaction.response.defer()
                            except discord.InteractionResponded:
                                continue

                button_random.callback = button_vs_callback
                button_vs1.callback = button_vs_callback
                button_vs2.callback = button_vs_callback
                if button_ev1:
                    button_ev1.callback = button_vs_callback
                if button_ev2:
                    button_ev2.callback = button_vs_callback
                if button_ev3:
                    button_ev3.callback = button_vs_callback
                if button_ev4:
                    button_ev4.callback = button_vs_callback
                if button_ev5:
                    button_ev5.callback = button_vs_callback

        async def button_team_callback(interaction):
            if str(interaction.user) == user_name:
                embedteam = await viewteam(user_id)

                view = View()
                view.add_item(button_team)
                view.add_item(button_scout)
                view.add_item(button_play)
                view.add_item(button_events)
                view.add_item(button_leaderboard)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedteam)
                await interaction.response.defer()

        async def button_nfts_callback(interaction):
            if str(interaction.user) == user_name:
                global indice
                indice = 0

                await interaction.response.defer()

                playerslist = await view_nfts(user_id, indice)

                async def nftembed(playerslist, indice):
                    default_color = 0xffff00
                    embednfts = discord.Embed(
                        title="Your NFTS", description="Below your squad", color=default_color)
                    description = ""
                    buttons = []
                    b1 = None
                    b2 = None
                    b3 = None
                    b4 = None
                    b5 = None
                    i = 0
                    for x in playerslist[indice]:
                        nation = x.split(",")[0]
                        positions = x.split(",")[1]
                        ovr = x.split(",")[2]
                        displayName = x.split(",")[3]
                        rarity = x.split(",")[4]

                        if rarity == "common":
                            rarity_flag = "⚪"
                        elif rarity == "uncommon":
                            rarity_flag = "🟢"
                        elif rarity == "rare":
                            rarity_flag = "🔵"
                        elif rarity == "legend":
                            rarity_flag = "🟣"

                        if len(positions) == 3:
                            description = description + ":flag_" + nation + ":`" + positions + " " + str(
                                ovr) + "`" + rarity_flag + " *" + displayName + "*\n"
                        else:
                            description = description + ":flag_" + nation + ":`" + positions + "  " + str(
                                ovr) + "`" + rarity_flag + " *" + displayName + "*\n"

                        if i == 0:
                            b1 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b1)
                        elif i == 1:
                            b2 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b2)
                        elif i == 2:
                            b3 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b3)
                        elif i == 3:
                            b4 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b4)
                        elif i == 4:
                            b5 = Button(label=displayName, style=discord.ButtonStyle.blurple, row=1, custom_id="Player "+str(i))
                            buttons.append(b5)
                        i += 1

                    embednfts.add_field(name="Players", value=description)

                    viewnfts = View()
                    viewnfts.add_item(button_previous)
                    viewnfts.add_item(button_next)
                    viewnfts.add_item(button_team)

                    async def button_scoutnft_callback(interaction):
                        if str(interaction.user) == user_name:
                            viewscout = View()
                            viewscout.add_item(button_team)
                            viewscout.add_item(button_recruit)
                            viewscout.add_item(button_letleave)

                            select = int(interaction.data['custom_id'].split(" ")[1])
                            player = playerslist[indice][select]
                            nat = player.split(",")[0]
                            pos = player.split(",")[1]
                            ovr = player.split(",")[2]
                            name = player.split(",")[3]
                            rarity = player.split(",")[4]
                            embedscout = await scoutnft(user_id, name, ovr, pos, nat, rarity)

                            await showmenu.edit_original_message(view=viewscout, embed=embedscout)
                            await interaction.response.defer()

                    if b1:
                        b1.callback = button_scoutnft_callback
                    if b2:
                        b2.callback = button_scoutnft_callback
                    if b3:
                        b3.callback = button_scoutnft_callback
                    if b4:
                        b4.callback = button_scoutnft_callback
                    if b5:
                        b5.callback = button_scoutnft_callback

                    for x in buttons:
                        viewnfts.add_item(x)

                    return embednfts, viewnfts

                async def button_move_callback(interaction):
                    global indice
                    if str(interaction.user) == user_name:
                        page = interaction.data['custom_id']
                        if page == "next":
                            indice += 1
                        elif page == "prev":
                            indice -= 1

                        embednfts, viewnfts = await nftembed(playerslist, indice)


                        await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                        await interaction.response.defer()

                button_previous = Button(style=discord.ButtonStyle.blurple, custom_id="prev", emoji="◀")
                button_next = Button(style=discord.ButtonStyle.blurple, custom_id="next", emoji="▶")
                button_next.callback = button_move_callback
                button_previous.callback = button_move_callback

                embednfts, viewnfts = await nftembed(playerslist, indice)

                await showmenu.edit_original_message(view=viewnfts, embed=embednfts)
                #await interaction.response.defer()

        async def button_scout_callback(interaction):
            if str(interaction.user) == user_name:
                viewscout = View()
                viewscout.add_item(button_team)
                viewscout.add_item(button_recruit)
                viewscout.add_item(button_letleave)
                embedplayer = await scout(user_id)
                await showmenu.edit_original_message(view=viewscout, embed=embedplayer)
                await interaction.response.defer()

        async def button_leaderboard_callback(interaction):
            if str(interaction.user) == user_name:

                viewlead = View()
                viewlead.add_item(button_team)
                viewlead.add_item(button_scout)
                viewlead.add_item(button_play)

                embedlead = await viewleads(user_id)
                eventlist = await viewevents("vs")
                i = 1

                button_global = Button(label="Global", style=discord.ButtonStyle.blurple,
                                        row=1, custom_id="goals")
                viewlead.add_item(button_global)

                if eventlist[0] != "":
                    button_ev1 = None
                    button_ev2 = None
                    button_ev3 = None
                    button_ev4 = None
                    button_ev5 = None

                    for event in eventlist:
                        eventcode = event.split(",")[0]
                        eventname = event.split(",")[1]
                        print(eventname)
                        eventdesc = event.split(",")[2]
                        eventstatus = event.split(",")[3]
                        eventkind = event.split(",")[4]
                        eventopponent = event.split(",")[5]

                        if i == 1:
                            button_ev1 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=eventcode+","+eventopponent)
                            viewlead.add_item(button_ev1)
                        elif i == 2:
                            button_ev2 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=eventcode+","+eventopponent)
                            viewlead.add_item(button_ev2)
                        elif i == 3:
                            button_ev3 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=eventcode+","+eventopponent)
                            viewlead.add_item(button_ev3)
                        elif i == 4:
                            button_ev4 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=eventcode+","+eventopponent)
                            viewlead.add_item(button_ev4)
                        elif i == 5:
                            button_ev5 = Button(label=eventname, style=discord.ButtonStyle.blurple,
                                                    row=2, custom_id=eventcode+","+eventopponent)
                            viewlead.add_item(button_ev5)
                        i += 1

                async def button_leads_callback(interaction):
                    event = interaction.data['custom_id'].split(",")[0]
                    print(event)

                    embedlead = await viewleads(event)

                    await showmenu.edit_original_message(view=viewlead, embed=embedlead)
                    await interaction.response.defer()


                button_global.callback = button_leads_callback
                if button_ev1:
                    button_ev1.callback = button_leads_callback
                if button_ev2:
                    button_ev2.callback = button_leads_callback
                if button_ev3:
                    button_ev3.callback = button_leads_callback
                if button_ev4:
                    button_ev4.callback = button_leads_callback
                if button_ev5:
                    button_ev5.callback = button_leads_callback

                await showmenu.edit_original_message(view=viewlead, embed=embedlead)
                await interaction.response.defer()

        async def button_events_callback(interaction):
            if str(interaction.user) == user_name:
                eventlist = await viewevents("all")

                default_color = 0x00ff00
                embedevent = discord.Embed(
                    title="Events", description="Below the list of current events", color=default_color)

                for event in eventlist:
                    eventcode = event.split(",")[0]
                    eventname = event.split(",")[1]
                    eventdesc = event.split(",")[2]
                    eventstatus = event.split(",")[3]
                    eventkind = event.split(",")[4]

                    embedevent.add_field(name=eventname, value=eventdesc)

                await showmenu.edit_original_message(view=view, embed=embedevent)
                await interaction.response.defer()

        async def button_recruit_callback(interaction):
            if str(interaction.user) == user_name:
                playerscheck = interaction.message.embeds[0].fields
                playersinfos = playerscheck[0].value.split(" ")
                nat = playersinfos[0].split("`")[0].split("_")[1].replace(":", "")
                num = playersinfos[0].split("`")[1]

                pos = playersinfos[2]
                ovr = playersinfos[3].replace("`", "")
                name = playersinfos[5] + " " + playersinfos[6]

                name = name.replace("*", "")
                await scout_player(user_id, num, name, ovr, pos, nat)
                embedteam = await viewteam(user_id)

                view = View()
                view.add_item(button_team)
                view.add_item(button_scout)
                view.add_item(button_play)
                view.add_item(button_events)
                view.add_item(button_leaderboard)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedteam)
                await interaction.response.defer()

        async def button_letleave_callback(interaction):
            if str(interaction.user) == user_name:

                view = View()
                view.add_item(button_team)
                view.add_item(button_scout)
                view.add_item(button_play)
                view.add_item(button_events)
                view.add_item(button_leaderboard)
                view.add_item(button_nfts)

                await showmenu.edit_original_message(view=view, embed=embedmenu)
                await interaction.response.defer()

        button_play.callback = button_play_callback
        button_events.callback = button_events_callback
        button_leaderboard.callback = button_leaderboard_callback
        button_team.callback = button_team_callback
        button_scout.callback = button_scout_callback
        button_recruit.callback = button_recruit_callback
        button_letleave.callback = button_letleave_callback
        button_nfts.callback = button_nfts_callback

        view = viewdefault

        showmenu = await ctx.respond("\u200b", view=view, embed=embedmenu, ephemeral=True)


#### BOT TOKEN ########################
with open('token.txt', 'r') as f:
    token = f.readline()
bot.run(token)
