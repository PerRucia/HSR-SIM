from Lightcone import Lightcone
from Buff import *
from Result import Result

class ReturnToDarkness(Lightcone):
    name = "Return to Darkness"
    path = "HUN"
    baseHP = 846.7
    baseATK = 529.20
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.03 + 0.09
        buffList.append(Buff("DarknessCR", "CR%", crBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    
    