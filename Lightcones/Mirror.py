from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Delay import *

class Mirror(Lightcone):
    name = "Past Self in Mirror"
    path = Path.HARMONY
    baseHP = 1058.4
    baseATK = 529.20
    baseDEF = 529.20

    def __init__(self, wearerRole, level = 1):
        super().__init__(wearerRole, level)
    
    def equip(self, enemyID=-1):
        bl, dbl, al, dl = super().equip(enemyID)
        be = self.level * 0.1 + 0.5
        bl.append(Buff("MirrorBE", Pwr.BE_PERCENT, be, self.wearerRole))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        dmg = self.level * 0.04 + 0.2
        bl.append(Buff("MirrorDMG", Pwr.DMG_PERCENT, dmg, Role.ALL, turns=3, tdType=TickDown.END))
        bl.append(Buff("MirrorSP", Pwr.SKLPT, 1, self.wearerRole))
        return bl, dbl, al, dl