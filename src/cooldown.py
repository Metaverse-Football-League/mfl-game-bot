import datetime
from config import config

cooldown_scout = config["cooldown_scout"]
cooldown_match = config["cooldown_match"]

cooldowns_scout_by_user = {}
cooldowns_match_by_user = {}


def end_cooldown(user, cd_date, cd_dict, cd_name):
    now = datetime.datetime.now()

    if cd_name == "scout":
        cooldown = int(cooldown_scout)
    elif cd_name == "match":
        cooldown = int(cooldown_match)

    if now - datetime.timedelta(minutes=cooldown) > cd_date:
        cd_dict.pop(user)
        return("no")
    else:
        cdtime = cd_date + datetime.timedelta(minutes=cooldown)
        return(cdtime)


def get_user_cooldowns(user):
    cooldowns_for_user = {}

    if (user in cooldowns_scout_by_user.keys()):
        cd_date = cooldowns_scout_by_user[user]
        cd_end = end_cooldown(user, cd_date, cooldowns_scout_by_user, cd_name="scout")
        if cd_end != "no":
            cooldowns_for_user["scout"] = cd_end

    if (user in cooldowns_match_by_user.keys()):
        cd_date = cooldowns_match_by_user[user]
        cd_end = end_cooldown(user, cd_date, cooldowns_match_by_user, cd_name="match")
        if cd_end != "no":
            cooldowns_for_user["match"] = cd_end

    return(cooldowns_for_user)

def add_cd_scout(user):
    cooldowns_scout_by_user[user] = datetime.datetime.now()

def add_cd_match(user):
    cooldowns_match_by_user[user] = datetime.datetime.now()
