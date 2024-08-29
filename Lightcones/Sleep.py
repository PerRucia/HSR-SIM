from Lightcone import Lightcone
from Buff import *
from Result import Result
from Misc import *

class Sleep(Lightcone):
    name = "Sleep like the Dead"
    path = Path.HUNT
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        cdBuff = self.level * 0.05 + 0.25
        buffList.append(Buff("SleepCD", Pwr.DMG_PERCENT, cdBuff, self.wearerRole, [AtkType.BSC, AtkType.SKL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    