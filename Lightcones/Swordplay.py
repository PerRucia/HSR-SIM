from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Swordplay(Lightcone):
    name = "Swordplay"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBuff = (self.level * 0.02 + 0.06) * 5
        buffList.append(Buff("SwordplayDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList

    

    