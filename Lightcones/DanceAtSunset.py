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
        buffList.append(Buff("SunsetCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        dmgBuff = self.level * 0.06 + 0.3
        buffList.append(Buff("SunsetDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [Move.ULT, "FUA"], 2, 2, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList
    
    