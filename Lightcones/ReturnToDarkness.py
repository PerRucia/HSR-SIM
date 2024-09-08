from Buff import *
from Lightcone import Lightcone
from Misc import *


class ReturnToDarkness(Lightcone):
    name = "Return to Darkness"
    path = Path.HUNT
    baseHP = 846.7
    baseATK = 529.20
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.03 + 0.09
        buffList.append(Buff("DarknessCR", Pwr.CR_PERCENT, crBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    