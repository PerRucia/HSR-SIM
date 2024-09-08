from Buff import *
from Lightcone import Lightcone
from Misc import *


class Silence(Lightcone):
    name = "Only Silence Remains"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5, uptime=0.75):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        atkBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("SilenceATK", Pwr.ATK_PERCENT, atkBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        crBuff = (self.level * 0.03 + 0.09) * self.uptime
        buffList.append(Buff("SilenceCR", Pwr.CD_PERCENT, crBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    