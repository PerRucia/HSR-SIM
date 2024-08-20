from Lightcone import Lightcone
from Buff import *
from Delay import *

class ResolutionPela(Lightcone):
    name = "Resolution Shines as Pearls of Sweat"
    path = "NIH"
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def useBsc(self, enemyID):
        bl, dbl, al, dl = super().useBsc(enemyID)
        shredBuff = self.level * 0.01 + 0.11
        dbl.append(Debuff("ResoShred", self.wearerRole, "SHRED", shredBuff, enemyID, ["ALL"], 1, 1, False, False))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID):
        bl, dbl, al, dl = super().useSkl(enemyID)
        shredBuff = self.level * 0.01 + 0.11
        dbl.append(Debuff("ResoShred", self.wearerRole, "SHRED", shredBuff, enemyID, ["ALL"], 1, 1, False, False))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        shredBuff = self.level * 0.01 + 0.11
        dbl.append(Debuff("ResoShred", self.wearerRole, "SHRED", shredBuff, "ALL", ["ALL"], 1, 1, False, False))
        return bl, dbl, al, dl
    