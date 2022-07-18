from config import config
import utils_file

f_events = config["dataPath"] + "events.csv"

class Event:
    def __init__(self, code, name, desc, status, kind, opponent, leaderboard, reward):
        self.code = code
        self.name = name
        self.desc = desc
        self.status = status
        self.kind = kind
        self.opponent = opponent
        self.leaderboard = leaderboard
        self.reward = reward

def create_event_from_csv(row, columns):
    code = columns[0]
    name = columns[1]
    desc = columns[2]
    status = columns[3]
    kind = columns[4]
    opponent = columns[5]
    leaderboard = columns[6]
    reward = columns[7]

    if int(status) > 1:
        return(None)

    return(Event(code, name, desc, status, kind, opponent, leaderboard, reward))

async def get():
    events = utils_file.read_csv_file(create_event_from_csv, f_events)
    return events

async def get_by_code(code):
    def create_event_from_csv_for_code(row, columns):
        eventCode = columns[0]
        if code != eventCode:
            return(None)
        return(create_event_from_csv(row, columns))

    events = utils_file.read_csv_file(create_event_from_csv_for_code, f_events)
    return events
