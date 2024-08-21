from Character import Character
from Lightcones.PostOpConversation import PostOp
from Relics.Longevous import Longevous
from Relics.Messenger import Messenger
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn

class HuoHuo(Character):
    # Standard Character Settings
    name = "HuoHuo"
    path = "ABU"
    element = "WIN"
    scaling = "HP"
    baseHP = 1358.3
    baseATK = 601.52
    baseDEF = 509.36
    baseSPD = 98
    maxEnergy = 140
    currEnergy = 70
    ultCost = 140
    currAV = 0
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "BREAK": 0} # Adjust accordingly
    hasSpecial = True
    
    # Unique Character Properties
    ally1Energy = 0
    ally2Energy = 0
    ally3Energy = 0
    ally1Role = 0
    ally2Role = 0
    ally3Role = 0
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(8, 2, 3, 4, 7, 6, 4, 0, 0, 9, 5, 0, "OGH%", "SPD%", "HP%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = PostOp(self.role, 5)
        self.relic1 = Messenger(self.role, 2, True)
        self.relic2 = Longevous(self.role, 2)
        self.planar = Keel(self.role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("HHTraceHP", "HP%", 0.28, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("HHTraceERS", "ERS%", 0.18, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("HHTraceSPD", "SPD", 5, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [0.5, 0], [10, 0], 20, self.scaling, 1, "HuoHuoBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["SKL"], [self.element], [0, 0], [0,0], 36, self.scaling, -1, "HuoHuoSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        bl.append(Buff("HuoHuoUltATK", "ATK%", 0.4, "ALL", ["ALL"], 2, 1, "SELF", "END"))
        bl.append(Buff("HuoHuoERR", "ERR_F", self.ally1Energy, self.ally1Role, ["ALL"], 1, 1, self.ally1Role, "PERM"))
        bl.append(Buff("HuoHuoERR", "ERR_F", self.ally2Energy, self.ally2Role, ["ALL"], 1, 1, self.ally2Role, "PERM"))
        bl.append(Buff("HuoHuoERR", "ERR_F", self.ally3Energy, self.ally3Role, ["ALL"], 1, 1, self.ally3Role, "PERM"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["ULT"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "HuoHuoULT"))
        return bl, dbl, al, dl, tl
    
    def special(self):
        self.hasSpecial = False
        return "HuoHuoUlt"
    
    def handleSpecialStart(self, specialRes: Special):
        self.ally1Energy = specialRes.attr1[0]
        self.ally1Role = specialRes.attr1[1]
        self.ally2Energy = specialRes.attr2[0]
        self.ally2Role = specialRes.attr2[1]
        self.ally3Energy = specialRes.attr3[0]
        self.ally3Role = specialRes.attr3[1]
        return super().handleSpecialStart(specialRes)
    
    