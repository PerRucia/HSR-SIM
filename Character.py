from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from RelicStats import RelicStats
from Planar import Planar
from Turn import Turn
from Result import *
from Misc import *
import logging

logger = logging.getLogger(__name__)

class Character:
    # Standard Character Properties
    name = "Character"
    path = "PATH"
    element = "ELE"
    scaling = "ATK"
    baseHP = 0
    baseATK = 0
    baseDEF = 0
    baseSPD = 100
    maxEnergy = 100
    ultCost = 100
    currEnergy = maxEnergy / 2
    currAV = 100.0
    rotation = ["E", "A", "A"]
    dmgDct = {"BSC": 0, "SKL": 0, "ULT": 0, "BREAK": 0}
    hasSpecial = False
    hasSummon = False
    specialEnergy = False
    basics = 0
    skills = 0
    ults = 0
    fuas = 0
    turn = 0
    
    # Unique Character Properties
    
    # Relic Settings
    
    def __init__(self, pos: int, role: str, defaultTarget: int) -> None:
        self.pos = pos
        self.role = role
        self.priority = 0
        self.currSPD = 100
        self.defaultTarget = defaultTarget
        
    def __str__(self) -> str:
        res = f"{self.name} | {self.element.name}-{self.path.name} | {self.role.name} | POS:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self): # function to add base buffs to wearer
        return self.parseEquipment("EQUIP")
    
    def useSkl(self, enemyID=-1):
        self.skills = self.skills + 1
        return *self.parseEquipment("BASIC", enemyID=enemyID), []
    
    def useBsc(self, enemyID=-1):
        self.basics = self.basics + 1
        return *self.parseEquipment("SKILL", enemyID=enemyID), []
    
    def useUlt(self, enemyID=-1):
        self.ults = self.ults + 1
        return *self.parseEquipment("ULT", enemyID=enemyID), []
        
    def useFua(self, enemyID=-1):
        self.fuas = self.fuas + 1
        return *self.parseEquipment("FUA", enemyID=enemyID), []
        
    def useHit(self, enemyID=-1):
        return *self.parseEquipment("HIT", enemyID=enemyID), []
    
    def ownTurn(self, result: Result):
        if result.atkType in self.dmgDct:
            self.dmgDct[result.atkType] = self.dmgDct[result.atkType] + result.turnDmg
        self.dmgDct["BREAK"] = self.dmgDct["BREAK"] + result.wbDmg
        self.currEnergy = min(self.maxEnergy, self.currEnergy + result.errGain)
        return *self.parseEquipment("OWN", result=result), []
    
    def special(self):
        return ""
    
    def handleSpecialStart(self, specialRes: Special):
        return *self.parseEquipment("SPECIALS", special=specialRes), []
    
    def handleSpecialMiddle(self, specialRes: Special):
        return *self.parseEquipment("SPECIALM", special=specialRes), []
    
    def handleSpecialEnd(self, specialRes: Special):
        return *self.parseEquipment("SPECIALE", special=specialRes), []
    
    def allyTurn(self, turn: Turn, result: Result):
        return *self.parseEquipment("ALLY", turn=turn, result=result), []
        
    def parseEquipment(self, actionType: str, turn=None, result=None, special=None, enemyID=-1):
        buffList, debuffList, advList, delayList = [], [], [], []
        equipmentList = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipmentList.append(self.relic2)
            
        for equipment in equipmentList:
            if actionType == "BASIC":
                buffs, debuffs, advs, delays = equipment.useBsc(enemyID)
            elif actionType == "SKILL":
                buffs, debuffs, advs, delays = equipment.useSkl(enemyID)
            elif actionType == "ULT":
                buffs, debuffs, advs, delays = equipment.useUlt(enemyID)
            elif actionType == "FUA":
                buffs, debuffs, advs, delays = equipment.useFua(enemyID)
            elif actionType == "EQUIP":
                buffs, debuffs, advs, delays = equipment.equip()
            elif actionType == "HIT":
                buffs, debuffs, advs, delays = equipment.useHit(enemyID)
            elif actionType == "SPECIALS":
                buffs, debuffs, advs, delays = equipment.specialStart(special)
            elif actionType == "SPECIALM":
                buffs, debuffs, advs, delays = equipment.specialMiddle(special)
            elif actionType == "SPECIALE":
                buffs, debuffs, advs, delays = equipment.specialEnd(special)
            elif actionType == "OWN":
                buffs, debuffs, advs, delays = equipment.ownTurn(result)    
            elif actionType == "ALLY":
                buffs, debuffs, advs, delays = equipment.allyTurn(turn, result)
                
            buffList.extend(buffs)
            debuffList.extend(debuffs)
            advList.extend(advs)
            delayList.extend(delays)
        return buffList, debuffList, advList, delayList
    
    def addEnergy(self, amount: float):
        self.currEnergy = min(self.maxEnergy, self.currEnergy + amount)
        
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0, self.currAV - reduceValue)
        
    def getRelicScalingStats(self) -> tuple[float, float]:
        return self.relicStats.getScalingValue(self.scaling)
    
    def getSPD(self) -> float:
        return self.relicStats.getSPD()
    
    def canUseUlt(self) -> bool:
        return self.currEnergy >= self.ultCost
    
    def isChar(self) -> bool:
        return True
    
    def isSummon(self) -> bool:
        return False
    
    def takeTurn(self) -> str:
        res = self.turn
        self.turn = self.turn + 1
        return self.rotation[res % len(self.rotation)]
    
    def gettotalDMG(self) -> tuple[str, float]:
        ttl = sum(self.dmgDct.values())
        res = ""
        for key, val in self.dmgDct.items():
            res += f"-{key}: {val:.3f} | {val / ttl * 100 if ttl > 0 else 0:.3f}%\n"
        return res, ttl
    
    def getBaseStat(self) -> tuple[float, float, float]:
        if self.scaling == Scaling.ATK:
            baseStat = self.baseATK + self.lightcone.baseATK
        if self.scaling == Scaling.HP:
            baseStat = self.baseATK + self.lightcone.baseHP
        if self.scaling == Scaling.DEF:
            baseStat = self.baseDEF + self.lightcone.baseDEF
        return baseStat, *self.getRelicScalingStats()
    
    def standardAVred(self, av: float):
        self.currAV = max(0, self.currAV - av)
        
    def getTargetID(self, enemyID: int):
        if enemyID == -1:
            return self.defaultTarget
        return enemyID
    
        
    
        