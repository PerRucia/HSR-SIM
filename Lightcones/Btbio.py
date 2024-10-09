from Buff import *
from Lightcone import Lightcone
from Misc import *


class Btbio(Lightcone):
    name = "But the Battle isn't Over"
    path = Path.HARMONY
    baseHP = 1164.2
    baseATK = 529.20
    baseDEF = 463.05
    
    counter = 0

    def __init__(self, wearerRole, level=1, targetRole = Role.DPS):
        super().__init__(wearerRole, level)
        self.targetRole = targetRole
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("BtbioERR", Pwr.ERR_PERCENT, self.level * 0.02 + 0.08, self.wearerRole))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        bl.append(Buff("BtbioDMG", Pwr.DMG_PERCENT, self.level * 0.05 + 0.25, self.targetRole, [AtkType.ALL], 1, 1, self.targetRole, TickDown.END))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        self.counter += 1
        if self.counter % 2 == 1:
            bl.append(Buff("BtbioSP", Pwr.SKLPT, 1, self.wearerRole))
        return bl, dbl, al, dl
    