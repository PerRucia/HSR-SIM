from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from RelicStats import RelicStats
from Planar import Planar
from Turn import Turn
from Result import *

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
    basics = 0
    skills = 0
    ults = 0
    fuas = 0
    turn = 0
    
    # Unique Character Properties
    
    # Relic Settings
    relicStats = RelicStats(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "HP%", "HP%", "HP%", "HP%") # Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str) -> None:
        self.pos = pos
        self.role = role
        self.priority = 0
        self.currSPD = 100
    
    def __str__(self) -> str:
        res = f"{self.name} | {self.element}-{self.path} | {self.role} | POS:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self): # function to add base buffs to wearer
        return self.parseEquipment("EQUIP")
    
    def useSkl(self, enemyID=-1):
        self.skills = self.skills + 1
        return *self.parseEquipment("BASIC"), []
    
    def useBsc(self, enemyID=-1):
        self.basics = self.basics + 1
        return *self.parseEquipment("SKILL"), []
    
    def useUlt(self, enemyID=-1):
        self.ults = self.ults + 1
        return *self.parseEquipment("ULT"), []
        
    def useFua(self, enemyID=-1):
        self.fuas = self.fuas + 1
        return *self.parseEquipment("FUA"), []
        
    def useHit(self, enemyID=-1):
        return *self.parseEquipment("HIT"), []
    
    def ownTurn(self, result: Result):
        if result.atkType in self.dmgDct:
            self.dmgDct[result.atkType] = self.dmgDct[result.atkType] + result.turnDmg
        self.dmgDct["BREAK"] = self.dmgDct["BREAK"] + result.wbDmg
        self.currEnergy = self.currEnergy + result.errGain
        return *self.parseEquipment("OWN", result), []
    
    def special(self):
        return ""
    
    def handleSpecial(self, specialRes: Special):
        return self.parseEquipment("SPECIAL")
    
    def allyTurn(self, turn: Turn, result: Result):
        return *self.parseEquipment("ALLY", turn, result), []
        
    def parseEquipment(self, actionType: str, turn=None, result=None):
        buffList, debuffList, advList, delayList = [], [], [], []
        equipmentList = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipmentList.append(self.relic2)
            
        for equipment in equipmentList:
            if actionType == "BASIC":
                buffs, debuffs, advs, delays = equipment.useBsc()
            elif actionType == "SKILL":
                buffs, debuffs, advs, delays = equipment.useSkl()
            elif actionType == "ULT":
                buffs, debuffs, advs, delays = equipment.useUlt()
            elif actionType == "FUA":
                buffs, debuffs, advs, delays = equipment.useFua()
            elif actionType == "EQUIP":
                buffs, debuffs, advs, delays = equipment.equip()
            elif actionType == "HIT":
                buffs, debuffs, advs, delays = equipment.useHit()
            elif actionType == "SPECIAL":
                buffs, debuffs, advs, delays = equipment.special()
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
    
    def takeTurn(self) -> str:
        res = self.turn
        self.turn = self.turn + 1
        return self.rotation[res % len(self.rotation)]
    
    def gettotalDMG(self) -> tuple[str, float]:
        ttl = sum(self.dmgDct.values())
        res = ""
        for key, val in self.dmgDct.items():
            res += f"{key}: {val:.3f} | {val / ttl * 100:.3f}%\n"
        return res, ttl
    
    def getBaseStat(self) -> tuple[float, float, float]:
        if self.scaling == "ATK":
            baseStat = self.baseATK + self.lightcone.baseATK
        if self.scaling == "HP":
            baseStat = self.baseATK + self.lightcone.baseHP
        if self.scaling == "DEF":
            baseStat = self.baseDEF + self.lightcone.baseDEF
        return baseStat, *self.getRelicScalingStats()
    
    def standardAVred(self, av: float):
        self.currAV = max(0, self.currAV - av)
    
        