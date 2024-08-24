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
        buffList.append(Buff("SunsetCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        dmgBuff = self.level * 0.06 + 0.3
        buffList.append(Buff("SunsetDMG", "DMG%", dmgBuff, self.wearerRole, ["ULT", "FUA"], 2, 2, Role.SELF, "END"))
        return buffList, debuffList, advList, delayList
    
    