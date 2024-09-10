from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Ninjitsu(Lightcone):
    name = "Ninjitsu Inscription: Dazzling Evilbreaker"
    path = Path.ERUDITION
    baseHP = 952.6
    baseATK = 582.12
    baseDEF = 529.20

    raiton = False
    raitonCount = 0

    def __init__(self, wearerRole, level: int = 1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("NinjitsuBE", Pwr.BE_PERCENT, self.level * 0.10 + 0.5, self.wearerRole))
        bl.append(Buff("NinjitsuERR", Pwr.ERR_T, self.level * 2.5 + 27.5, self.wearerRole))
        return bl, dbl, al, dl

    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        if self.raiton:
            self.raitonCount -= 1
            if self.raitonCount == 0:
                self.raiton = False
                al.append(Advance("NinjitsuADV", self.wearerRole, self.level * 0.05 + 0.45))
        return bl, dbl, al, dl

    def useUlt(self, enemyID=-1):
        self.raiton = True
        self.raitonCount = 2
        return super().useUlt(enemyID)

    

    