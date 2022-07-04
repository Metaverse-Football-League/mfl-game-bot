import discord

f_nations = "nations.csv"
teams_selections = "selections/team_"
active_teams = "selections/active_team_"

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
    team = team.upper()
    filepath = active_teams+team
    prefix = nations[team]

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
            nat = line.split(",")[3]
            rarity = line.split(",")[5].lower()
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
