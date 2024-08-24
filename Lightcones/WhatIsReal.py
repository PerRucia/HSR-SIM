from Lightcone import Lightcone
from Buff import *
from Misc import *

class WhatIsReal(Lightcone):
    name = "What is Real"
    path = Path.ABUNDANCE
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        beBuff = self.level * 0.06 + 0.18
        buffList.append(Buff("WhatIsRealBE", Pwr.BE_PERCENT, beBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    