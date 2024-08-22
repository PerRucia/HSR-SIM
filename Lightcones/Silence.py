from Lightcone import Lightcone
from Buff import *
from Result import Result

class Silence(Lightcone):
    name = "Only Silence Remains"
    path = "HUN"
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5, uptime=0.75):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        atkBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("SilenceATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        crBuff = (self.level * 0.03 + 0.09) * self.uptime
        buffList.append(Buff("SilenceCR", "CD%", crBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    
    