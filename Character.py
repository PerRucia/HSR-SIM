from Buff import *
from Lightcone import Lightcone
from Relic import Relic
from Planar import Planar

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
        buff_lst = []
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.useSkl()
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
        return buff_lst, debuff_lst
    
    def useBsc(self):
        buff_lst = []
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.useBsc()
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
        return buff_lst, debuff_lst
    
    def useUlt(self):
        buff_lst = []
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.useUlt()
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
        return buff_lst, debuff_lst
    
    def useFua(self):
        buff_lst = []
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.useFua()
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
        return buff_lst, debuff_lst
    
    def useHit(self):
        buff_lst = []
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.useHit()
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
        return buff_lst, debuff_lst
    
    def allyTurn(self, turn):
        buff_lst = [] 
        debuff_lst = []
        
        equipment_list = [self.lightcone, self.relic1, self.planar]
        if self.relic2:
            equipment_list.append(self.relic2)
        
        for equipment in equipment_list:
            buffs, debuffs = equipment.allyTurn(turn)
            buff_lst.extend(buffs)
            debuff_lst.extend(debuffs)
        return buff_lst, debuff_lst