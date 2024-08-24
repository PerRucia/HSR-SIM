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
    dmgDct = {"BSC": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(10, 2, 2, 2, 2, 14, 4, 0, 4, 8, 0, 0, "OGH%", "SPD", "ATK%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Multi(role, 5)
        self.relic1 = Musketeer(role, 4)
        self.relic2 = None
        self.planar = Keel(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("LuochaTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LuochaTraceHP", "HP%", 0.18, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LuochaTraceDEF", "DEF%", 0.125, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "LuochaBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["SKL"], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "LuochaSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "AOE", ["ULT"], [self.element], [2.0, 0], [20, 0], 5, self.scaling, 0, "LuochaUlt"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if result.turnName != "LuochaAutohealERR":
            tl.append(Turn(self.name, self.role, self.getTargetID(-1), "NA", ["ALL"], [self.element], [0, 0], [0, 0], 10, self.scaling, 0, "LuochaAutohealERR"))
        return bl, dbl, al, dl, tl
    
    
    