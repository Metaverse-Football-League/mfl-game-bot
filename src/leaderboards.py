import discord
import events
from config import config
import utils_file

f_goals = config["dataPath"] + "goals.csv"
f_points = config["dataPath"] + "points.csv"

async def get(leaderboard_name):
    leaderboard_aggregate = "byPlayer"
    reward = 0

    f_data_path = f_goals

    if "event_" in leaderboard_name:
        event = await events.get_by_code(leaderboard_name)
        leaderboard_aggregate = event[0].leaderboard
        reward = event[0].reward
        f_data_path = config["dataPath"] + "goals_" + leaderboard_name + ".csv"

    if leaderboard_name == "points":
        f_data_path = f_points
        leaderboard_aggregate = "byTeam"

    leaderboard_lines = await utils_file.read_csv_file(None, f_data_path)
    leaderboard_lines.sort(reverse=True, key=lambda line: int(line[0]))

    line_number = 1
    embed_score = ""
    nb_goal = 0
    for line in leaderboard_lines:
        score = line[0]
        if int(reward) > 0:
            nb_goal += int(line_number)
        if line_number <= 10:
            team = line[1]
            if leaderboard_aggregate == "byPlayer":
                name = line[2]
                embed_score += "**" + str(score) + "**: " + name + " (*" + team + "*)\n"
            else:
                embed_score += team + " - **" + str(line_number) + "pts**\n"
            line_number += 1

    if embed_score == "":
        embed_score = "\u200b"

    default_color = 0x00ff00

    if "event_" in leaderboard_name:
        name = leaderboard_name.split("_")[1].upper()
        embed_lead = discord.Embed(
            title="Leaderboards", description="Top 10 for **"+name+"** event", color=default_color)
    else:
        embed_lead = discord.Embed(
            title="Leaderboards", description="Top 10", color=default_color)

    embed_lead.add_field(name="Ranking", value=embed_score)
    if int(reward) > 0:
        embed_lead.add_field(name="Road to "+str(reward)+" goals !", value=str(nb_goal)+"/"+str(reward), inline=False)

    return embed_lead
