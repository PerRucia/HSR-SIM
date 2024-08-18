from Turn import *
from Buff import *
from Result import *
from Delay import *

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