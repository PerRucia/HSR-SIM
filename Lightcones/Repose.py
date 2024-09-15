from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Result import Result
from Turn import Turn


class Repose(Lightcone):
    name = "Geniuses' Repose"
    path = Path.ERUDITION
    baseHP = 846.7
    baseATK = 476.28
    baseDEF = 396.90

    def __init__(self, wearerRole, level: int = 5, uptime = 0.5):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("ReposeATK", Pwr.ATK_PERCENT, self.level * 0.04 + 0.12, self.wearerRole))
        bl.append(Buff("ReposeCD", Pwr.CD_PERCENT, self.uptime * (self.level * 0.06 + 0.18), self.wearerRole))
        return bl, dbl, al, dl



    