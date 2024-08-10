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
    baseHP = 0
    baseATK = 0
    baseDEF = 0
    baseSPD = 100
    
    # Equipment
    lightcone = Lightcone(1)
    relic1 = Relic(4)
    relic2 = None
    planar = Planar()
    
    def __init__(self, pos: int) -> None:
        self.pos = pos
    
    def __str__(self) -> str:
        res = f"{self.name} | {self.path} | {self.element} | Pos:{self.pos}\n"
        res += f"{self.lightcone}\n"
        res += f"{self.relic1}" + (f"| {self.relic2}\n" if self.relic2 != None else "\n")
        res += f"{self.planar}"
        return res
        
    def equip(self): # function to add base buffs to wearer
        buff_lst = []
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.equip()
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
            
        return buff_lst, debuff_lst
    
    def useSkl(self):
        return self.parseEquipment("BASIC"), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0])
    
    def useBsc(self):
        return self.parseEquipment("SKILL"), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0])
    
    def useUlt(self):
        return self.parseEquipment("ULT"), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0])
        
    def useFua(self):
        return self.parseEquipment("FUA"), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0])
        
    def useHit(self):
        return self.parseEquipment("HIT"), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0])
    
    def allyTurn(self, turn, result):
        return self.parseEquipment("ALLY", turn, result), Turn(self.role, -1, "NA", [], [self.element], [0, 0], [0, 0])
        
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
            elif actionType == "HIT":
                buffs, debuffs, advs, spds = equipment.useHit()    
            elif actionType == "ALLY":
                buffs, debuffs, advs, spds = equipment.allyTurn(turn, result)
                
            buffList.append(buffs)
            debuffList.append(debuffs)
            advList.append(advs)
            spdList.append(spds)
        
        return buffList, debuffList, advList, spdList
        