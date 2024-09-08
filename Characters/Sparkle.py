from Character import Character
from RelicStats import RelicStats
from Lightcones.Dance3 import Dance3
from Relics.Messenger import Messenger
from Planars.Keel import Keel
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Sparkle(Character):
    # Standard Character Settings
    name = "Sparkle"
    path = Path.HARMONY
    element = Element.QUANTUM 
    scaling = Scaling.ATK
    baseHP = 1397.1
    baseATK = 523.91
    baseDEF = 485.10
    baseSPD = 101
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    cdStat = 0
    startSP = True
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, targetRole = Role.DPS, quaAllies = 0, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Dance3(role)
        self.relic1 = r1 if r1 else Messenger(role, 4, True)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else Keel(role)
        self.relicStats = subs if subs else RelicStats(13, 4, 0, 4, 4, 0, 3, 3, 3, 3, 0, 11, Pwr.CD_PERCENT, Pwr.SPD, Pwr.HP_PERCENT, Pwr.ERR_PERCENT)
        self.targetRole = targetRole
        self.quaAllies = quaAllies
        self.rotation = rotation if rotation else ["E"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("SparkleTraceHP", Pwr.HP_PERCENT, 0.28, self.role))
        bl.append(Buff("SparkleTraceCD", Pwr.CD_PERCENT, 0.24, self.role))
        bl.append(Buff("SparkleTraceERS", Pwr.ERS_PERCENT, 0.10, self.role))
        atkBoost = [0, 0.05, 0.15, 0.30]
        bl.append(Buff("SparkleTeamATK", Pwr.ATK_PERCENT, 0.15 + atkBoost[self.quaAllies], Role.ALL))
        e5DMG = 0.066 if self.eidolon >= 5 else 0.06
        bl.append(Buff("SparkleDMG", Pwr.DMG_PERCENT, e5DMG * 3, Role.ALL))
        if self.eidolon >= 2:
            bl.append(Buff("SparkleE2SHRED", Pwr.SHRED, 0.24, Role.ALL))
        if self.eidolon == 6:
            bl.append(Buff("SparkleE6CD", Pwr.CD_PERCENT, 0.30, Role.ALL))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Mul = 1.1 if self.eidolon >= 3 else 1.0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Mul, 0], [10, 0], 30, self.scaling, 1, "SparkleBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e3CDMul = 0.264 if self.eidolon >= 3 else 0.24
        e3CDFlat = 0.486 if self.eidolon >= 3 else 0.45
        bl.append(Buff("SparkleCD", Pwr.CD_PERCENT, self.cdStat * e3CDMul + e3CDFlat, self.targetRole, turns=2, tickDown=self.targetRole, tdType=TickDown.START))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "SparkleSkill"))
        if self.role != self.targetRole:
            al.append(Advance("SparkleForward", self.targetRole, 0.50))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        e1Turns = 3 if self.eidolon >= 1 else 2
        e4SP = 5 if self.eidolon >= 4 else 4
        e5DMG = 0.108 if self.eidolon >= 5 else 0.1
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, e4SP, "SparkleUlt"))
        bl.append(Buff("SparkleUltDMG", Pwr.DMG_PERCENT, e5DMG * 3, Role.ALL, turns=e1Turns, tdType=TickDown.END))
        if self.eidolon >= 1:
            bl.append(Buff("SparkleE1ATK", Pwr.ATK_PERCENT, 0.40, Role.ALL, turns=3, tdType=TickDown.END))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)

        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Sparkle"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if self.startSP:
            self.startSP = False
            tl.append(Turn(self.name, self.role, self.defaultTarget, Targeting.NA, [AtkType.SPECIAL], [self.element], [0, 0], [0, 0], 0, self.scaling, 3, "SparkleTechSP"))
        self.cdStat = specialRes.attr1
        return bl, dbl, al, dl, tl
    