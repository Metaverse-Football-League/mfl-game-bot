import datetime

on_cooldown_scout = {}
on_cooldown_match = {}

cooldown = 5

def end_cooldown(user, cd_date, cd_dict):
    now = datetime.datetime.now()

    if now - datetime.timedelta(minutes=cooldown) > cd_date:
        cd_dict.pop(user)
        return("no")
    else:
        cdtime = cd_date + datetime.timedelta(minutes=cooldown)
        return(str(cdtime).split(" ")[1].split(".")[0])


def check(user):

    cd_list = {}

    if (user in on_cooldown_scout.keys()):
        cd_date = on_cooldown_scout[user]
        cd_end = end_cooldown(user, cd_date, on_cooldown_scout)
        if cd_end != "no":
            cd_list["scout"] = cd_end

    if (user in on_cooldown_match.keys()):
        cd_date = on_cooldown_match[user]
        cd_end = end_cooldown(user, cd_date, on_cooldown_match)
        if cd_end != "no":
            cd_list["match"] = cd_end

    return(cd_list)

def add_cd_scout(user):
    if "KevinKazama" not in user:
        on_cooldown_scout[user] = datetime.datetime.now()

def add_cd_match(user):
    if "KevinKazama" not in user:
        on_cooldown_match[user] = datetime.datetime.now()



