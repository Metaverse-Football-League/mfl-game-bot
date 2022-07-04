players_file = "all_players.csv"

nations = {
    'ALGERIA': 'dz',
    'ARGENTINA': 'ar',
    'AUSTRALIA': 'au',
    'AUSTRIA': 'at',
    'BELGIUM': 'be',
    'BRAZIL': 'br',
    'CANADA': 'ca',
    'CAMEROON': 'cm',
    'CHILE': 'cl',
    'COLOMBIA': 'co',
    'COSTA_RICA': 'cr',
    'CROATIA': 'hr',
    'CZECH_REPUBLIC': 'cz',
    'DENMARK': 'dk',
    'ECUADOR': 'ec',
    'ENGLAND': 'gb',
    'EGYPT': 'eg',
    'FRANCE': 'fr',
    'GERMANY': 'de',
    'HUNGARY': 'hu',
    'KOREA_REPUBLIC': 'kr',
    'ITALY': 'it',
    'IRAN': 'ir',
    'JAPAN': 'jp',
    'MEXICO': 'mx',
    'MOROCCO': 'ma',
    'NETHERLANDS': 'nl',
    'NIGERIA': 'ng',
    'NORWAY': 'no',
    'PARAGUAY': 'py',
    'PERU': 'pe',
    'POLAND': 'pl',
    'PORTUGAL': 'pt',
    'UKRAINE': 'ua',
    'REPUBLIC_OF_IRELAND': 'ie',
    'ROMANIA': 'ro',
    'RUSSIA': 'ru',
    'SAUDI_ARABIA': 'sa',
    'SCOTLAND': 'gb',
    'SENEGAL': 'sn',
    'SERBIA': 'rs',
    'SLOVAKIA': 'sk',
    'SPAIN': 'es',
    'SWITZERLAND': 'ch',
    'SWEDEN': 'se',
    'TUNISIA': 'tn',
    'TURKEY': 'tr',
    'UNITED_STATES': 'us',
    'URUGUAY': 'uy',
    'WALES': 'gb'
}

positions = {
    'GK': 1,
    'LB': 2,
    'LWB': 2,
    'CB': 3,
    'RB': 5,
    'RWB': 5,
    'CDM': 6,
    'CM': 6,
    'CAM': 8,
    'AM': 8,
    'LW': 9,
    'LM': 9,
    'RW': 10,
    'RM': 10,
    'CF': 11,
    'ST': 11,
    'FW': 11
}

### Create best XI for each country
for x in nations.keys():
    players_number = ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No"]
    i = 0
    filepath = "selections/best_team_"+x
    with open(filepath, "a") as tfile:
        for line in reversed(open("all_players.csv").readlines()):
            if i < 11:
                if '"' in line.split(',')[2]:
                    nation = line.split('"')[2].split(',')[2]
                    pos = line.split('"')[1].split(',')[0]
                    ovr = line.split('"')[2].split(',')[3]
                else:
                    nation = line.split(',')[4]
                    pos = line.split(',')[2]
                    ovr = line.split(',')[5]

                displayName = line.split(',')[0]
                try:
                    number = positions[pos]
                except:
                    continue
                rarity = line.split(',')[1]
                teamid = x

                if nation == x:
                    if (number == 3) or (number == 6):
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number - 1] = description
                        elif players_number[number] == "No":
                            print("Find : " + displayName + " " + pos + " : " + str(number))
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number] = description

                    else:
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number-1] = description

        for x in players_number:
            tfile.write(x)



"""
for x in nations.keys():
    players_number = ["No", "No", "No", "No", "No", "No", "No", "No", "No", "No", "No"]
    i = 0
    filepath = "selections/active_team_"+x
    with open(filepath, "a") as tfile:
        for line in open("all_players.csv").readlines():
            if i < 11:
                if '"' in line.split(',')[2]:
                    nation = line.split('"')[2].split(',')[2]
                    pos = line.split('"')[1].split(',')[0]
                    ovr = line.split('"')[2].split(',')[3]
                else:
                    nation = line.split(',')[4]
                    pos = line.split(',')[2]
                    ovr = line.split(',')[5]

                displayName = line.split(',')[0]
                try:
                    number = positions[pos]
                except:
                    continue
                rarity = line.split(',')[1]
                teamid = x

                if nation == x:
                    if (number == 3) or (number == 6):
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number - 1] = description
                        elif players_number[number] == "No":
                            print("Find : " + displayName + " " + pos + " : " + str(number))
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[
                                x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number] = description

                    else:
                        if players_number[number - 1] == "No":
                            i += 1
                            description = displayName + "," + str(ovr) + "," + pos + "," + str(teamid) + "," + nations[x] + "," + "Yes" + "," + rarity + ",0,\n"
                            players_number[number-1] = description

        for x in players_number:
            tfile.write(x)




for x in nations.keys():
    players_number = []
    i = 0
    filepath = "selections/team_"+x
    with open(filepath, "a") as tfile:
        for line in reversed(open("all_players.csv").readlines()):
            if i < 33:
                if '"' in line.split(',')[2]:

                    nation = line.split('"')[2].split(',')[2]
                    pos = line.split('"')[1].split(',')[0]
                    ovr = line.split('"')[2].split(',')[3]
                else:
                    nation = line.split(',')[4]
                    pos = line.split(',')[2]
                    ovr = line.split(',')[5]

                displayName = line.split(',')[0]
                try:
                    number = positions[pos]
                except:
                    continue
                rarity = line.split(',')[1]
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