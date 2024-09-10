from Delay import *
from Lightcone import Lightcone
from Misc import *
from Buff import *


class Passkey(Lightcone):
    name = "Passkey"
    path = Path.ERUDITION
    baseHP = 740.9
    baseATK = 370.44
    baseDEF = 264.60

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        bl.append(Buff("PasskeyERR", Pwr.ERR_T, self.level * 1 + 7, self.wearerRole))
        return bl, dbl, al, dl
    
    