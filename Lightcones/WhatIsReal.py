from Lightcone import Lightcone
from Buff import *

class WhatIsReal(Lightcone):
    name = "What is Real"
    path = "ABU"
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 330.75

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)

    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        beBuff = self.level * 0.06 + 0.18
        buffList.append(Buff("WhatIsRealBE", "BE%", beBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    
    