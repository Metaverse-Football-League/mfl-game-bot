import discord
import names
from random import randint, choice

f_players = "players.csv"


class Player:
    def __init__(self, displayName, ovr, pos, teamid, form, number, isYellowCard, isRedCard):
        self.displayName = displayName
        self.form = form
        self.number = number
        self.pos = pos
        self.ovr = ovr
        self.teamid = teamid
        self.isYellowCard = isYellowCard
        self.isRedCard = isRedCard



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
            pfile.write(displayName + "," + str(ovr) + "," + position + "," + str(
                owner) + "," + nat + "," + nft + "," + rarity + ",\n")
            i += 1


async def get(id):
    with open(f_players, "r+") as pfile:
        playerfile = pfile.readlines()
        playerlist = []
        for line in playerfile:
            if id in line:
                playerlist.append(line)
        return playerlist


async def get2(id):
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
                isYellowCard = False
                isRedCard = False
                form = 3
                myplayer = Player(displayName, ovr, pos, teamid, form, i, isYellowCard, isRedCard)
                print(type(myplayer))
                i += 1
                playerlist.append(myplayer)
        return playerlist


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
    embeddescription = ":flag_" + nat + ":`" + str(
        i) + " - " + pos + " " + ovr + "` " + rarity_flag + " *" + name + "*\n"
    oldplayer = ":flag_" + old_nat + ":`" + str(i) + " - " + old_pos + " " + old_ovr + "` ~~" + old_name + "~~\n"

    embedplayer.add_field(name="New player", value=embeddescription)
    embedplayer.add_field(name="Player you will remove", value=oldplayer, inline=False)

    return embedplayer


async def recruit(id, num, name, ovr, pos, nat):
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
