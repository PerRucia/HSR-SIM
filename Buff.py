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
tickDown = ["ENEMY", "SELF", "DPS", "SUP1", "SUP2", "SUS"] | determines on whose turn this buff ticks down on, if set to "SELF", will tick down on "SELF"'s turn
tdType = ["PERM", "START", "END"] | determines whether the buff ticks down, PERM = permanent buff, START = at start of turn, END = at end of turn
'''

class Buff:
    def __init__(self, name: str, buffType: str, val: float, target: str, atkType: list, turns: int, stackLimit: int, tickDown: str, tdType: str):
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
        res = f"{self.name} | {self.buffType} | Stacks: {self.stacks} | Value: {self.stacks * self.val} | "
        res += f"Remaining Turns: {self.turns} | TickDown: {self.tickDown}, {self.tdType} | "
        res += f"Target: {self.target} | Affects: {self.atkType}"
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
    def __init__(self, name: str, debuffType: str, val: float, target: list, atkType: list, turns: int, stackLimit: int, isDot: bool):
        self.name = name
        self.debuffType = debuffType
        self.val = val
        self.target = target
        self.atkType = atkType
        self.storedTurns = turns
        self.turns = self.storedTurns
        self.stackLimit = stackLimit
        self.stacks = 1
        self.isDot = isDot
        
    def __str__(self) -> str:
        res = f"{self.name} | {self.debuffType} | Stacks: {self.stacks} | Value: {self.stacks * self.val} | "
        res += f"Remaining Turns: {self.turns} | "
        res += f"Target: {self.target} | Affects: {self.atkType} | DOT: {self.isDot}"
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