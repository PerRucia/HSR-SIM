from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class VentureForth(Lightcone):
    name = "I Venture Forth to Hunt"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 635.04
    baseDEF = 463.05

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.025 + 0.125
        buffList.append(Buff("VentureCR", Pwr.CR_PERCENT, crBuff, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useFua(self, enemyID):
        bl, dbl, al, dl = super().useFua(enemyID)
        shredBuff = self.level * 0.03 + 0.24
        bl.append(Buff("VentureSHRED", Pwr.SHRED, shredBuff, self.wearerRole, [Move.ULT], 2, 2, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
    
class VentureForthFeixiao(VentureForth):
    name = "I Venture Forth to Hunt"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 635.04
    baseDEF = 463.05

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        shredBuff = self.level * 0.03 + 0.24
        bl.append(Buff("VentureSHRED", Pwr.SHRED, shredBuff, self.wearerRole, [Move.ALL], 2, 2, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        shredBuff = self.level * 0.03 + 0.24
        bl.append(Buff("VentureSHRED", Pwr.SHRED, shredBuff, self.wearerRole, [Move.ULT], 2, 2, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
    
    
    