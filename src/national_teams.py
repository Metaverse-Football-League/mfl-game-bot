import discord
from config import config
import utils.nations
import players.models

f_nations = config["dataPath"] + "nations.csv"
teams_selections = config["dataPath"] + "selections/team_"
active_teams = config["dataPath"] + "selections/active_team_"

class NationalTeam:
    def __init__(self, displayName, prefix, manager):
        self.displayName = displayName
        self.prefix = prefix
        self.manager = manager

async def check(id):
    myNationTeam = None
    with open(f_nations, "r+") as file:
        lines = file.readlines()

        for line in lines:
            if id in line:
                displayName = line.split(",")[0]
                prefix = line.split(",")[3]
                manager = line.split(",")[2]
                myNationTeam = NationalTeam(displayName, prefix, manager)

    return myNationTeam

async def get(team):
    team = team.upper()

    # Find team which owned by called player
    with open(f_nations, "r") as tfile:
        teamfile = tfile.readlines()

        for line in teamfile:
            try:
                if team == str(line.split(",")[0]):
                    return line
            except:
                continue

async def getAll(team):

    if len(team) == 2:
        for nation, prefix in utils.nations.nations_codes.items():
            if prefix == team:
                team = nation

    team = team.upper()
    filepath = active_teams+team
    prefix = utils.nations.nations_codes[team]

    i = 0
    default_color = 0x00ff00

    embedteam = discord.Embed(
        title="National Team", description="You are currently the manager of :flag_"+prefix+": "+team, color=default_color)

    embeddescription = ""

    with open(filepath, "r+") as pfile:
        datas = pfile.readlines()

        for line in datas:
            name = line.split(",")[0]
            ovr = line.split(",")[1]
            pos = line.split(",")[2]
            rarity = line.split(",")[6].lower()
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
                embeddescription = embeddescription + ":flag_" + prefix + ":`" + pos + " " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            else:
                embeddescription = embeddescription + ":flag_" + prefix + ":`" + pos + "  " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            i += 1

    embedteam.add_field(name="Players", value=embeddescription)

    return embedteam

async def getList(team):
    team = team.upper()
    filepath = teams_selections+team
    prefix = utils.nations.nations_codes[team]
    playerslist = []
    formatlist = []

    i = 0
    default_color = 0x00ff00

    embeddescription = ""

    with open(filepath, "r+") as pfile:
        datas = pfile.readlines()

        for line in datas:
            name = line.split(",")[0]
            ovr = line.split(",")[1]
            pos = line.split(",")[2]
            nat = line.split(",")[3]
            rarity = line.split(",")[6].lower()
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
                embeddescription = embeddescription + ":flag_" + prefix + ":`" + pos + " " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            else:
                embeddescription = embeddescription + ":flag_" + prefix + ":`" + pos + "  " + str(ovr) + "`" + rarity_flag + " *" + name + "*\n"
            i += 1
            playerslist.append(line)

            if (i % 5 == 0) or (i == len(datas)):
                formatlist.append(playerslist)
                playerslist = []

    return formatlist

async def alreadyinTeam(team, name):
    filepath = active_teams + team
    with open(filepath, "r+") as pfile:
        playerfile = pfile.readlines()
        i = 0
        alreadyinTeam = False
        for line in playerfile:
            if alreadyinTeam == True:
                continue
            else:
                displayName = line.split(",")[0]
                if displayName == name:
                    alreadyinTeam = True

        return alreadyinTeam


async def search(team, name, ovr, pos, nat, rarity):
    team = team
    name = name
    ovr = int(ovr)
    pos = pos
    number = players.models.players_positions_placements[pos]
    print(number)
    nat = nat
    nft = "1"
    rarity = rarity

    filepath = active_teams+team
    with open(filepath, "r+") as pfile:
        playerlist = pfile.readlines()

    p_info = []
    i = 0
    for line in playerlist:
        old_displayName = line.split(",")[0]
        old_ovr = line.split(",")[1]
        old_pos = line.split(",")[2]
        old_teamid = line.split(",")[3]
        old_nat = line.split(",")[4]
        old_rarity = line.split(",")[6]
        isYellowCard = False
        isRedCard = False
        form = 3
        myplayer = players.models.Player(old_displayName, old_ovr, old_pos, old_teamid, old_nat, old_rarity, form, i, isYellowCard, isRedCard)
        i += 1
        p_info.append(myplayer)

    if rarity == "common":
        rarity_flag = "⚪"
    elif rarity == "uncommon":
        rarity_flag = "🟢"
    elif rarity == "rare":
        rarity_flag = "🔵"
    elif rarity == "legend":
        rarity_flag = "🟣"

    old_number = number - 1
    if number in (3, 4):
        ovr3 = p_info[2].ovr
        ovr4 = p_info[3].ovr
        if ovr3 < ovr4:
            old_name = p_info[2].displayName
            old_ovr = p_info[2].ovr
            old_pos = p_info[2].pos.upper()
            old_nat = p_info[2].nat
            number = 3
        else:
            old_name = p_info[3].displayName
            old_ovr = p_info[3].ovr
            old_pos = p_info[3].pos.upper()
            old_nat = p_info[3].nat
            number = 4
    elif number in (7, 8):
        ovr6 = p_info[6].ovr
        ovr7 = p_info[7].ovr
        if ovr6 < ovr7:
            old_name = p_info[6].displayName
            old_ovr = p_info[6].ovr
            old_pos = p_info[6].pos.upper()
            old_nat = p_info[6].nat
            number = 7
        else:
            old_name = p_info[7].displayName
            old_ovr = p_info[7].ovr
            old_pos = p_info[7].pos.upper()
            old_nat = p_info[7].nat
            number = 7
    else:
        old_name = p_info[old_number].displayName
        old_ovr = p_info[old_number].ovr
        old_pos = p_info[old_number].pos.upper()
        old_nat = p_info[old_number].nat

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
        title=name, description="You find a new player!", color=default_color)
    embeddescription = ":flag_" + nat + ":`" + str(i) + " - " + pos + " " + str(ovr) + "` " + rarity_flag + " *" + name + "*\n"
    oldplayer = ":flag_" + old_nat + ":`" + str(i) + " - " + old_pos + " " + str(old_ovr) + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer

async def replace(num, name, ovr, pos, nat):
    nat = nat
    for nation, prefix in utils.nations.nations_codes.items():
        if prefix == nat:
            team = nation

    nft = "1"
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

    filepath = active_teams+team
    pfile = open(filepath, "r+")

    c = 0
    playerfile = pfile.readlines()
    playerlist = []
    i = int(num)
    for line in playerfile:
        try:
            c += 1
            if c == i:
                displayName = name
                ovr = ovr
                position = pos
                owner = team.upper()
                new_line = displayName + "," + str(ovr) + "," + position + "," + str(
                        owner) + "," + nat + "," + nft + "," + rarity + ",\n"
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
