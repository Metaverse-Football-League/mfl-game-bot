import random

import discord
from random import randint
import teams
import players

f_goals = "goals.csv"

commentaries = {
    'win': ["At home, **TEAM1** wins the game against TEAM2",
                "**TEAM1** makes a great match and overcomes TEAM2"],
    'ARGENTINA': 'ar',
    'AUSTRALIA': 'au',
    'AUSTRIA': 'at',
    'BELGIUM': 'be',
    'BRAZIL': 'br',
    'CANADA': 'ca',
    'CAMEROON': 'cm'
}

async def simulate(id, vs, event):
    # Find player's team information
    t_info = await teams.get(id)
    p_info = await players.get(id)
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
        t_vs_info = await teams.get(vs)
        p_vs_info = await players.get(vs)
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

    def get_actions(team):
        ## Define scoring probabilities
        what = randint(1, 20)
        if what > 17:
            what = "Goal"

        else:
            what = "No Goal"

        whonumber = randint(1, 100)
        if team == "home":
            teamname = team_name_home
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
            teamname = team_name_away
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

        ## Recheck team value (can change during game)
        home_bonus = round(home_ovr - away_ovr)
        ## Give a balance between the 2 teams (if same OVR : 1-50 and 51-100 to find who makes the action)
        ratio = round(50 + 2 * home_bonus)

        i += 1
        x = randint(1, minutes)
        hvalue = home_scorers[i - 1]
        avalue = away_scorers[i - 1]

        ### Déclenchement actions
        if x < nb_actions:
            who_attack = randint(1, 100)
            if who_attack > ratio:
                who, what, team = get_actions("away")
            else:
                who, what, team = get_actions("home")

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
            comment = random.choice(commentaries['win'])
            comment = comment.replace("TEAM1", team_name_home)
            comment = comment.replace("TEAM2", team_name_away)
            commentary[minutes] = comment
        elif score_home < score_away:
            comment = random.choice(commentaries['win'])
            comment = comment.replace("TEAM1", team_name_away)
            comment = comment.replace("TEAM2", team_name_home)
            commentary[minutes] = comment
        else:
            commentary[
                minutes] = "What a game !\n But " + team_name_home + " and " + team_name_away + " " + "could not tell the difference"
    matchinfo.append(commentary)

    return matchinfo, matchevents, home_scorers, away_scorers

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
