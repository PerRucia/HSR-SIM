from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Result import Result
from Turn import Turn


class Charmony(Lightcone):
    name = "After the Charmony Fall"
    path = Path.ERUDITION
    baseHP = 846.7
    baseATK = 476.28
    baseDEF = 396.90

    def __init__(self, wearerRole, level: int = 5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("CharmonyBE", Pwr.BE_PERCENT, self.level * 0.07 + 0.21, self.wearerRole))
        return bl, dbl, al, dl

    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        bl.append(Buff("CharmonySPD", Pwr.SPD_PERCENT, self.level * 0.02 + 0.06, self.wearerRole, turns=2, tdType=TickDown.END))
        return bl, dbl, al, dl

    