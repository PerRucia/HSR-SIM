from Character import Character
from Lightcones.Multi import Multi
from Relics.Messenger import Messenger
from Relics.Thief import Thief
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Gallagher(Character):
    # Standard Character Settings
    name = "Gallagher"
    path = "ABU"
    element = "FIR"
    scaling = "ATK"
    baseHP = 1305.4
    baseATK = 529.20
    baseDEF = 441.00
    baseSPD = 98
    maxEnergy = 110
    currEnergy = 55 + 20 # 20 from e1
    ultCost = 110
    currAV = 0
    rotation = ["A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    hasSpecial = True
    
    # Unique Character Properties
    enhancedBasic = False
    canUlt = False
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(11, 3, 3, 3, 4, 4, 4, 11, 4, 2, 0, 0, "OGH%", "SPD", "HP%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Multi(role, 5)
        self.relic1 = Messenger(role, 2, False)
        self.relic2 = Thief(role, 2)
        self.planar = Keel(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("GallyTraceERS", "ERS%", 0.28 + 0.5, self.role, ["ALL"], 1, 1, "SELF", "PERM")) # 50% from e1
        bl.append(Buff("GallyTraceBE", "BE%", 0.133 + 0.2, self.role, ["ALL"], 1, 1, "SELF", "PERM")) # 20% from e6
        bl.append(Buff("GallyTraceHP", "HP%", 0.18, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("GallyTraceWBE", "WBE%", 0.20, self.role, ["ALL"], 1, 1, "SELF", "PERM")) # from e6
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        if self.enhancedBasic:
            self.enhancedBasic = False
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [2.75, 0], [30, 0], 20, self.scaling, 1, "GallyEnhancedBasic"))
        else:
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.1, 0], [10, 0], 20, self.scaling, 1, "GallyBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["SKL"], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "GallySkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.enhancedBasic = True
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "AOE", ["ULT"], [self.element], [1.65, 0], [20, 0], 5, self.scaling, 0, "GallyUlt"))
        dbl.append(Debuff("Besotted", self.role, "VULN", 0.132, "ALL", ["BREAK"], 3, 1, False, False)) # 3 turns from e4
        al.append(Advance("GallyUltAdv", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "CheckGallyUlt"
    
    def handleSpecialStart(self, specialRes: Special):
        self.canUlt = specialRes.attr1
        return super().handleSpecialEnd(specialRes)
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False
    
    
    