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
from Misc import *

class Buff:
    def __init__(self, name: str, buffType: str, val: float, target: Role, atkType: list, turns: int, stackLimit: int, tickDown: Role, tdType: TickDown):
        self.name = name
        self.buffType = buffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.storedTurns = turns
        self.turns = self.storedTurns
        self.stackLimit = stackLimit
        self.stacks = 1
        self.tickDown = tickDown
        self.tdType = tdType
        
    def __str__(self) -> str:
        res = f"{self.name} | {self.buffType} | Stacks: {self.stacks} | Value: {self.stacks * self.val:.3f} | "
        res += f"Remaining Turns: {self.turns} | TickDown: {self.tickDown.name}, {self.tdType.name} | "
        res += f"Target: {self.target.name} | Affects: {self.atkType}"
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
    
    def updateBuffVal(self, val: float):
        self.val = val
        
class Debuff:
    def __init__(self, name: str, charRole: Role, debuffType: str, val: float, target: list, atkType: list, turns: int, stackLimit: int, isDot: bool, dotSplit, isBlast: bool):
        self.name = name
        self.charRole = charRole
        self.debuffType = debuffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.storedTurns = turns
        self.turns = self.storedTurns
        self.stackLimit = stackLimit
        self.stacks = 1
        self.isDot = isDot
        self.dotSplit = dotSplit
        self.isBlast = isBlast
        self.dotMul = 0
        
    def __str__(self) -> str:
        res = f"{self.name} | From: {self.charRole.name} | {self.debuffType} | Stacks: {self.stacks} | Value: {self.stacks * self.val:.3f} | "
        res += f"Remaining Turns: {self.turns} | Target: {self.target} | Affects: {self.atkType} | DOT: {self.isDot} | Blast: {self.isBlast}"
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
        if self.name == "AshenRoasted":
            return self.val + (self.stacks) * 0.05
        return self.val * self.stacks

    def atMaxStacks(self) -> bool:
        return True if (self.stacks == self.stackLimit) else False