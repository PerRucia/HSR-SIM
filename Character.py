from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from Planar import Planar

class Character:
    # Basic Stats
    name = "Character"
    path = "PATH"
    element = "ELE"
    role = "DPS" # DPS/SDPS/SUS/SUP
    baseHP = 0
    baseATK = 0
    baseDEF = 0
    baseSPD = 0
    
    # Equipment
    lightcone = Lightcone(1)
    relic1 = Relic(4)
    relic2 = Relic(2)
    planar = Planar()
    
    def __init__(self, pos: int) -> None:
        self.pos = pos
    
    def __str__(self) -> str:
        res = f"{self.name} | {self.path} | {self.element} | Pos:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self) -> tuple[list, list]: # init function to add base buffs to wearer
        pass
    
    def useSkl(self):
        pass
    
    def useBsc(self):
        pass
    
    def useUlt(self):
        pass
    
    def useFua(self):
        pass
    
    def useHit(self):
        pass
    
    def allyTurn(self, turn):
        pass
    
a = Character(2)
print(a)