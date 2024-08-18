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
        
    def isChar(self) -> bool:
        return True
    
    def isSummon(self) -> bool:
        return False
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        return [], [], [], [], []
    
    def standardAVred(self, av: float):
        self.currAV = max(0, self.currAV - av)
        
class Numby(Summon):
    name = "Numby"
    element = "FIR"
    currSPD = 80
    currAV = 10000 / currSPD
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.role, -1, "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0, "ATK", 0, "NumbyGoGo"))
        return bl, dbl, al, dl, tl