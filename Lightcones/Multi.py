from Lightcone import Lightcone
from Buff import Buff
from Delay import *
from Misc import *

class Multi(Lightcone):
    name = "Multiplication"
    path = Path.ABUNDANCE
    baseHP = 952.6
    baseATK = 317.52
    baseDEF = 198.45

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def useBsc(self, enemyID):
        bl, dbl, al, dl = super().useBsc(enemyID)
        advAmount = self.level * 0.02 + 0.10
        al.append(Advance("MultiplicationADV", self.wearerRole, advAmount))
        return bl, dbl, al, dl
    
    