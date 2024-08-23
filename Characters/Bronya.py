from Character import Character
from Lightcones.PastAndFuture import PastAndFuture
from Relics.Messenger import Messenger
from Planars.Lushaka import Lushaka
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Bronya(Character):
    # Standard Character Settings
    name = "Bronya"
    path = Path.HARMONY
    element = Element.WIND
    scaling = "ATK"
    baseHP = 1241.9
    baseATK = 582.12
    baseDEF = 533.61
    baseSPD = 99
    maxEnergy = 120
    currEnergy = 60
    ultCost = 120
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {"BSC": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    cdStat = 0
    targetRole = "DPS"
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(4, 3, 3, 3, 3, 3, 3, 3, 3, 8, 0, 12, "CD%", "SPD", "HP%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = PastAndFuture(role)
        self.relic1 = Messenger(role, 4, True)
        self.relic2 = None
        self.planar = Lushaka(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("BronyaTech", "ATK%", 0.15, "ALL", ["ALL"], 2, 1, "SELF", "END"))
        bl.append(Buff("BronyaBasicCR", "CR%", 1.0, self.role, ["BSC"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("BronyaTeamDEF", "DEF%", 2.0, "ALL", ["ALL"], 2, 1, "SELF", "END"))
        bl.append(Buff("BronyaTraceDMG", "DMG%", 0.224, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("BronyaTraceCD", "CD%", 0.24, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("BronyaTraceERS", "ERS%", 0.10, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("BronyaFeixiaoUltDMG", "DMG%", 0.66, self.targetRole, ["ULT"], 1, 1, self.targetRole, "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "BronyaBasic"))
        al.append(Advance("BronyaBasic", self.role, 0.30))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["SKL"], [self.element], [0.0, 0], [0, 0], 30, self.scaling, -1, "BronyaSkill"))
        bl.append(Buff("BronyaSkillDMG", "DMG%", 0.66, self.targetRole, ["ALL"], 1, 1, self.targetRole, "END"))
        if self.role != self.targetRole:
            al.append(Advance("BronyaForward", self.targetRole, 1.0))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, -1, "NA", ["ULT"], [self.element], [0.0, 0], [0, 0], 5, self.scaling, 0, "BronyaUlt"))
        bl.append(Buff("BronyaUltATK", "ATK%", 0.55, "ALL", ["ALL"], 2, 1, "SELF", "END"))
        bl.append(Buff("BronyaUltCD", "CD%", 0.16 * self.cdStat + 0.20, "ALL", ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Bronya"
    
    def handleSpecialStart(self, specialRes: Special):
        self.cdStat = specialRes.attr1
        return super().handleSpecialStart(specialRes)
    
    
    