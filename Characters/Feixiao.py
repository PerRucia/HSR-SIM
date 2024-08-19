from Character import Character
from Lightcones.VentureForth import VentureForthFeixiao
from Relics.WindSoaring import WindSoaringYunli
from Planars.Duran import Duran
from Planars.Salsotto import Salsotto
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
import logging

logger = logging.getLogger(__name__)

class Feixiao(Character):
    # Standard Character Settings
    name = "Feixiao (V3)"
    path = "HUN"
    element = "WIN"
    scaling = "ATK"
    baseHP = 1047.8
    baseATK = 601.52
    baseDEF = 388.08
    baseSPD = 112
    maxEnergy = 12
    currEnergy = 4
    ultCost = 6
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0, "TECH": 0} # Adjust accordingly
    specialEnergy = True
    hasSpecial = True
    
    # Unique Character Properties
    fuaTrigger = True
    techFua = False
    robinUlt = False
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(0, 3, 0, 3, 3, 0, 4, 4, 4, 4, 6, 18, "CR%", "SPD", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int= -1):
        super().__init__(pos, role, defaultTarget)
        self.lightcone = VentureForthFeixiao(role, 1)
        self.relic1 = WindSoaringYunli(role, 4) # same as yunli, ult also counts as FuA
        self.relic2 = None
        self.planar = Duran(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("FeixiaoTraceCR", "CR%", 0.12, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("FeixiaoTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("FeixiaoTraceDEF", "DEF%", 0.125, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("FeixiaoFuaCD", "CD%", 0.36, self.role, ["FUA"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 0.5, self.scaling, 1, "FeixiaoBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["SKL"], [self.element], [2.0, 0], [20, 0], 0.5, self.scaling, -1, "FeixiaoSkill"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["FUA"], [self.element], [1.1, 0], [5, 0], 0.5, self.scaling, 0, "FeixiaoSkillFUA"))
        bl.append(Buff("FeixiaoBuffATK", "ATK%", 0.48, self.role, ["ALL"], 3, 1, "SELF", "END"))
        bl.append(Buff("FeixiaoBuffDMG", "DMG%", 0.6, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        for _ in range(6):
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA"], [self.element], [0.9, 0], [10, 0], 0, self.scaling, 0, "FeixiaoUlt"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA"], [self.element], [1.6, 0], [0, 0], 0, self.scaling, 0, "FeixiaoUltFinal"))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        return super().useFua()
    
    def allyTurn(self, turn, result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveType != "NA" and turn.moveName not in bonusDMG:
            logger.critical("ALERT: Feixiao gained 0.5 stacks of FA")
            self.currEnergy = self.currEnergy + 0.5
            if self.fuaTrigger:
                self.fuaTrigger = False
                bl, dbl, al, dl, tl = self.useFua()
                tl.append(Turn(self.name, self.role, result.enemiesHit[0], "ST", ["FUA"], [self.element], [1.1, 0], [5, 0], 0, self.scaling, 0, "FeixiaoFUA"))
                bl.append(Buff("FeixiaoBuffDMG", "DMG%", 0.6, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.fuaTrigger = True
        self.currEnergy = self.currEnergy + 0.5
        return super().takeTurn()
    
    def special(self):
        if not self.techFua:
            self.techFua = True
            return "FeixiaoStartFUA"
        return "FeixiaoCheckRobin"
        
    def canUseUlt(self) -> bool:
        if self.robinUlt and self.currEnergy >= self.ultCost:
            return True
        else:
            return False
    
    def handleSpecial(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecial(specialRes)
        if specialRes.specialName == "FeixiaoStartFUA":
            tl.append(Turn(self.name, self.role, self.defaultTarget, "AOE", ["TECH"], [self.element], [2.2, 0], [10, 0], 0.5, self.scaling, 0, "FeixiaoTech"))
            bl.append(Buff("FexiaoTechCR", "CR%", 1.0, self.role, ["TECH"], 1, 1, "SELF", "END"))
        elif specialRes.specialName == "FeixiaoCheckRobin":
            self.robinUlt = specialRes.attr1
        return bl, dbl, al, dl, tl
    
    
    