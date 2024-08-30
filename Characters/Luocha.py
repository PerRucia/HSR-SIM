from Character import Character
from Lightcones.Multi import Multi
from Relics.Musketeer import Musketeer
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Result
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Luocha(Character):
    # Standard Character Settings
    name = "Luocha"
    path = Path.ABUNDANCE
    element = Element.IMAGINARY
    scaling = Scaling.ATK
    baseHP = 1280.7
    baseATK = 756.76
    baseDEF = 363.82
    baseSPD = 101
    maxEnergy = 100
    currEnergy = 50
    ultCost = 100
    currAV = 0
    rotation = ["A"] # Adjust accordingly
    dmgDct = {AtkType.BSC: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else Multi(role, 5)
        self.relic1 = r1 if r1 else Musketeer(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Keel(role)
        self.relicStats = subs if subs else RelicStats(13, 2, 3, 2, 4, 8, 4, 4, 4, 4, 0, 0, Pwr.OGH_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.ERR_PERCENT)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("LuochaTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LuochaTraceHP", Pwr.HP_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LuochaTraceDEF", Pwr.DEF_PERCENT, 0.125, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "LuochaBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "LuochaSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.ULT], [self.element], [2.0, 0], [20, 0], 5, self.scaling, 0, "LuochaUlt"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if result.turnName != "LuochaAutohealERR":
            tl.append(Turn(self.name, self.role, self.getTargetID(-1), Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 10, self.scaling, 0, "LuochaAutohealERR"))
        return bl, dbl, al, dl, tl
    
    
    