'''
buffList = [
    "SPD",
    "HP",
    "ATK",
    "DEF",
    "HP%",
    "ATK%",
    "DEF%",
    "CR%",
    "CD%",
    "BE%",
    "OGH%",
    "ERR%",
    "EHR%",
    "ERS%",
    "DMG%",
    "SHRED",
    "VULN",
    "PEN"
]

targets = ["DPS", "SDPS", "SUP", "SUS", "ALL"]
atkTypes = ["BASIC", "SKILL", "ULT", "FUA", "ALL"]
'''

class Buff:
    def __init__(self, name=str, buffType=str, val=float, target=list, atkType=list, turns=int):
        self.name = name
        self.buffType = buffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.turns = turns
        
class Debuff:
    def __init__(self, name=str, debuffType=str, val=float, target=list, atkType=list, turns=int):
        self.name = name
        self.debuffType = debuffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.turns = turns