from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Nightglow(Lightcone):
    name = "Flowing Nightglow"
    path = Path.HARMONY
    baseHP = 952.6
    baseATK = 635.04
    baseDEF = 463.05

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        err = (self.level * 0.005 + 0.025) * 5
        buffList.append(Buff("NightglowERR", Pwr.ERR_PERCENT, err, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        atk = self.level * 0.12 + 0.36
        dmg = self.level * 0.04 + 0.20
        buffList.append(Buff("NightglowATK", Pwr.ATK_PERCENT, atk, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        buffList.append(Buff("NightglowDMG", Pwr.DMG_PERCENT, dmg, Role.ALL, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList    
    