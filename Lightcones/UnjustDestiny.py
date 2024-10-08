from Lightcone import Lightcone
from Buff import *
from Misc import *

class UnjustDestinyAven(Lightcone):
    name = "Inherently Unjust Destiny"
    path = Path.PRESERVATION
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 661.50

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        defBuff = self.level * 0.06 + 0.34
        buffList.append(Buff("UnjustDEF", Pwr.DEF_PERCENT, defBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        cdBuff = self.level * 0.06 + 0.34
        buffList.append(Buff("UnjustCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, [AtkType.ALL], 2, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.06 + 0.34
        bl.append(Buff("UnjustCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, [AtkType.ALL], 2, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl = super().useFua(enemyID)
        cdBuff = self.level * 0.06 + 0.34
        bl.append(Buff("UnjustCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, [AtkType.ALL], 2, 1, Role.SELF, TickDown.PERM))
        vulnDebuff = self.level * 0.015 + 0.085
        dbl.append(Debuff("UnjustVuln", self.wearerRole, Pwr.VULN, vulnDebuff, Role.ALL, [AtkType.ALL], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    
    