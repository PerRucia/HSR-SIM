from Character import Character
from Lightcones.Aeon import Sunset
from Relics.WindSoaring import WindSoaringYunli
from Planars.Duran import Duran
from RelicStats import RelicStats
from Buff import *
from Result import *
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Template(Character):
    # Standard Character Settings
    name = None
    path = None
    element = None 
    scaling = None
    baseHP = 0
    baseATK = 0
    baseDEF = 0
    baseSPD = 0
    maxEnergy = 0
    currEnergy = 0
    ultCost = 0
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "HP%", "HP%", "HP%", "HP%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = None
        self.relic1 = None
        self.relic2 = None
        self.planar = None
        
    def equip(self):
        bl, dbl, al, dl = super().equip()

        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)

        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)

        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)

        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        
        return bl, dbl, al, dl, tl
    
    
    