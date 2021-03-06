import random
import discord
from random import randint
import events
import teams
import players
import commentaries
import nations
from config import config

f_goals = config["dataPath"] + "goals.csv"
f_points = config["dataPath"] + "points.csv"

class Teams:
    def __init__(self, home, away):
        self.home = home
        self.away = away


class Score:
    def __init__(self, home, away):
        self.home = home
        self.away = away


class Event:
    def __init__(self, kind, player, team, minute):
        self.kind = kind
        self.player = player
        self.team = team
        self.minute = minute


class MatchEvent:
    def __init__(self, teams: Teams, score: Score, event, commentary, minutes, note):
        self.teams = teams
        self.score = score
        self.event = event
        self.commentary = commentary
        self.minutes = minutes
        self.note = note


async def simulate(id, vs, event):
    # Find player's team information
    eventinfo = await events.getbyCode(event)
    leads = "byPlayer"

    if len(eventinfo) > 0:
        leads = eventinfo[0].leaderboard

    if event == "international":
        t_info = await nations.get(id)
        playershome = await players.getnation(id)
        if len(playershome) == 11:
            playershome.insert(0, "Manager")

    else:
        t_info = await teams.get(id)
        playershome = await players.get(id)

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
        try:
            playerform = int(teamform)
        except:
            playerform = 3

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

    if event == "international":
        t_vs_info = await nations.get(vs)
        playersaway = await players.getnation(vs)
        if len(playersaway) == 11:
            playersaway.insert(0, "Manager")

    else:
        t_vs_info = await teams.get(vs)
        playersaway = await players.get(vs)

    team_name_away = t_vs_info.split(",")[0]
    try:
        team_form_away = t_vs_info.split(",")[3]
    except:
        team_form_away = 3

    away_man = playersaway[0]
    away_ovr_list = []
    for x in playersaway:
        if x == "Manager":
            continue
        if x.pos != "COACH":
            x.form = player_form(team_form_away)
            x.ovr += x.form
            away_ovr_list.append(x.ovr)

    away_ovr = round(sum(away_ovr_list) / len(away_ovr_list))


    ### Home team stats
    team_name_home = t_info.split(",")[0]
    team_form_home = t_info.split(",")[3]

    teamsname = Teams(team_name_home, team_name_away)
    home_man = playershome[0]
    home_ovr_list = []

    for x in playershome:
        if x == "Manager":
            continue
        if x.pos != "COACH":
            x.form = player_form(team_form_home)
            x.ovr += x.form
            home_ovr_list.append(x.ovr)

    home_ovr = round(sum(home_ovr_list) / len(home_ovr_list))

    ### Matchs initialisation
    score_home = 0
    score_away = 0
    score = Score(score_home, score_away)
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
    eventlist = []
    curevent = "\u200b"

    startPlayer = playershome[randint(2,11)]
    commentary = commentaries.getCommentary('matchStart', {'HOME_TEAM': teamsname.home, 'AWAY_TEAM': teamsname.away, 'START_PLAYER_NAME': startPlayer.displayName})

    def get_actions(team):
        ## Define scoring probabilities
        what = randint(1, 20)

        shootprob = [0,3,9,15,18,24,30,42,57,72,100]

        if what > 17:
            what = "Shoot"
            success = 1
        elif what > 15:
            what = "Bonus"
            success = 1
        elif what > 4:
            what = "Shoot"
            success = 0
        else:
            what = "Fault"

        indice = 1

        if what == "Shoot":
            number = randint(1, 100)
            for x in shootprob:
                if number > x:
                    indice += 1

        else:
            indice = randint(2,11)

        if what == "Fault":
            number = randint(1,15)
            if number > 10:
                success = 0
            elif 10 >= number > 2:
                success = 1
            else:
                success = 2

        if team == "home":
            teamname = team_name_home
            who = playershome[indice]

        if team == "away":
            teamname = team_name_away
            who = playersaway[indice]

        return who, teamname, what, team, success

    async def register_goals(player, team, sort):
        # Update f_goals

        if event == "no":
            pfile = open(f_goals, "r+")
        else:
            pfile = open(config["dataPath"] + "goals_" + event + ".csv", "r+")

        playerfile = pfile.readlines()
        playerlist = []
        newgoals = 1
        status = 0

        if len(playerfile) > 0:
            if sort == "byPlayer":
                new_line = str(newgoals) + "," + team + "," + player + ",\n"
                for line in playerfile:
                    fteam = line.split(",")[1]
                    fplayer = line.split(",")[2]

                    if (fplayer == player) and (fteam == team):
                        fgoals = int(line.split(",")[0])
                        newgoals = fgoals + 1
                        new_line = str(newgoals) + "," + team + "," + player + ",\n"
                        replace = line.replace(line, new_line)
                        line = replace
                        if "," not in line:
                            line = ",,,,\n"
                        status = 1

                    playerlist.append(line)

            elif sort == "byTeam":
                new_line = str(newgoals) + ","+ team + ",\n"
                for line in playerfile:
                    fteam = line.split(",")[1]

                    if fteam == team:
                        fgoals = int(line.split(",")[0])
                        newgoals = fgoals + 1
                        new_line = str(newgoals) + ","+ team + ",\n"
                        replace = line.replace(line, new_line)
                        line = replace
                        if "," not in line:
                            line = ",,,,\n"
                        status = 1

                    playerlist.append(line)

        if status == 0:
            pfile.write(new_line)
        else:
            pfile.seek(0)
            pfile.truncate(0)
            pfile.writelines(playerlist)
        #else:
        #    newgoals = 1
        #    pfile.write(str(newgoals) + "," + player + "," + team + ",\n")

        pfile.close()

    #### Start of the simulation ###############

    matchevent = MatchEvent(teamsname, score, curevent, commentary, i, note)
    eventlist.append(matchevent)

    while i < minutes:

        ## Recheck team value (can change during game)
        home_ovr_list = []
        curevent = "\u200b"

        for x in playershome:
            if x == "Manager":
                continue
            if x.pos != "COACH":
                home_ovr_list.append(x.ovr)

        home_ovr = round(sum(home_ovr_list) / len(home_ovr_list))

        away_ovr_list = []
        for x in playersaway:
            if x == "Manager":
                continue
            if x.pos != "COACH":
                away_ovr_list.append(x.ovr)

        away_ovr = round(sum(away_ovr_list) / len(away_ovr_list))

        home_bonus = round(home_ovr - away_ovr)

        ## Give a balance between the 2 teams (if same OVR : 1-50 and 51-100 to find who makes the action)
        ratio = round(50 + 2 * home_bonus)

        i += 1
        x = randint(1, minutes)

        ### D??clenchement actions
        if x < nb_actions:
            who_attack = randint(1, 100)
            if who_attack > ratio:
                who, whoTeam, what, team, success = get_actions("away")
            else:
                who, whoTeam, what, team, success = get_actions("home")

            if who.isRedCard != True:

                whoplay = who.displayName

                if what == "Shoot":

                    commentary = commentaries.getCommentary('shoot', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})
                    matchevent = MatchEvent(teamsname, score, curevent, commentary, i, note)
                    eventlist.append(matchevent)

                    if success == 1:

                        if team == "home":
                            score_home += 1
                            score = Score(score_home, score_away)
                            if event != "versus":
                                await register_goals(whoplay, teamsname.home, leads)

                        else:
                            score_away += 1
                            score = Score(score_home, score_away)
                            if event != "versus":
                                await register_goals(whoplay, teamsname.away, leads)


                        curevent = Event("goal", whoplay, whoTeam, i)
                        commentary = commentaries.getCommentary('goal',
                                                                {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})

                    else:
                        who.ovr = who.ovr + 2
                        commentary = commentaries.getCommentary('missedShot', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})


                elif what == "Fault":
                    commentary = commentaries.getCommentary('dangerousFoul', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})

                    if success == 0:
                        who.ovr = who.ovr - 3
                        commentary = commentaries.getCommentary('noCardAfterDangerousFoul', {'PLAYER_NAME': whoplay, 'PLAYER_TEAM': whoTeam})

                    if success == 1:
                        if who.isYellowCard == False:
                            who.ovr = who.ovr - 10
                            who.isYellowCard = True
                            curevent = Event("yelcard", whoplay, whoTeam, i)
                            commentary = commentaries.getCommentary('yellowCard',
                                                                    {'PLAYER_TEAM': whoTeam, "PLAYER_NAME": whoplay})
                        else:
                            who.ovr = 0
                            who.isRedCard = True
                            curevent = Event("redcard", whoplay, whoTeam, i)
                            commentary = commentaries.getCommentary('redCard',
                                                                    {'PLAYER_TEAM': whoTeam, "PLAYER_NAME": whoplay})

                elif what == "Bonus":
                    commentary = commentaries.getCommentary('dominant',
                                                            {'DOMINANT_TEAM': teamsname.home if team == "home" else teamsname.away,
                                                             'DOMINATED_TEAM': teamsname.away if team == "home" else teamsname.home})

                else:
                    commentary = commentaries.getCommentary('noAction')

        else:
            commentary = commentaries.getCommentary('noAction')

        matchevents.append(str(i) + "," + str(score_home) + "," + str(score_away))

        matchevent = MatchEvent(teamsname, score, curevent, commentary, i, note)
        eventlist.append(matchevent)

    ### Note review
    if (int(score_away + score_home) <= 1) and (note > 1):
        note = note - 1
    elif int(score_away + score_home) > 3 and (note < 3):
        note = note + 1
    elif (int(score_away + score_home) <= 2) and (note > 3):
        note = note - 1

    ### Points Leaderboard
    async def update_points_leaderboard(team, addpoints):
        status = 0
        points_file = open(f_points, "r+")
        lines = []
        for line in points_file:
            fteam = line.split(",")[1]
            if fteam == team:
                points = int(line.split(",")[0])
                points = points + addpoints
                new_line = str(points) + "," + team + ",\n"
                replace = line.replace(line, new_line)
                line = replace
                if "," not in line:
                    line = ",,,,\n"
                status = 1
            lines.append(line)
        if status == 0:
            new_line = str(addpoints) + "," + team + ",\n"
            points_file.write(new_line)
        else:
            points_file.seek(0)
            points_file.truncate(0)
            points_file.writelines(lines)

    if event == "no":
        if score_home > score_away:
            await update_points_leaderboard(team_name_home, 3)
        elif score_home == score_away:
            await update_points_leaderboard(team_name_home, 1)

    commentaryKey = 'homeWin' if score_home > score_away else "awayWin" if score_home < score_away else "draw"
    commentary = commentaries.getCommentary(commentaryKey, {'HOME_TEAM': team_name_home, 'AWAY_TEAM': team_name_away})

    # Goal reset
    curevent = "\u200b"

    matchevent = MatchEvent(teamsname, score, curevent, commentary, i, note)
    eventlist.append(matchevent)

    return eventlist


#### SIMULATE MATCHES ####
async def play(id, vs, events):
    user_id = str(id)
    eventlist = await simulate(user_id, vs, events)

    home_name = eventlist[0].teams.home
    away_name = eventlist[0].teams.away
    commentary = eventlist[0].commentary

    description_start = "Welcome to the match !\nToday, *" + home_name + "* will face *" + away_name + "*.\n\nThe teams enter the " \
                                                                                                    "field... let's go! "
    description_default = "Welcome to the match !\nToday, *" + home_name + "* will face *" + away_name + "*.\n"

    note = int(eventlist[0].note)
    if note == 1:
        note = "???"
    elif note == 2:
        note = "??????"
    elif note == 3:
        note = "?????????"
    elif note == 4:
        note = "????????????"
    elif note == 5:
        note = "???????????????"

    default_color = 0xffff00
    embedlist = []

    nogoal = "\u200b"
    hgoal = nogoal
    agoal = nogoal
    hcard = nogoal
    acard = nogoal
    lastcommentaries = "\u200b"

    i = 0

    oldcommentaries = []

    for x in eventlist:

        lastevent1 = eventlist[i - 1].commentary
        minutes1 = eventlist[i - 1].minutes

        commentary = x.commentary

        if i > 1:
            if lastevent1 != "---":
                oldcommentaries.append("("+str(minutes1)+"') " + lastevent1)

        if len(oldcommentaries) > 2:
            lastcommentaries = oldcommentaries[-1] + "\n" + oldcommentaries[-2] + "\n" + oldcommentaries[-3]
        elif len(oldcommentaries) > 1:
            lastcommentaries = oldcommentaries[-1] + "\n" + oldcommentaries[-2]
        elif len(oldcommentaries) > 0:
            lastcommentaries = oldcommentaries[-1]

        i += 1

        minutes = x.minutes
        if int(minutes) == 1:
            description = description_start
        elif x == eventlist[len(eventlist) - 1]:
            description = "The referee whistles the end of the game !"
        else:
            description = description_default

        home_score = str(x.score.home)
        away_score = str(x.score.away)
        embedscore = discord.Embed(
            title='Match Day', color=default_color, description=description)
        embedscore.add_field(name=home_name+" - "+away_name, value=home_score+" - "+away_score, inline=True)
        embedscore.add_field(name="MIN", value=str(minutes) + "'", inline=True)
        #embedscore.add_field(name=away_name, value=str(away_score), inline=True)
        embedscore.add_field(name="Commentary", value=commentary, inline=False)
        if len(oldcommentaries) > 0:
            embedscore.add_field(name="\u200b", value=lastcommentaries, inline=False)
        embedscore.add_field(name="\u200b", value="**Goals**", inline=False)

        goals = x.event

        if type(goals) != str:
            if goals.kind == "goal":
                if goals.team == home_name:
                    hgoal += goals.player + " " +str(goals.minute) + "'\n"
                elif goals.team == away_name:
                    agoal += goals.player + " " +str(goals.minute) + "'\n"
            elif goals.kind == "yelcard":
                if goals.team == home_name:
                    hcard += "???? "+goals.player + " " +str(goals.minute) + "'\n"
                elif goals.team == away_name:
                    acard += "???? "+goals.player + " " +str(goals.minute) + "'\n"
            elif goals.kind == "redcard":
                if goals.team == home_name:
                    hcard += "???? "+ goals.player + " " +str(goals.minute) + "'\n"
                elif goals.team == away_name:
                    acard += "???? "+ goals.player + " " +str(goals.minute) + "'\n"

        embedscore.add_field(name="\u200b", value=hgoal, inline=True)
        embedscore.add_field(name="\u200b", value=agoal, inline=True)
        embedscore.add_field(name="\u200b", value="**Events**", inline=False)
        embedscore.add_field(name="\u200b", value=hcard, inline=True)
        embedscore.add_field(name="\u200b", value=acard, inline=True)
        embedscore.add_field(name="Match Note", value=note, inline=False)

        embedlist.append(embedscore)

    return embedlist
