from Lightcone import Lightcone
from Buff import *

class UnjustDestinyAven(Lightcone):
    name = "Inherently Unjust Destiny"
    path = "PRE"
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 661.50

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        defBuff = self.level * 0.06 + 0.34
        buffList.append(Buff("UnjustDEF", "DEF%", defBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        cdBuff = self.level * 0.06 + 0.34
        buffList.append(Buff("UnjustCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 2, 1, "SELF", "END"))
        return buffList, debuffList, advList, delayList
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.06 + 0.34
        bl.append(Buff("UnjustCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl = super().useFua(enemyID)
        cdBuff = self.level * 0.06 + 0.34
        bl.append(Buff("UnjustCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 2, 1, "SELF", "END"))
        vulnDebuff = self.level * 0.015 + 0.085
        dbl.append(Debuff("UnjustVuln", self.wearerRole, "VULN", vulnDebuff, "ALL", ["ALL"], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    
    