from Lightcone import Lightcone
from Buff import *
from Result import Result
from Misc import *

class Breakfast(Lightcone):
    name = "The Seriousness of Breakfast"
    path = Path.ERUDTION
    baseHP = 846.7
    baseATK = 476.28
    baseDEF = 396.90

    def __init__(self, wearerRole, level=5, uptime=0.5):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBuff = self.level * 0.03 + 0.09
        buffList.append(Buff("BreakfastDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        atkBuff = (self.level * 0.01 + 0.03) * 3 * self.uptime
        buffList.append(Buff("BreakfastATK", Pwr.ATK_PERCENT, atkBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    