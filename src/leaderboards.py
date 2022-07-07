import discord
import events
from config import config

async def get(i):
    f_goals = config["dataPath"] + "goals.csv"
    leaderboard = "byPlayer"
    reward = 0
    nbgoal = 0

    if "event_" in i:
        event = await events.getbyCode(i)
        leaderboard = event[0].leaderboard
        reward = event[0].reward
        f_goals = config["dataPath"] + "goals_" + i + ".csv"
        print(f_goals)

    with open(f_goals, "r") as tgoals:
        goalfile = tgoals.readlines()
        goalfile.sort(reverse=True, key=lambda x: int(x.split(",")[0]))
        embedscore = ""
        indice = 1

        for line in goalfile:
            number = line.split(",")[0]
            if int(reward) > 0:
                nbgoal += int(number)
            if indice <= 10:
                number = line.split(",")[0]
                team = line.split(",")[1]
                if leaderboard == "byPlayer":
                    name = line.split(",")[2]
                    embedscore = embedscore + "**"+ str(number) + "** : " + name + " (*" + team + "*)\n"
                else:
                    embedscore = embedscore + "**"+ str(number) + "** : "+team+"\n"
                indice += 1

        if embedscore == "":
            embedscore = "\u200b"

        default_color = 0x00ff00

        if "event_" in i:
            name = i.split("_")[1].upper()
            embedlead = discord.Embed(
                title="Leaderboards", description="Best players for the **"+name+"** event", color=default_color)
        else:
            embedlead = discord.Embed(
                title="Leaderboards", description="Best players", color=default_color)

        if leaderboard == "byPlayer":
            embedlead.add_field(name="Goals : Player (Team)", value=embedscore)
        else:
            embedlead.add_field(name="Goals : Team", value=embedscore)
        if int(reward) > 0:
            embedlead.add_field(name="Road to "+str(reward)+" goals !", value=str(nbgoal)+"/"+str(reward), inline=False)

        return embedlead
