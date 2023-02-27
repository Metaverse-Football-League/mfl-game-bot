import asyncio
import datetime

import requests
from config import config

f_quests = config["dataPath"] + "quests.csv"
community = config["crew3_community"]
url = "https://api.crew3.xyz/communities/"+community+"/"
apiKey = config["crew3_api"]
quests = config["crew3_quests"].split(",")

headers = {
    'x-api-key': apiKey
}

###### Quests CSV Variables ######
# 0 : discordId
# 1 : nb match played today
# 2 : nb goals scored today
# 3 : nb victory today
# 4 : nb match all time
# 5 : nb score all time
# 6 : nb victory all time
# 7 : victory vs PVE daily

###### Known Quests ####
# 4215cec3-dfb2-4bde-b92a-2a44ca5679f5 : play one game / daily
# bc879911-c61c-4eba-a789-3993d30014df : win one game vs MFL Team

class Quests:
    def __init__(self, id, checked_value, nb):
        self.id = id
        self.checked_value = int(checked_value)
        self.nb = nb

def finduser(discordId):
    discordId = str(discordId)

    query = {
        'discordId': discordId
    }

    response = requests.get(url+'users', params=query, headers=headers)
    view = response.json()
    id = view['id']
    return(id)

def give_xp(id, xp, label):

    q_give_xp = {
        'xp': xp,
        'label': label,
        'description': 'Congrats'
    }

    add_xp = requests.post(url+'users/'+str(id)+'/xp', json=q_give_xp, headers=headers)
    print(add_xp.json())
    return("OK")

def check_quests(id, variable, value):
    def infos(id, variable):
        file = open(f_quests, "r+")
        lines = file.readlines()
        for line in lines:
            name = line.split(',')[0]
            if name == id:
                return(line.split(',')[variable])

    filters = {
        'quest_id': id,
        'status': 'pending',
    }

    quests = requests.get(url+'claimed-quests', params=filters, headers=headers)
    result = quests.json()

    if len(result['data']) > 0:
        #try:
            discordID = result['data'][0]['user']['discordId']
            reviewID = result['data'][0]['id']
            uservalue = int(infos(discordID, variable))
            print(uservalue)

            if uservalue >= value:

                body = {
                    'status': 'success',
                    'claimedQuestIds': [reviewID],
                    'comment': 'Congrats ! You made it ! :)'
                }
                review = requests.post(url+'claimed-quests/review', json=body, headers=headers)
                print(review.json())
            return ("OK")
        #except:
            print("No team found")

def update(team, goals, victory, pve):
    file = open(f_quests, "r+")
    lines = file.readlines()
    l_lines = []
    found = 0
    d_pve = str(pve)
    for line in lines:
        name = line.split(',')[0]
        if name == team:
            d_match = str(int(line.split(',')[1])+1)
            d_goals = str(int(line.split(',')[2])+goals)
            d_vict = str(int(line.split(',')[3])+victory)
            at_match = str(int(line.split(',')[4])+1)
            at_goals = str(int(line.split(',')[5])+goals)
            at_vict = str(int(line.split(',')[6])+victory)
            newline = "\n"+name+","+d_match+","+d_goals+","+d_vict+","+at_match+","+at_goals+","+at_vict+","+d_pve+","
            replace = line.replace(line, newline)
            line = replace
            found = 1
        l_lines.append(line)
    if found == 0:
        addline = "\n"+team+","+str(1)+","+str(goals)+","+str(victory)+","+str(1)+","+str(goals)+","+str(victory)+","+d_pve+","
        l_lines.append(addline)
    file.seek(0)
    file.truncate(0)
    file.writelines(l_lines)
    return("OK")

def reset_file(file):
    file = open(file, "r+")
    lines = file.readlines()
    l_lines = []
    for line in lines:
        name = line.split(',')[0]
        if name != "discordId":
            at_match = str(line.split(',')[4])
            at_goals = str(line.split(',')[5])
            at_vict = str(line.split(',')[6])
            newline = name+",0,0,0,"+at_match+","+at_goals+","+at_vict+",0,"
            replace = line.replace(line, newline)
            line = replace
        l_lines.append(line)
    file.seek(0)
    file.truncate(0)
    file.writelines(l_lines)
    return("OK")

def callquests():
    for x in quests:
        ## check_quests variable : x, indice between 0-7 and number to check
        ### Quest : Play 1 game (daily)
        if str(x) == "4215cec3-dfb2-4bde-b92a-2a44ca5679f5":
            check_quests(x, 1, 1)
        ### Quest : Play 1 game vs mfl (daily)
        if str(x) == "bc879911-c61c-4eba-a789-3993d30014df":
            check_quests(x, 7, 1)