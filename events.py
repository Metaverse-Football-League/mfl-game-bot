## Event (name, desc, status)
f_events = "events.csv"


class Event:
    def __init__(self, code, name, desc, status, kind, opponent):
        self.code = code
        self.name = name
        self.desc = desc
        self.status = status
        self.kind = kind
        self.opponent = opponent

async def get(i):
    with open(f_events, "r") as tevents:
        eventfile = tevents.readlines()
        eventlist = []

        for event in eventfile:
            code = event.split(",")[0]
            name = event.split(",")[1]
            desc = event.split(",")[2]
            status = event.split(",")[3]
            kind = event.split(",")[4]
            opponent = event.split(",")[5]

            if int(status) > 1:
                continue

            if i == "all":
                mevent = Event(code, name, desc, status, kind, opponent)
                eventlist.append(mevent)
            elif i == kind:
                mevent = Event(code, name, desc, status, kind, opponent)
                eventlist.append(mevent)

        return eventlist