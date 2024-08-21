from Lightcone import Lightcone
from Buff import Buff
from Result import Special

class BaptismFeixiao(Lightcone):
    name = "Baptism of Pure Thought"
    path = "HUN"
    baseHP = 952.6
    baseATK = 582.12
    baseDEF = 529.20

    targetDebuffs = 0
    
    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        cdBuff = self.level * 0.03 + 0.17
        buffList.append(Buff("BaptismCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        cdBuff = (self.level * 0.01 + 0.07) * self.targetDebuffs
        bl.append(Buff("BaptismDebuffCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)    
        cdBuff = (self.level * 0.01 + 0.07) * self.targetDebuffs
        bl.append(Buff("BaptismDebuffCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        cdBuff = (self.level * 0.01 + 0.07) * self.targetDebuffs
        bl.append(Buff("BaptismDebuffCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        dmgBuff = self.level * 0.06 + 0.30
        bl.append(Buff("BaptismDispDMG", "DMG%", dmgBuff, self.wearerRole, ["ALL"], 2, 1, "SELF", "END"))
        shredBuff = self.level * 0.04 + 0.20
        bl.append(Buff("BaptismDispSHRED", "SHRED", shredBuff, self.wearerRole, ["FUA"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl
    
    def specialStart(self, special: Special):
        if special.specialName == "FeixiaoStartFUA" or special.specialName == "FeixiaoCheckRobin":
            self.targetDebuffs = min(3.0, special.attr2)
        return super().specialStart(special)
    
    