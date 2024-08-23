from Character import Character
from Lightcones.VentureForth import VentureForthFeixiao
from Lightcones.Cruising import Cruising
from Relics.WindSoaring import WindSoaringYunli
from Relics.Duke import DukeFeixiao
from Planars.Duran import Duran
from Planars.Izumo import Izumo
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Result, Special
from Turn import Turn
from Misc import *
import logging

logger = logging.getLogger(__name__)
    
class Feixiao(Character):
    # Standard Character Settings
    name = "Feixiao"
    path = Path.HUNT
    element = Element.WIND
    scaling = "ATK"
    baseHP = 1047.8
    baseATK = 601.52
    baseDEF = 388.08
    baseSPD = 112
    maxEnergy = 12
    currEnergy = 3
    ultCost = 6
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0, "TECH": 0} # Adjust accordingly
    specialEnergy = True
    hasSpecial = True
    
    # Unique Character Properties
    fuaTrigger = True
    technique = True
    canUlt = False
    firstTurn = True
    e2Count = 6
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    # Default = RelicStats(0, 3, 0, 3, 3, 0, 4, 4, 4, 4, 6, 18, "CR%", "SPD", "DMG%", "ATK%")
    # Bronya Tuning = RelicStats(3, 3, 0, 3, 3, 0, 4, 4, 4, 4, 6, 18, "CR%", "SPD", "DMG%", "ATK%")
    relicStats = RelicStats(0, 3, 0, 3, 3, 0, 4, 4, 4, 4, 6, 18, "CR%", "SPD", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int= -1, eidolon: int = 0, lcLevel: int = 1, sig: bool = True):
        super().__init__(pos, role, defaultTarget)
        self.lightcone = VentureForthFeixiao(role, lcLevel) if sig else Cruising(role, 5)
        self.relic1 = WindSoaringYunli(role, 4) # same as yunli, ult also counts as FuA
        self.relic2 = None
        self.planar = Duran(role)
        self.eidolon = eidolon
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("FeixiaoTraceCR", "CR%", 0.12, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("FeixiaoTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("FeixiaoTraceDEF", "DEF%", 0.125, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("FeixiaoFuaCD", "CD%", 0.36, self.role, ["FUA"], 1, 1, "SELF", "PERM"))
        if self.eidolon == 6:
            bl.append(Buff("FeixiaoE6PEN", "PEN", 0.20, self.role, ["ULT"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        basicMul = 1.1 if self.eidolon >= 3 else 1.0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [basicMul, 0], [10, 0], 0.5, self.scaling, 1, "FexiaoBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e2Bonus = 0.5 if self.eidolon >= 2 else 0
        e4Bonus = 5 if self.eidolon >= 4 else 0
        sklMul = 2.2 if self.eidolon >= 5 else 2.0
        fuaMul = 1.21 if self.eidolon >= 5 else 1.1
        e6Bonus = 1.4 if self.eidolon == 6 else 0
        atkType = ["FUA", "ULT", "DUKEFUA"] if self.eidolon == 6 else ["FUA", "DUKEFUA"]
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["SKL"], [self.element], [sklMul, 0], [20, 0], 0.5, self.scaling, -1, "FeixiaoSkill"))
        self.fuas = self.fuas + 1
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", atkType, [self.element], [fuaMul + e6Bonus, 0], [5 + e4Bonus, 0], 0.5 + e2Bonus, self.scaling, 0, "FeixiaoSkillFUA"))
        bl.append(Buff("FeixiaoSkillATK", "ATK%", 0.48, self.role, ["ALL"], 3, 1, "SELF", "END"))
        bl.append(Buff("FeixiaoFuaDMG", "DMG%", 0.60, self.role, ["ALL"], 2, 1, "SELF", "END"))
        if self.eidolon >= 4:
            bl.append(Buff("FeixiaoE4SPD", "SPD%", 0.08, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        dmgMul = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5] if self.eidolon >= 1 else [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        boltMul = 0.978 if self.eidolon >= 3 else 0.9
        finalMul = 1.728 if self.eidolon >= 3 else 1.6
        for i in range(6):
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA", "DUKEULT"], [self.element], [boltMul * dmgMul[i], 0], [10, 0], 0, self.scaling, 0, "FeixiaoUlt"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA", "DUKEULT"], [self.element], [finalMul * dmgMul[5], 0], [0, 0], 0, self.scaling, 0, "FeixiaoUltFinal"))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        e2Bonus = 0.5 if self.eidolon >= 2 else 0
        e4Bonus = 5 if self.eidolon >= 4 else 0
        fuaMul = 1.21 if self.eidolon >= 5 else 1.1
        e6Bonus = 1.4 if self.eidolon == 6 else 0
        atkType = ["FUA", "ULT", "DUKEFUA"] if self.eidolon == 6 else ["FUA", "DUKEFUA"]
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", atkType, [self.element], [fuaMul + e6Bonus, 0], [5 + e4Bonus, 0], 0.5 + e2Bonus, self.scaling, 0, "FeixiaoFua"))
        bl.append(Buff("FeixiaoFuaDMG", "DMG%", 0.60, self.role, ["ALL"], 2, 1, "SELF", "END"))
        if self.eidolon >= 4:
            bl.append(Buff("FeixiaoE4SPD", "SPD%", 0.08, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveType != "NA" and turn.moveName not in bonusDMG:
            if self.fuaTrigger:
                self.fuaTrigger = False
                bl, dbl, al, dl, tl = self.useFua()
            if "FUA" in turn.atkType and self.eidolon >= 2 and self.e2Count > 0:
                self.e2Count = max(0, self.e2Count - 1)
                tl.append(Turn(self.name, self.role, self.defaultTarget, "NA", ["ALL"], [self.element], [0, 0], [0, 0], 1.0, self.scaling, 0, "FeixiaoAllyEnergy(E2FUA)"))
            else:
                tl.append(Turn(self.name, self.role, self.defaultTarget, "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0.5, self.scaling, 0, "FeixiaoAllyEnergy"))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.fuaTrigger = True # reset fuaTrigger on turn start
        self.firstTurn = False
        self.e2Count = 4
        return super().takeTurn()
    
    def special(self):
        if self.technique:
            self.technique = False
            return "FeixiaoTech"
        return "Feixiao"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "FeixiaoTech":
            tl.append(Turn(self.name, self.role, self.defaultTarget, "AOE", ["TECH"], [self.element], [2.0, 0], [20, 0], 1.5, self.scaling, 0, "FeixiaoTech"))
        elif specialRes.specialName == "Feixiao":
            if self.fuaTrigger and specialRes.attr2 and not self.firstTurn:
                tl.append(Turn(self.name, self.role, self.defaultTarget, "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0.5, self.scaling, 0, "FeixiaPityEnergy"))
        self.canUlt = specialRes.attr1
        return bl, dbl, al, dl ,tl
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False
            
         

    
    