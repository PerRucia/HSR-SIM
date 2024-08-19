from Character import Character
from Lightcones.ConcertForTwo import ConcertForTwo
from Relics.Knight import Knight
from Relics.Messenger import Messenger
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *

class Aventurine(Character):
    # Standard Character Settings
    name = "Aventurine"
    path = "PRE"
    element = "IMG"
    scaling = "DEF"
    baseHP = 1203.0
    baseATK = 446.29
    baseDEF = 654.88
    baseSPD = 106
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    rotation = ["A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    baseDefStat = 0
    bbPerHit = 0
    fuaTrigger = 3
    blindBetStacks = 0

    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(3, 2, 1, 8, 4, 3, 3, 0, 4, 2, 13, 7, "DEF%", "SPD", "DEF%", "DEF%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = ConcertForTwo(role, 5, 1.0)
        self.relic1 = Knight(role, 2)
        self.relic2 = Messenger(role, 2, False)
        self.planar = Keel(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("AvenTraceDEF", "DEF%", 0.35, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("AvenTraceDMG", "DMG%", 0.144, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("AvenTraceERS", "ERS%", 0.10, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "AvenBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["SKL"], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "AvenSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT"], [self.element], [2.7, 0], [30, 0], 5, self.scaling, 0, "AvenUlt"))
        self.currEnergy = self.currEnergy - self.ultCost
        self.blindBetStacks = min(self.blindBetStacks + 4, 10)
        dbl.append(Debuff("AvenUltCD", self.role, "CD%", 0.15, 1, ["ALL"], 3, 1, False, False))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        self.blindBetStacks = self.blindBetStacks - 7
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["FUA"], [self.element], [0.25, 0], [10/3, 0], 1, self.scaling, 0, "AvenFUA"))
        for _ in range(6):
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["FUA"], [self.element], [0.25, 0], [10/3, 0], 1, self.scaling, 0, "AvenFUAExtras"))
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)
        self.blindBetStacks = min(10, self.blindBetStacks + self.bbPerHit)
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Turn):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if ("FUA" in turn.atkType) and (turn.moveName not in bonusDMG) and (self.fuaTrigger > 0):
            self.fuaTrigger = self.fuaTrigger - 1
            self.blindBetStacks = min(10, self.blindBetStacks + 1)
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.fuaTrigger = 3
        return super().takeTurn()
    
    def special(self):
        return "getAvenDEF" if self.baseDefStat == 0 else "checkAvenFUA"
    
    def handleSpecial(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecial(specialRes)
        if self.blindBetStacks >= 7 and specialRes.specialName == "checkAvenFUA":
            bl, dbl, al, dl, tl = self.useFua()
        if specialRes.specialName == "getAvenDEF":
            self.baseDefStat = specialRes.attr1
            self.bbPerHit = specialRes.attr2
            crBuff = min((self.baseDefStat - 1600) // 100, 24)
            bl.append(Buff("AvenBonusCR", "CR%", 0.02 * crBuff, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl, tl
    
    
    