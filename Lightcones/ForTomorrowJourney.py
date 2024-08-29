from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Journey(Lightcone):
    name = "For Tomorrow's Journey"
    path = Path.HARMONY
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        atkBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("JourneyATK", Pwr.ATK_PERCENT, atkBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        dmgBuff = self.level * 0.03 + 0.15
        buffList.append(Buff("JourneyUltDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList    
    