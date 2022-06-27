import random
import discord
from random import randint
import teams
import players

f_goals = "goals.csv"

commentaries = {
    'win': ["At home, **TEAM1** wins the game against TEAM2",
            "**TEAM1** makes a great match and overcomes TEAM2"]

}


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
    t_info = await teams.get(id)
    playershome = await players.get(id)

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
        playersaway = await players.get(vs)

        team_name_away = t_vs_info.split(",")[0]
        team_form_away = t_vs_info.split(",")[3]

        away_man = playersaway[0]
        away_ovr_list = []
        for x in playersaway:
            if x.pos != "COACH":
                x.form = player_form(team_form_away)
                x.ovr += x.form
                away_ovr_list.append(x.ovr)

        away_ovr = round(sum(away_ovr_list) / len(away_ovr_list))

    except:
        team_name_away = "MFL Team"
        away_ovr = randint(65, 72)

    ### Home team stats
    team_name_home = t_info.split(",")[0]
    team_form_home = t_info.split(",")[3]

    teamsname = Teams(team_name_home, team_name_away)
    home_man = playershome[0]
    home_ovr_list = []

    for x in playershome:
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
    goal_scorers = []
    curevent = "\u200b"

    commentary = "The match begins !"

    def get_actions(team):
        ## Define scoring probabilities
        what = randint(1, 20)

        shootprob = [0,4,11,18,22,29,36,46,61,76,100]

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
                if number < x:
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

        return who, what, team, success

    def register_goals(player, team):
        print(event)
        # Update f_goals
        if event == "no":
            pfile = open(f_goals, "r+")
        else:
            pfile = open("goals_" + event + ".csv", "r+")

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

    #### Start of the simulation ###############

    matchevent = MatchEvent(teamsname, score, curevent, commentary, i, note)
    eventlist.append(matchevent)

    while i < minutes:

        ## Recheck team value (can change during game)
        home_ovr_list = []
        curevent = "\u200b"

        for x in playershome:
            if x.pos != "COACH":
                home_ovr_list.append(x.ovr)

        home_ovr = round(sum(home_ovr_list) / len(home_ovr_list))

        away_ovr_list = []
        for x in playersaway:
            if x.pos != "COACH":
                away_ovr_list.append(x.ovr)

        away_ovr = round(sum(away_ovr_list) / len(away_ovr_list))

        home_bonus = round(home_ovr - away_ovr)

        ## Give a balance between the 2 teams (if same OVR : 1-50 and 51-100 to find who makes the action)
        ratio = round(50 + 2 * home_bonus)

        i += 1
        x = randint(1, minutes)

        ### Déclenchement actions
        if x < nb_actions:
            who_attack = randint(1, 100)
            if who_attack > ratio:
                who, what, team, success = get_actions("away")
            else:
                who, what, team, success = get_actions("home")

            if who.isRedCard != True:

                whoplay = who.displayName

                if what == "Shoot":

                    commentary = whoplay + " is in a good position and shoot..."
                    matchevent = MatchEvent(teamsname, score, curevent, commentary, i, note)
                    eventlist.append(matchevent)

                    if success == 1:

                        if team == "home":
                            register_goals(whoplay, teamsname.home)
                            score_home += 1
                            score = Score(score_home, score_away)
                            curevent = Event("goal", whoplay, teamsname.home, i)
                            commentary = "What a goal for " + teamsname.home + " by **" + whoplay + "**"
                        else:
                            register_goals(whoplay, teamsname.away)
                            score_away += 1
                            score = Score(score_home, score_away)
                            curevent = Event("goal", whoplay, teamsname.away, i)
                            commentary = "What a goal for " + teamsname.away + " by **" + whoplay + "**"
                    else:
                        who.ovr = who.ovr + 2
                        if team == "home":
                            commentary = "Beautiful action for " + team_name_home + " but " + whoplay + " missed the shoot"
                        else:
                            commentary = "Beautiful action for " + team_name_away + " but " + whoplay + " missed the shoot"

                elif what == "Fault":
                    commentary = "What a dangerous tacle from " + teamsname.home + " by **" + whoplay + "**"

                    if success == 0:
                        who.ovr = who.ovr - 3
                        if team == "home":
                            commentary = team_name_home + " : No card for " + whoplay
                        else:
                            commentary = team_name_away + " : No card for " + whoplay

                    if success == 1:
                        if who.isYellowCard == False:
                            who.ovr = who.ovr - 10
                            who.isYellowCard = True
                            if team == "home":
                                curevent = Event("yelcard", whoplay, teamsname.home, i)
                                commentary = team_name_home + " : It's a yellow card for " + whoplay
                            else:
                                curevent = Event("yelcard", whoplay, teamsname.away, i)
                                commentary = team_name_away + " : It's a yellow card for " + whoplay
                        else:
                            success = 2
                    if success == 2:
                        print(who.displayName+" RC")
                        who.ovr = 0
                        who.isRedCard = True
                        if team == "home":
                            score_home += 1
                            curevent = Event("redcard", whoplay, teamsname.home, i)
                            commentary = "What a goal for " + teamsname.home + " by **" + whoplay + "**"
                        else:
                            score_away += 1
                            curevent = Event("redcard", whoplay, teamsname.away, i)
                            commentary = "What a goal for " + teamsname.away + " by **" + whoplay + "**"

                elif what == "Bonus":
                    if team == "home":
                        commentary = teamsname.home + " is dominant"
                    else:
                        commentary = teamsname.away + " is dominant"

                else:
                    commentary = "---"

        else:
            commentary = "---"

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

    ### Commentary review

    if score_home > score_away:
        comment = random.choice(commentaries['win'])
        comment = comment.replace("TEAM1", team_name_home)
        comment = comment.replace("TEAM2", team_name_away)
        commentary = comment
    elif score_home < score_away:
        comment = random.choice(commentaries['win'])
        comment = comment.replace("TEAM1", team_name_away)
        comment = comment.replace("TEAM2", team_name_home)
        commentary = comment

    else:
        commentary = "What a game !\n But " + team_name_home + " and " + team_name_away + " " + "could not make the difference"

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

    description_start = "Welcome to the match !\nToday, " + home_name + " will face " + away_name + ".\n\nThe teams enter the " \
                                                                                                    "field... let's go! "
    description_default = "Welcome to the match !\nToday, " + home_name + " will face " + away_name + ".\n"

    note = int(eventlist[0].note)
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

    nogoal = "\u200b"
    hgoal = nogoal
    agoal = nogoal
    hcard = nogoal
    acard = nogoal


    for x in eventlist:

        minutes = x.minutes
        if int(minutes) == 1:
            description = description_start
        elif x == eventlist[len(eventlist) - 1]:
            description = "The referee whistles the end of the game !"
        else:
            description = description_default

        home_score = x.score.home
        away_score = x.score.away
        embedscore = discord.Embed(
            title='Match Day', color=default_color, description=description)
        embedscore.add_field(name="MIN", value=str(minutes) + "'", inline=True)
        embedscore.add_field(name=home_name, value=str(home_score), inline=True)
        embedscore.add_field(name=away_name, value=str(away_score), inline=True)
        embedscore.add_field(name="\u200b", value="**Goals**", inline=True)

        goals = x.event
        #agoals = away_scorers[int(minutes)].split(',')

        if type(goals) != str:
            if goals.kind == "goal":
                if goals.team == home_name:
                    hgoal += goals.player + " " +str(goals.minute) + "'\n"
                elif goals.team == away_name:
                    agoal += goals.player + " " +str(goals.minute) + "'\n"
            elif goals.kind == "yelcard":
                if goals.team == home_name:
                    hcard += "🟨 "+goals.player + " " +str(goals.minute) + "'\n"
                elif goals.team == away_name:
                    acard += "🟨 "+goals.player + " " +str(goals.minute) + "'\n"
            elif goals.kind == "redcard":
                if goals.team == home_name:
                    hcard += "🟥 "+ goals.player + " " +str(goals.minute) + "'\n"
                elif goals.team == away_name:
                    acard += "🟥 "+ goals.player + " " +str(goals.minute) + "'\n"

        embedscore.add_field(name="\u200b", value=hgoal, inline=True)
        embedscore.add_field(name="\u200b", value=agoal, inline=True)
        embedscore.add_field(name="\u200b", value="**Events**", inline=True)
        embedscore.add_field(name="\u200b", value=hcard, inline=True)
        embedscore.add_field(name="\u200b", value=acard, inline=True)
        embedscore.add_field(name="Commentary", value=x.commentary, inline=False)
        embedscore.add_field(name="Match Note", value=note, inline=False)

        embedlist.append(embedscore)
    return embedlist