from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from Planar import Planar
from Turn import Turn

class Character:
    # Basic Stats
    name = "Character"
    path = "PATH"
    element = "ELE"
    role = "DPS" # DPS/SDPS/SUS/SUP
    scaling = "ATK"
    baseHP = 0
    baseATK = 0
    baseDEF = 0
    baseSPD = 100
    maxEnergy = 100
    currEnergy = maxEnergy / 2
    
    def __init__(self, pos: int) -> None:
        self.pos = pos
        
    
    def __str__(self) -> str:
        res = f"{self.name} | {self.path} | {self.element} | Pos:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self): # function to add base buffs to wearer
        return self.parseEquipment("EQUIP")
    
    def useSkl(self, enemyID=-1):
        return *self.parseEquipment("BASIC"), Turn(self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 30, self.scaling)
    
    def useBsc(self, enemyID=-1):
        return *self.parseEquipment("SKILL"), Turn(self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 20, self.scaling)
    
    def useUlt(self, enemyID=-1):
        return *self.parseEquipment("ULT"), Turn(self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling)
        
    def useFua(self, enemyID=-1):
        return *self.parseEquipment("FUA"), Turn(self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling)
        
    def useHit(self, enemyID=-1):
        return *self.parseEquipment("HIT"), Turn(self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 0, self.scaling)
    
    def allyTurn(self, turn, result):
        return *self.parseEquipment("ALLY", turn, result), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0], 0, self.scaling)
        
    def parseEquipment(self, actionType: str, turn=None, result=None):
        buffList, debuffList, advList, spdList = [], [], [], []
        equipmentList = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipmentList.append(self.relic2)
            
        for equipment in equipmentList:
            if actionType == "BASIC":
                buffs, debuffs, advs, spds = equipment.useBsc()
            elif actionType == "SKILL":
                buffs, debuffs, advs, spds = equipment.useSkl()
            elif actionType == "ULT":
                buffs, debuffs, advs, spds = equipment.useUlt()
            elif actionType == "FUA":
                buffs, debuffs, advs, spds = equipment.useFua()
            elif actionType == "EQUIP":
                buffs, debuffs, advs, spds = equipment.equip()
            elif actionType == "HIT":
                buffs, debuffs, advs, spds = equipment.useHit()    
            elif actionType == "ALLY":
                buffs, debuffs, advs, spds = equipment.allyTurn(turn, result)
                
            buffList.extend(buffs)
            debuffList.extend(debuffs)
            advList.extend(advs)
            spdList.extend(spds)
        return buffList, debuffList, advList, spdList
    
    def addEnergy(self, amount: float):
        self.currEnergy = min(self.maxEnergy, self.currEnergy + amount)
        