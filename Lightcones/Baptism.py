from Lightcone import Lightcone
from Buff import Buff
from Result import Special
from Misc import *

class BaptismFeixiao(Lightcone):
    name = "Baptism of Pure Thought"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 582.12
    baseDEF = 529.20

    targetDebuffs = 0
    
    def __init__(self, wearerRole, level = 1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        cdBuff = self.level * 0.03 + 0.17
        buffList.append(Buff("BaptismCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        cdBuff = (self.level * 0.01 + 0.07) * self.targetDebuffs
        bl.append(Buff("BaptismDebuffCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)    
        cdBuff = (self.level * 0.01 + 0.07) * self.targetDebuffs
        bl.append(Buff("BaptismDebuffCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        cdBuff = (self.level * 0.01 + 0.07) * self.targetDebuffs
        bl.append(Buff("BaptismDebuffCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        dmgBuff = self.level * 0.06 + 0.30
        bl.append(Buff("BaptismDispDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, ["ALL"], 2, 1, Role.SELF, TickDown.END))
        shredBuff = self.level * 0.04 + 0.20
        bl.append(Buff("BaptismDispSHRED", Pwr.SHRED, shredBuff, self.wearerRole, ["FUA"], 2, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
    
    def specialStart(self, special: Special):
        if special.specialName == "Feixiao" or special.specialName == "FeixiaoTech":
            self.targetDebuffs = min(3.0, special.attr3)
        return super().specialStart(special)
    
    