from random import sample
import discord
import players.service
from config import config

## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = config["dataPath"] + "teams.csv"

# Find team by id (team id == user id)
async def get_by_id(team_id):
    with open(f_teams, "r") as tfile:
        team_file = tfile.readlines()
        for line in team_file:
            try:
                if team_id == str(line.split(",")[1]):
                    return line
            except:
                continue

async def getAll(id):
    user_id = str(id)
    t_info = await get_by_id(user_id)

    if t_info is None or t_info == "Error":
        return "You have no team!"
    else:
        p_info = await players.service.get(user_id)
        team_name = t_info.split(",")[0]

        i = 0
        default_color = 0x00ff00

        embedteam = discord.Embed(
            title=team_name, description="Below your squad", color=default_color)

        embeddescription = ""

        while i <= 11:
            if i == 0:
                i += 1

            name = p_info[i].displayName
            ovr = p_info[i].ovr
            pos = p_info[i].pos.upper()
            nat = p_info[i].nat
            rarity = p_info[i].rarity
            rarity_flag = "⚫"

            if rarity == "common":
                rarity_flag = "⚪"
            elif rarity == "uncommon":
                rarity_flag = "🟢"
            elif rarity == "rare":
                rarity_flag = "🔵"
            elif rarity == "legend":
                rarity_flag = "🟣"

            if len(pos) == 3:
                embeddescription = embeddescription + ":flag_" + nat + ":`" + pos + " " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            else:
                embeddescription = embeddescription + ":flag_" + nat + ":`" + pos + "  " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            i += 1

        man_name = p_info[0].displayName
        embedmanager = "*" + man_name + "*"
        embedteam.add_field(name="Players", value=embeddescription)
        embedteam.add_field(name="Coach", value=embedmanager, inline=False)

        return embedteam

async def get_by_ida(id):
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
                    else:
                        username = str(teamfile[x].split(",")[4])
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


async def create(team_name, team_id, real_user, nation, coach_name):
    with open(f_teams, "r+") as tfile:
        tfile.write(team_name + "," + team_id + "," + real_user + "," + nation + "," + coach_name + "\n")
        await players.service.create_starting_eleven(team_id, coach_name)
