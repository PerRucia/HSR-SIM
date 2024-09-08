from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Sunset(Lightcone):
    name = "Dance at Sunset"
    path = Path.DESTRUCTION
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level = 1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        cdBuff = self.level * 0.06 + 0.3
        buffList.append(Buff("SunsetCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID=-1):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        dmgBuff = self.level * 0.06 + 0.3
        buffList.append(Buff("SunsetDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [AtkType.ULT, AtkType.FUA], 2, 2, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList
    
    