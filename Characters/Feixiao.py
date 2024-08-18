from Character import Character
from Lightcones.VentureForth import VentureForthFeixiao
from Relics.WindSoaring import WindSoaringYunli
from Planars.Duran import Duran
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
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    specialEnergy = True
    hasSpecial = True
    
    # Unique Character Properties
    fuaTrigger = True
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(0, 3, 0, 3, 3, 0, 4, 4, 4, 4, 7, 17, "CR%", "ATK%", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str):
        super().__init__(pos, role)
        self.lightcone = VentureForthFeixiao(role, 1)
        self.relic1 = WindSoaringYunli(role, 4)
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
        tl.append(Turn(self.name, self.role, enemyID, "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 0.5, self.scaling, 1, "FeixiaoBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "ST", ["SKL"], [self.element], [2.0, 0], [20, 0], 0.5, self.scaling, -1, "FeixiaoSkill"))
        tl.append(Turn(self.name, self.role, enemyID, "ST", ["SKL"], [self.element], [1.1, 0], [5, 0], 0.5, self.scaling, 0, "FeixiaoSkillFUA"))
        bl.append(Buff("FeixiaoBuffDMG", "DMG%", 0.6, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        for _ in range(6):
            tl.append(Turn(self.name, self.role, enemyID, "ST", ["ULT", "FUA"], [self.element], [0.9, 0], [10, 0], 0, self.scaling, 0, "FeixiaoUlt"))
        tl.append(Turn(self.name, self.role, enemyID, "ST", ["ULT", "FUA"], [self.element], [1.6, 0], [0, 0], 0, self.scaling, 0, "FeixiaoUltFinal"))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        if self.fuaTrigger:
            self.fuaTrigger = False
            tl.append(Turn(self.name, self.role, enemyID, "ST", ["SKL"], [self.element], [1.1, 0], [5, 0], 0.5, self.scaling, 1, "FeixiaoFUA"))
            bl.append(Buff("FeixiaoBuffDMG", "DMG%", 0.6, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn, result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveType != "NA" and turn.moveName not in bonusDMG:
            logger.critical("ALERT: Feixiao gained 0.5 stacks of FA")
            self.currEnergy = self.currEnergy + 0.5
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.fuaTrigger = True
        return super().takeTurn()
    
    def special(self):
        self.hasSpecial = False
        return "FeixiaoStartFUA"
    
    def handleSpecial(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecial(specialRes)
        tl.append(Turn(self.name, self.role, -1, "ST", ["FUA"], [self.element], [1.1, 0], [5, 0], 0.5, self.scaling, 0, "FeixiaoStartFUA"))
        return bl, dbl, al, dl, tl
    
    
    