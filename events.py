## Event (name, desc, status)
f_events = "events.csv"

async def get(i):
    with open(f_events, "r") as tevents:
        eventfile = tevents.readlines()
        eventlist = []

        for event in eventfile:
            eventcode = event.split(",")[0]
            eventname = event.split(",")[1]
            eventdesc = event.split(",")[2]
            eventstatus = event.split(",")[3]
            eventkind = event.split(",")[4]

            if int(eventstatus) > 1:
                continue

            if i == "all":
                eventlist.append(event)
            elif i == eventkind:
                eventlist.append(event)

        return eventlist