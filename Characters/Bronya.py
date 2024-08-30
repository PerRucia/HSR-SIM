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
    scaling = Scaling.ATK
    baseHP = 1241.9
    baseATK = 582.12
    baseDEF = 533.61
    baseSPD = 99
    maxEnergy = 120
    currEnergy = 60
    ultCost = 120
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {AtkType.BSC: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    cdStat = 0
    targetRole = Role.DPS
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else PastAndFuture(role)
        self.relic1 = r1 if r1 else Messenger(role, 4, True)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Lushaka(role)
        self.relicStats = subs if subs else RelicStats(14, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 10, Pwr.CD_PERCENT, Pwr.SPD, Pwr.HP_PERCENT, Pwr.ERR_PERCENT)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("BronyaTech", Pwr.ATK_PERCENT, 0.15, Role.ALL, [AtkType.ALL], 2, 1, Role.SELF, TickDown.END))
        bl.append(Buff("BronyaBasicCR", Pwr.CR_PERCENT, 1.0, self.role, [AtkType.BSC], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("BronyaTeamDEF", Pwr.DEF_PERCENT, 2.0, Role.ALL, [AtkType.ALL], 2, 1, Role.SELF, TickDown.END))
        bl.append(Buff("BronyaTraceDMG", Pwr.DMG_PERCENT, 0.224, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("BronyaTraceCD", Pwr.CD_PERCENT, 0.24, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("BronyaTraceERS", Pwr.ERS_PERCENT, 0.10, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("BronyaFeixiaoUltDMG", Pwr.DMG_PERCENT, 0.66, self.targetRole, [AtkType.ULT], 1, 1, self.targetRole, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "BronyaBasic"))
        al.append(Advance("BronyaBasic", self.role, 0.30))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0.0, 0], [0, 0], 30, self.scaling, -1, "BronyaSkill"))
        bl.append(Buff("BronyaSkillDMG", Pwr.DMG_PERCENT, 0.66, self.targetRole, [AtkType.ALL], 1, 1, self.targetRole, TickDown.END))
        if self.role != self.targetRole:
            al.append(Advance("BronyaForward", self.targetRole, 1.0))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, -1, Targeting.NA, [AtkType.ULT], [self.element], [0.0, 0], [0, 0], 5, self.scaling, 0, "BronyaUlt"))
        bl.append(Buff("BronyaUltATK", Pwr.ATK_PERCENT, 0.55, Role.ALL, [AtkType.ALL], 2, 1, Role.SELF, TickDown.END))
        bl.append(Buff("BronyaUltCD", Pwr.CD_PERCENT, 0.16 * self.cdStat + 0.20, Role.ALL, [AtkType.ALL], 2, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Bronya"
    
    def handleSpecialStart(self, specialRes: Special):
        self.cdStat = specialRes.attr1
        return super().handleSpecialStart(specialRes)
    
    
    