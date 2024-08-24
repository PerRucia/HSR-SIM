from Lightcone import Lightcone
from Buff import *
from Misc import *

class ConcertForTwo(Lightcone):
    name = "Concert for Two"
    path = Path.PRESERVATION
    baseHP = 952.6
    baseATK = 370.44
    baseDEF = 463.05

    def __init__(self, wearerRole, level=5, uptime=1):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        defBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("ConcertConeDEF", Pwr.DEF_PERCENT, defBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        dmgBuff = (self.level * 0.01 + 0.03) * 4 * self.uptime
        buffList.append(Buff("ConcertConeDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    