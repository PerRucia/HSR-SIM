import logging

from Buff import *
from Character import Character
from Delay import *
from Lightcones.Texture import Texture
from Planars.Keel import Keel
from RelicStats import RelicStats
from Relics.Longevous import Longevous
from Relics.Messenger import Messenger
from Result import Special
from Turn import Turn

logger = logging.getLogger(__name__)

class Fuxuan(Character):
    # Standard Character Settings
    name = "FuXuan"
    path = Path.PRESERVATION
    element = Element.QUANTUM
    scaling = Scaling.HP
    baseHP = 1474.7
    baseATK = 465.70
    baseDEF = 606.38
    baseSPD = 100
    maxEnergy = 135
    currEnergy = 135 /2
    ultCost = 135
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    aggroSplit = []
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 1, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Texture(role, 5)
        self.relic1 = r1 if r1 else Messenger(role, 2, False)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else Longevous(role, 2))
        self.planar = pl if pl else Keel(role)
        rope = Pwr.HP_PERCENT if eidolon >= 4 else Pwr.ERR_PERCENT
        self.relicStats = subs if subs else RelicStats(8, 0, 4, 4, 12, 4, 4, 4, 4, 4, 0, 0, Pwr.HP_PERCENT, Pwr.SPD, Pwr.HP_PERCENT, rope)
        self.rotation = rotation if rotation else ["E", "A", "A"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("FXTraceERS", Pwr.ERS_PERCENT, 0.1, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("FXTraceCR", Pwr.CR_PERCENT, 0.187, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("FXTraceHP", Pwr.HP_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 1:
            bl.append(Buff("FXE1CD", Pwr.CD_PERCENT, 0.3, Role.ALL))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e5Mul = 0.55 if self.eidolon >= 5 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Mul, 0], [10, 0], 20, self.scaling, 1, "FuxuanBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 50, self.scaling, -1, "FuxuanSkill"))
        bl.append(Buff("FuxuanCR", Pwr.CR_PERCENT, 0.132 if self.eidolon >= 3 else 0.12, Role.SELF, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        e5Mul = 1.08 if self.eidolon >= 5 else 1.0
        e6Mul = 2.4 if self.eidolon >= 6 else 0
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.ULT], [self.element], [e5Mul + e6Mul, 0], [20, 0], 5, self.scaling, 0, "FuxuanUlt"))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Fuxuan"
    
    def handleSpecialStart(self, specialRes: Special):
        self.hasSpecial = False
        self.aggroSplit = specialRes.attr1
        return super().handleSpecialStart(specialRes)
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)
        if self.eidolon >= 4:
            e4ERR = sum([self.aggroSplit[i] * 5 for i in range(len(self.aggroSplit)) if i != self.pos])
            bl.append(Buff("FuxuanE4ERR", Pwr.ERR_T, e4ERR, self.role))
        return bl, dbl, al, dl, tl
    
    
    