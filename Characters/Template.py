from Character import Character
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
    dmgDct = {Move.BSC: 0, Move.FUA: 0, Move.SKL: 0, Move.ULT: 0, Move.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else None
        self.relic1 = r1 if r1 else None
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else None
        self.relicStats = subs if subs else RelicStats(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, Pwr.HP_PERCENT, Pwr.HP_PERCENT, Pwr.HP_PERCENT, Pwr.HP_PERCENT)
        
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
    
    
    