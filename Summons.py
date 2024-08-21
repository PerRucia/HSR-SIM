from typing import Any
from Buff import Buff, Debuff
from Delay import Advance, Delay
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
        
class Numby(Summon):
    name = "Numby"
    element = "FIR"
    currSPD = 80
    currAV = 10000 / currSPD
    
    def __init__(self, ownerRole: str, role: str) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0, "ATK", 0, "NumbyGoGo"))
        return bl, dbl, al, dl, tl
    
class Fuyuan(Summon):
    name = "Fuyuan"
    element = "FIR"
    currSPD = 90
    currAV = 10000 / currSPD
    
    def __init__(self, ownerRole: str, role: str) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0, "ATK", 0, "FuyuanGoGo"))
        return bl, dbl, al, dl, tl