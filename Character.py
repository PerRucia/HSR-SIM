from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from RelicStats import RelicStats
from Planar import Planar
from Turn import Turn

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
    
    # Unique Character Properties
    
    # Relic Settings
    relicStats = RelicStats(4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, "HP%", "HP%", "HP%", "HP%")
    
    def __init__(self, pos: int, role: str) -> None:
        self.pos = pos
        self.role = role
        self.currSPD = 0
        
    
    def __str__(self) -> str:
        res = f"{self.name} | {self.element}-{self.path} | POS:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self): # function to add base buffs to wearer
        return self.parseEquipment("EQUIP")
    
    def useSkl(self, enemyID=-1):
        return *self.parseEquipment("BASIC"), Turn(self.name, self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 30, self.scaling)
    
    def useBsc(self, enemyID=-1):
        return *self.parseEquipment("SKILL"), Turn(self.name, self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 20, self.scaling)
    
    def useUlt(self, enemyID=-1):
        return *self.parseEquipment("ULT"), Turn(self.name, self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling)
        
    def useFua(self, enemyID=-1):
        return *self.parseEquipment("FUA"), Turn(self.name, self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling)
        
    def useHit(self, enemyID=-1):
        return *self.parseEquipment("HIT"), Turn(self.name, self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 0, self.scaling)
    
    def allyTurn(self, turn, result):
        return *self.parseEquipment("ALLY", turn, result), Turn(self.name, self.role, -1, "NA", [], [self.element], [0, 0], [0, 0], 0, self.scaling)
        
    def parseEquipment(self, actionType: str, turn=None, result=None):
        buffList, debuffList, advList = [], [], []
        equipmentList = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipmentList.append(self.relic2)
            
        for equipment in equipmentList:
            if actionType == "BASIC":
                buffs, debuffs, advs = equipment.useBsc()
            elif actionType == "SKILL":
                buffs, debuffs, advs = equipment.useSkl()
            elif actionType == "ULT":
                buffs, debuffs, advs = equipment.useUlt()
            elif actionType == "FUA":
                buffs, debuffs, advs = equipment.useFua()
            elif actionType == "EQUIP":
                buffs, debuffs, advs = equipment.equip()
            elif actionType == "HIT":
                buffs, debuffs, advs = equipment.useHit()    
            elif actionType == "ALLY":
                buffs, debuffs, advs = equipment.allyTurn(turn, result)
                
            buffList.extend(buffs)
            debuffList.extend(debuffs)
            advList.extend(advs)
        return buffList, debuffList, advList
    
    def addEnergy(self, amount: float):
        self.currEnergy = min(self.maxEnergy, self.currEnergy + amount)
        
    def advanceAV(self, adjPercent: float, currSPD: float):
        avAdjustment = (10000 / currSPD) * adjPercent
        self.currAV = max(0, self.currAV - avAdjustment)
        
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0, self.currAV - reduceValue)
        
    def getRelicScalingStats(self) -> tuple[float, float]:
        return self.relicStats.getScalingValue(self.scaling)
    
    def getSPD(self) -> float:
        return self.relicStats.getSPD()
    
    def canUseUlt(self) -> bool:
        return self.currEnergy >= self.ultCost