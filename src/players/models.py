class Player:
    def __init__(self, displayName, ovr, pos, teamid, nat, rarity, form, number, isYellowCard, isRedCard):
        self.displayName = displayName
        self.form = int(form)
        self.number = number
        self.nat = nat
        self.pos = pos
        self.ovr = int(ovr)
        self.rarity = rarity
        self.teamid = teamid
        self.isYellowCard = isYellowCard
        self.isRedCard = isRedCard

players_positions_indices = {
    'GK': 1,
    'LB': 2,
    'LWB': 2,
    'CB': 4,
    'RB': 5,
    'RWB': 5,
    'CDM': 6,
    'CM': 7,
    'CAM': 8,
    'LW': 12,
    'LM': 9,
    'RW': 13,
    'RM': 10,
    'CF': 11,
    'ST': 14,
}

players_positions_placements = {
    'GK': 1,
    'LB': 2,
    'LWB': 2,
    'CB': 3,
    'RB': 5,
    'RWB': 5,
    'CDM': 6,
    'CM': 7,
    'CAM': 7,
    'AM': 7,
    'LW': 9,
    'LM': 9,
    'RW': 10,
    'RM': 10,
    'CF': 11,
    'ST': 11,
    'FW': 11
}
