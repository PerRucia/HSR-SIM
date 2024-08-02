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
    def __init__(self, name=str, buffType=str, val=float, target=list, atkType=list, turns=int, stackLimit=int):
        self.name = name
        self.buffType = buffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.turns = turns
        self.stackLimit = stackLimit
        self.stacks = 1
        
    def reduceTurns(self) -> None:
        self.turns = self.turns - 1
    
    def refreshTurns(self) -> None:
        self.turns = self.storedTurns
        
    def increaseStacks(self) -> None:
        if self.stacks == self.stackLimit:
            return
        self.stacks = self.stacks + 1
        self.refreshTurns()
        
    def getBuffVal(self) -> float:
        return self.val * self.stacks
        
class Debuff:
    def __init__(self, name=str, debuffType=str, val=float, target=list, atkType=list, turns=int, stackLimit=int):
        self.name = name
        self.debuffType = debuffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.storedTurns = turns
        self.turns = self.storedTurns
        self.stackLimit = stackLimit
        self.stacks = 1
        
    def reduceTurns(self) -> None:
        self.turns = self.turns - 1
    
    def refreshTurns(self) -> None:
        self.turns = self.storedTurns
        
    def increaseStacks(self) -> None:
        if self.stacks == self.stackLimit:
            return
        self.stacks = self.stacks + 1
        self.refreshTurns()
        
    def getDebuffVal(self) -> float:
        return self.val * self.stacks