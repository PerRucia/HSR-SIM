from typing import Any
from Buff import Buff, Debuff
from Delay import Advance, Delay
from Result import Result
from Turn import *
from Buff import *
from Result import *
from Delay import *
from Turn import Turn

class Summon:
    name = "Summon"
    element = None
    currSPD = 100
    currAV = 10000 / currSPD
    currEnergy = 0
    maxEnergy = 0
    
    def __init__(self, ownerRole: str, role: str) -> None:
        self.ownerRole = ownerRole
        self.role = role
        self.priority = 0
        
    def isChar(self) -> bool:
        return True
    
    def isSummon(self) -> bool:
        return True
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        return [], [], [], [], []
    
    def standardAVred(self, av: float):
        self.currAV = max(0, self.currAV - av)
        
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0, self.currAV - reduceValue)
        
    def allyTurn(self, turn: Turn, result: Result)-> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        return [], [], [], [], []
        
class Numby(Summon):
    name = "Numby"
    element = Element.FIRE
    scaling = Scaling.ATK
    currSPD = 80
    currAV = 10000 / currSPD
    
    def __init__(self, ownerRole: str, role: str) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, "NumbyGoGo"))
        return bl, dbl, al, dl, tl
    
class Fuyuan(Summon):
    name = "Fuyuan"
    element = Element.FIRE
    scaling = Scaling.ATK
    currSPD = 90
    currAV = 10000 / currSPD
    
    def __init__(self, ownerRole: str, role: str) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, "FuyuanGoGo"))
        return bl, dbl, al, dl, tl
    
class deHenshin(Summon):
    name = "de-Henshin!"
    element = Element.FIRE
    scaling = Scaling.ATK
    currSPD = 1
    currAV = 10000
    
    def __init__(self, ownerRole: str, role: str) -> None:
        super().__init__(ownerRole, role)
        
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        self.currAV = 10000
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, self.name))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveName == "FireflyUlt":
            self.currAV = 10000 / 70
        return bl, dbl, al, dl, tl