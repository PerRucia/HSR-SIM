from Lightcone import Lightcone
from Buff import *

class ConcertForTwo(Lightcone):
    name = "Concert for Two"
    path = "PRE"
    baseHP = 952.6
    baseATK = 370.44
    baseDEF = 463.05

    def __init__(self, wearerRole, level, uptime=1):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        defBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("ConcertConeDEF", "DEF%", defBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        dmgBuff = (self.level * 0.01 + 0.03) * 4 * self.uptime
        buffList.append(Buff("ConcertConeDMG", "DMG%", dmgBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    
    