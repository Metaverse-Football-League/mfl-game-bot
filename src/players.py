import discord
import names
from random import randint, choice
from config import config
import players_models

f_players = config["dataPath"] + "players.csv"

async def create(id, manager):
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
        pfile.write(
            manager + "," + str(m_ovr) + "," + m_pos + "," + str(m_owner) + "," + nat + "," + nft + "," + rarity + "\n")

        while i <= 11:
            # To create better bot teams than players teams
            if int(id) < 1000000:
                ovr = randint(65, 82)
            else:
                # Value for players generate by Discord User creation team (Issue #2)
                ovr = randint(25, 30)

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
                position = "cdm"
            elif i == 7:
                position = "cm"
            elif i == 8:
                position = "cm"
            elif i == 9:
                position = "lw"
            elif i == 10:
                position = "rw"
            elif i == 11:
                position = "st"
            owner = id
            pfile.write(displayName + "," + str(ovr) + "," + position + "," + str(
                owner) + "," + nat + "," + nft + "," + rarity + ",\n")
            i += 1

async def get(id):
    with open(f_players, "r+") as pfile:
        playerfile = pfile.readlines()
        playerlist = []
        i = 0
        for line in playerfile:
            if id in line:
                displayName = line.split(",")[0]
                ovr = line.split(",")[1]
                pos = line.split(",")[2]
                teamid = line.split(",")[3]
                nat = line.split(",")[4]
                rarity = line.split(",")[6]
                isYellowCard = False
                isRedCard = False
                form = 3
                myplayer = players_models.Player(displayName, ovr, pos, teamid, nat, rarity, form, i, isYellowCard, isRedCard)
                i += 1
                playerlist.append(myplayer)
        return playerlist

async def get_nation(nation):
    with open(config["dataPath"] + "selections/active_team_"+nation.upper(), "r+") as pfile:
        playerfile = pfile.readlines()
        playerlist = []
        i = 0
        for line in playerfile:
            displayName = line.split(",")[0]
            ovr = line.split(",")[1]
            pos = line.split(",")[2]
            teamid = line.split(",")[3]
            nat = line.split(",")[4]
            rarity = line.split(",")[6]
            isYellowCard = False
            isRedCard = False
            form = 3
            myplayer = players_models.Player(displayName, ovr, pos, teamid, nat, rarity, form, i, isYellowCard, isRedCard)
            i += 1
            playerlist.append(myplayer)
        return playerlist

async def check(id, name):
    with open(f_players, "r+") as pfile:
        playerfile = pfile.readlines()
        i = 0
        alreadyinTeam = False
        for line in playerfile:
            if alreadyinTeam == True:
                continue
            if id in line:
                displayName = line.split(",")[0]
                if displayName == name:
                    alreadyinTeam = True

        return alreadyinTeam

async def generate(i):
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
        position = "dm"
    elif i == 7:
        position = "cm"
    elif i == 8:
        position = "cm"
    elif i == 9:
        position = "lw"
    elif i == 10:
        position = "rw"
    elif i == 11:
        position = "st"

    owner = id
    nft = "0"
    rarity = "no"
    new_line = displayName + "," + str(ovr) + "," + position + "," + str(
        owner) + "," + nat + "," + nft + "," + rarity + ",\n"
    return new_line


async def scout(id):
    user_id = str(id)
    p_info = await get(user_id)

    number = randint(1, 11)
    newp_info = await generate(number)
    name = newp_info.split(",")[0]
    ovr = newp_info.split(",")[1]
    pos = newp_info.split(",")[2].upper()
    nat = newp_info.split(",")[4]
    rarity = "no"
    rarity_flag = "⚫"
    nft = "0"

    ## Case of similar posts

    if number in (3, 4):
        ovr3 = p_info[3].ovr
        ovr4 = p_info[4].ovr
        if ovr3 < ovr4:
            old_name = p_info[3].displayName
            old_ovr = p_info[3].ovr
            old_pos = p_info[3].pos.upper()
            old_nat = p_info[3].nat
            number = 3
        else:
            old_name = p_info[4].displayName
            old_ovr = p_info[4].ovr
            old_pos = p_info[4].pos.upper()
            old_nat = p_info[4].nat
            number = 4
    elif number in (7, 8):
        ovr6 = p_info[7].ovr
        ovr7 = p_info[8].ovr
        if ovr6 < ovr7:
            old_name = p_info[7].displayName
            old_ovr = p_info[7].ovr
            old_pos = p_info[7].pos.upper()
            old_nat = p_info[7].nat
            number = 7
        else:
            old_name = p_info[8].displayName
            old_ovr = p_info[8].ovr
            old_pos = p_info[8].pos.upper()
            old_nat = p_info[8].nat
            number = 8
    else:
        old_name = p_info[number].displayName
        old_ovr = p_info[number].ovr
        old_pos = p_info[number].pos.upper()
        old_nat = p_info[number].nat

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
    embeddescription = ":flag_" + nat + ":`" + str(
        i) + " - " + pos + " " + ovr + "` " + rarity_flag + " *" + name + "*\n"
    oldplayer = ":flag_" + old_nat + ":`" + str(i) + " - " + old_pos + " " + str(old_ovr) + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer


async def recruit(id, num, name, ovr, pos, nat):
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
