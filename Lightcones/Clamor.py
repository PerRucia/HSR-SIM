from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Result import Result
from Turn import Turn


class Clamor(Lightcone):
    name = "Make the World Clamor"
    path = Path.ERUDITION
    baseHP = 846.7
    baseATK = 476.28
    baseDEF = 396.90

    def __init__(self, wearerRole, level: int = 5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("ClamorERR", Pwr.ERR_T, self.level * 3 + 17, self.wearerRole))
        bl.append(Buff("ClamorDMG", Pwr.DMG_PERCENT, self.level * 0.08 + 0.24, self.wearerRole, [AtkType.ULT]))
        return bl, dbl, al, dl


    