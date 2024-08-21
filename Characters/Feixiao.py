from Character import Character
from Lightcones.VentureForth import VentureForthFeixiao
from Relics.WindSoaring import WindSoaringYunli
from Planars.Duran import Duran
from Relics.Eagle import Eagle
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
    prevTurnFua = True
    
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
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if not self.prevTurnFua:
            tl.append(Turn(self.name, self.role, result.enemiesHit[0], "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0.5, self.scaling, 0, "FeixiaoPityEnergy"))
        self.prevTurnFua = True
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn, result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveType != "NA" and turn.moveName not in bonusDMG:
            tl.append(Turn(self.name, self.role, result.enemiesHit[0], "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0.5, self.scaling, 0, "FeixiaoAllyAttackEnergy"))
            if self.fuaTrigger:
                self.fuaTrigger = False
                self.prevTurnFua = True
                bl, dbl, al, dl, tl = self.useFua()
                tl.append(Turn(self.name, self.role, result.enemiesHit[0], "ST", ["FUA"], [self.element], [1.1, 0], [5, 0], 0.5, self.scaling, 0, "FeixiaoFUA"))
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
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "FeixiaoStartFUA":
            tl.append(Turn(self.name, self.role, self.defaultTarget, "AOE", ["TECH"], [self.element], [2.2, 0], [10, 0], 0.5, self.scaling, 0, "FeixiaoTech"))
            bl.append(Buff("FexiaoTechCR", "CR%", 1.0, self.role, ["TECH"], 1, 1, "SELF", "END"))
        elif specialRes.specialName == "FeixiaoCheckRobin":
            self.robinUlt = specialRes.attr1
        return bl, dbl, al, dl, tl
    
class FeixiaoEidolons(Character):
    # Standard Character Settings
    name = "Feixiao"
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
    prevTurnFua = True
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(0, 3, 0, 3, 3, 0, 4, 4, 4, 4, 6, 18, "CR%", "SPD", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int= -1, eidolon: int = 0):
        super().__init__(pos, role, defaultTarget)
        self.lightcone = VentureForthFeixiao(role, 1)
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
        if self.eidolon >= 4:
            bl.append(Buff("FeixiaoE4VULN", "VULN", 0.10, "ALL", ["FUA"], 1, 1, "SELF", "PERM"))
        if self.eidolon == 6:
            bl.append(Buff("FeixiaoE6PEN", "PEN", 0.20, "ALL", ["ULT"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Bonus = 0.1 if self.eidolon >= 3 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.0 + e3Bonus, 0], [10, 0], 0.5, self.scaling, 1, "FeixiaoBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        bonusStack = 0.5 if self.eidolon >= 2 else 0
        e5bonus = 0.2 if self.eidolon >= 5 else 0
        e5fuaBonus = 0.11 if self.eidolon >= 5 else 0
        fuaTypes = ["FUA", "ULT"] if self.eidolon == 6 else ["FUA"]
        e6fuaBonus = 1.4 if self.eidolon == 6 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["SKL"], [self.element], [2.0 + e5bonus, 0], [20, 0], 0.5, self.scaling, -1, "FeixiaoSkill"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", fuaTypes, [self.element], [1.1 + e5fuaBonus + e6fuaBonus, 0], [5, 0], 0.5 + bonusStack, self.scaling, 0, "FeixiaoSkillFUA"))
        bl.append(Buff("FeixiaoBuffATK", "ATK%", 0.48, self.role, ["ALL"], 3, 1, "SELF", "END"))
        bl.append(Buff("FeixiaoBuffDMG", "DMG%", 0.6, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        baseHitMul = 0.978 if self.eidolon >= 3 else 0.9
        finalHitMul = 1.728 if self.eidolon >= 3 else 1.6
        dmgMul = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.5] if self.eidolon >= 1 else [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        self.currEnergy = self.currEnergy - self.ultCost
        for i in range(6):
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA"], [self.element], [baseHitMul * dmgMul[i], 0], [10, 0], 0, self.scaling, 0, "FeixiaoUlt"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA"], [self.element], [finalHitMul * dmgMul[6], 0], [0, 0], 0, self.scaling, 0, "FeixiaoUltFinal"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if not self.prevTurnFua:
            tl.append(Turn(self.name, self.role, result.enemiesHit[0], "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0.5, self.scaling, 0, "FeixiaoPityEnergy"))
        self.prevTurnFua = True
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn, result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveType != "NA" and turn.moveName not in bonusDMG:
            tl.append(Turn(self.name, self.role, result.enemiesHit[0], "NA", ["ALL"], [self.element], [0, 0], [0, 0], 0.5, self.scaling, 0, "FeixiaoAllyAttackEnergy"))
            if self.fuaTrigger:
                self.fuaTrigger = False
                self.prevTurnFua = True
                bl, dbl, al, dl, tl = self.useFua()
                bonusStack = 0.5 if self.eidolon >= 2 else 0
                e5fuaBonus = 0.11 if self.eidolon >= 5 else 0
                fuaTypes = ["FUA", "ULT"] if self.eidolon == 6 else ["FUA"]
                e6fuaBonus = 1.4 if self.eidolon == 6 else 0
                tl.append(Turn(self.name, self.role, result.enemiesHit[0], "ST", fuaTypes, [self.element], [1.1 + e5fuaBonus + e6fuaBonus, 0], [5, 0], 0.5 + bonusStack, self.scaling, 0, "FeixiaoFUA"))
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
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "FeixiaoStartFUA":
            tl.append(Turn(self.name, self.role, self.defaultTarget, "AOE", ["TECH"], [self.element], [2.2, 0], [10, 0], 0.5, self.scaling, 0, "FeixiaoTech"))
            bl.append(Buff("FexiaoTechCR", "CR%", 1.0, self.role, ["TECH"], 1, 1, "SELF", "END"))
        elif specialRes.specialName == "FeixiaoCheckRobin":
            self.robinUlt = specialRes.attr1
        return bl, dbl, al, dl, tl
    
    
    