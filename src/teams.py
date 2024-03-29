from random import sample
import discord
import players
from config import config

## Teams
# Name, user_id, boolean(0 : bot, 1 : player, form)
f_teams = config["dataPath"] + "teams.csv"

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

async def getAll(id):
    user_id = str(id)
    t_info = await get(user_id)
    default_color = 0xffff00

    if t_info is None:
        return discord.Embed(title="No team found!", description="", color=default_color)
    elif t_info == "Error":
        return discord.Embed(title="Error", description="An error occurred during the request to get the teams.", color=default_color)
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

            name = p_info[i].displayName
            ovr = p_info[i].ovr
            pos = p_info[i].pos.upper()
            nat = p_info[i].nat
            #nft = p_info[i].split(",")[5]
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


async def getBest(id1, id2):
    user1_id = str(id1)
    user2_id = str(id2)

    default_color = 0x00ffff

    embedteam = discord.Embed(
        title="Before match", description="Let's focus on the best players for each team !", color=default_color)

    async def checkPlayers(id):
        team = await get(id)
        if team is None:
            return discord.Embed(title="No team found!", description="", color=default_color)
        elif team == "Error":
            return discord.Embed(title="Error", description="An error occurred during the request to get the teams.", color=default_color)
        else:
            p_info = await players.get(id)
            team_name = team.split(",")[0]

            i = 0

            def sortbyOVR(player):
                return player.ovr

            man_name = p_info[0].displayName
            p_info.sort(key=sortbyOVR, reverse=True)

            embeddescription = ""

            top = 3

            while i < top:

                name = p_info[i].displayName
                ovr = p_info[i].ovr
                pos = p_info[i].pos.upper()

                if pos == "COACH":
                    i += 1
                    top = top + 1
                    continue

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

            embedteam.add_field(name=team_name, value=embeddescription)

    await checkPlayers(user1_id)
    await checkPlayers(user2_id)

    return embedteam



async def find(id):
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
        #embedteam.add_field(name="Opponents", value=embedopponents)

        return embedteam, teamlist

async def rename(id, username, name):
    print("called")
    # Find team which owned by called player
    with open(f_teams, "r+") as tfile:
        teamfile = tfile.readlines()
        status = 0
        teams = []

        if len(teamfile) > 0:
            new_line = str(name)+","+str(id)+",yes,3,"+str(username)+",\n"
            for line in teamfile:
                uids = line.split(",")[1]
                if uids == id:
                    replace = line.replace(line, new_line)
                    line = replace
                    if "," not in line:
                        line = ",,,,\n"
                        status = 1

                teams.append(line)
        if status == 1:
            tfile.write(new_line)
        else:
            tfile.seek(0)
            tfile.truncate(0)
            tfile.writelines(teams)

        tfile.close()