from Character import Character
from Lightcones.Resolution import ResolutionPela
from Relics.Messenger import Messenger
from Relics.Longevous import Longevous
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Pela(Character):
    # Standard Character Settings
    name = "Pela"
    path = "NIH"
    element = "ICE"
    scaling = "ATK"
    baseHP = 987.8
    baseATK = 546.84
    baseDEF = 463.05
    baseSPD = 105
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {"BSC": 0, "SKL": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(11, 2, 2, 2, 2, 2, 2, 2, 13, 10, 0, 0, "HP%", "SPD", "DEF%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = ResolutionPela(role, 5)
        self.relic1 = Longevous(role, 2)
        self.relic2 = Messenger(role, 2)
        self.planar = Keel(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("PelaTraceEHR", "EHR%", 0.1, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("PelaTraceDMG", "DMG%", 0.224, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("PelaTraceATK", "ATK%", 0.18, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("PelaTeamEHR", "EHR%", 0.1, "ALL", ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("PelaDebuffBonusDMG", "DMG%", 0.2, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)

        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        dbl.append(Debuff("PelaIceRes", self.role, "ICEPEN", 0.12, self.getTargetID(enemyID), ["ALL"], 1, 1, False, False))
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
    
    
    