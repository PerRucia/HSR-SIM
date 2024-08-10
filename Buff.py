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
    "PEN",
    "ERR" 
]

targets = ["DPS", "SDPS", "SUP1", "SUP2", "SUS", "ALL"]
atkTypes = ["BASIC", "SKILL", "ULT", "FUA", "ALL"]
'''

class Buff:
    def __init__(self, name: str, buffType: str, val: float, target: str, atkType: list, turns: int, stackLimit: int):
        self.name = name
        self.buffType = buffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.storedTurns = turns
        self.turns = self.storedTurns
        self.stackLimit = stackLimit
        self.stacks = 1
        
    def __str__(self) -> str:
        res = f"{self.name} | {self.buffType} | Stacks: {self.stacks} | Value: {self.stacks * self.val}\n"
        res += f"Remaining Turns: {self.turns}\n"
        res += f"Targets: {self.target} | Affects: {self.atkType}\n"
        return res
        
    def reduceTurns(self) -> None:
        self.turns = self.turns - 1
    
    def refreshTurns(self) -> None:
        self.turns = self.storedTurns
        
    def incStack(self) -> None:
        self.refreshTurns()
        if self.stacks == self.stackLimit:
            return
        self.stacks = self.stacks + 1
        
    def getBuffVal(self) -> float:
        return self.val * self.stacks
    
    def atMaxStacks(self) -> bool:
        return True if (self.stacks == self.stackLimit) else False
        
class Debuff:
    def __init__(self, name: str, debuffType: str, val: float, target: list, atkType: list, turns: int, stackLimit: int):
        self.name = name
        self.debuffType = debuffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.storedTurns = turns
        self.turns = self.storedTurns
        self.stackLimit = stackLimit
        self.stacks = 1
        
    def __str__(self) -> str:
        res = f"{self.name} | {self.debuffType} | Stacks: {self.stacks} | Value: {self.stacks * self.val}\n"
        res += f"Remaining Turns: {self.turns}\n"
        res += f"Targets: {self.target} | Affects: {self.atkType}\n"
        return res
        
    def reduceTurns(self) -> None:
        self.turns = self.turns - 1
    
    def refreshTurns(self) -> None:
        self.turns = self.storedTurns
        
    def incStack(self) -> None:
        self.refreshTurns()
        if self.stacks == self.stackLimit:
            return
        self.stacks = self.stacks + 1
        
    def getDebuffVal(self) -> float:
        return self.val * self.stacks

    def atMaxStacks(self) -> bool:
        return True if (self.stacks == self.stackLimit) else False