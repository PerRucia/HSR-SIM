from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Delay import *

class Night(Lightcone):
    name = "Night of Fright"
    path = Path.ABUNDANCE
    baseHP = 1164.2
    baseATK = 476.28
    baseDEF = 529.20

    def __init__(self, wearerRole, level = 5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        bl, dbl, al, dl = super().equip(enemyID)
        err = self.level * 0.02 + 0.10
        bl.append(Buff("NightERR", Pwr.ERR_PERCENT, err, self.wearerRole))
        return bl, dbl, al, dl
    
class NightHuoHuo(Night):
    def __init__(self, wearerRole, level = 5, uptime = 1.0):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        bl, dbl, al, dl = super().equip(enemyID)
        atk = (self.level * 0.02 + 0.10) * self.uptime
        bl.append(Buff("NightATK", Pwr.ERR_PERCENT, atk, self.wearerRole))
        return bl, dbl, al, dl