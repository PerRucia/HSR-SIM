from Character import Character
from Lightcones.Texture import Texture
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
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(10, 2, 1, 5, 10, 3, 5, 0, 4, 8, 0, 0, "HP%", "SPD", "HP%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Texture(role, 5)
        self.relic1 = Messenger(role, 2, False)
        self.relic2 = Longevous(role, 2)
        self.planar = Keel(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("FXTraceERS", "ERS%", 0.1, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("FXTraceCR", "CR%", 0.187, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("FXTraceHP", "HP%", 0.18, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [0.5, 0], [10, 0], 20, self.scaling, 1, "FuxuanBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["SKL"], [self.element], [0, 0], [0, 0], 50, self.scaling, -1, "FuxuanSkill"))
        bl.append(Buff("FuxuanCR", "CR%", 0.12, Role.SELF, ["ALL"], 3, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "AOE", ["ULT"], [self.element], [1.0, 0], [20, 0], 5, self.scaling, 0, "FuxuanUlt"))
        return bl, dbl, al, dl, tl
    
    
    