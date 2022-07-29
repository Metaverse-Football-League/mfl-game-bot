import requests
from config import config
import utils_nations
import players_models

players_file = config["dataPath"] + "selections/all_players.csv"

"""
for n in nations.keys():

    host = config["apiUrl"] + "/players/nations/tops?nbPerPosition=5&nations=%5B%22"+str(n)+"%22%5D"
    print(host)
    headers = {
        'x-api-key': config["apiKey"]
    }
    getnft = requests.get(host, headers=headers)
    nfts = getnft.json()

    list = nfts[n]
    with open(players_file, "a") as tfile:
        for p in players_positions_indices.keys():
            plist = nfts[n][p]
            for x in plist:
                displayName = x['metadata']['firstName']+" "+x['metadata']['lastName']
                ovr = x['metadata']['overall']
                pos = p
                nat = n
                nft = "Yes"
                if ovr >= 85:
                    rarity = "legend"
                elif ovr >= 75:
                    rarity = "rare"
                elif ovr >= 65:
                    rarity = "uncommon"
                else:
                    rarity = "common"
                tfile.write(displayName + "," + str(ovr) + "," + pos + "," + nat + "," + nations[
                    nat] + "," + "Yes" + "," + rarity + ",\n")

### Generate file per country
for x in nations.keys():
    players_number = []
    i = 0
    filepath = "selections/team_"+x
    with open(filepath, "a") as tfile:
        for line in open(players_file).readlines():
            if i < 42:
                nation = line.split(',')[3]
                pos = line.split(',')[2]
                ovr = line.split(',')[1]

                displayName = line.split(',')[0]
                try:
                    number = players_positions_indices[pos]
                except:
                    continue
                rarity = line.split(',')[6]
                teamid = x

                if nation == x:
                    if (number == 3) or (number == 6):
                        ratio = 4
                    else:
                        ratio = 3
                    if players_number.count(number) < ratio:
                        players_number.append(number)
                        i += 1
                        tfile.write(displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[x] + "," + "Yes" + "," + rarity + ",\n")

"""


### Create starter 11 for each team
for x in utils_nations.nations_codes.keys():
    players_number = ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No"]
    i = 0
    filepath = config["dataPath"] + "selections/active_team_"+x
    with open(filepath, "a") as tfile:
        for line in reversed(open(players_file).readlines()):
            if i < 11:
                nation = line.split(',')[3]
                pos = line.split(',')[2]
                ovr = line.split(',')[1]

                displayName = line.split(',')[0]
                try:
                    number = players_models.players_positions_indices[pos]
                except:
                    continue
                rarity = line.split(',')[6]
                teamid = x
                if number > 11:
                    continue

                if nation == x:
                    number = number - 1
                    if (number == 3) or (number == 6):
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + utils_nations.nations_codes[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number - 1] = description
                        elif players_number[number] == "No":
                            print("Find : " + displayName + " " + pos + " : " + str(number))
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + utils_nations.nations_codes[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number] = description

                    else:
                        if players_number[number] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + utils_nations.nations_codes[x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number] = description

        for x in players_number:
            tfile.write(x)




"""
### Create best XI for each country
for x in utils_nations.nations_codes.keys():
    players_number = ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No"]
    i = 0
    filepath = "selections/best_team_"+x
    with open(filepath, "a") as tfile:
        for line in reversed(open("all_players.csv").readlines()):
            if i < 11:
                nation = line.split(',')[3]
                pos = line.split(',')[2]
                ovr = line.split(',')[1]
                displayName = line.split(',')[0]
                number = players_positions_indices[pos]
                rarity = line.split(',')[6]
                teamid = x

                if nation == x:
                    if (number == 3) or (number == 6):
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + utils_nations.nations_codes[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number - 1] = description
                        elif players_number[number] == "No":
                            print("Find : " + displayName + " " + pos + " : " + str(number))
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + utils_nations.nations_codes[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number] = description

                    else:
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + utils_nations.nations_codes[x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number-1] = description

        for x in players_number:
            tfile.write(x)


"""
