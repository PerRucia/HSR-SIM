from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Result import Result
from Turn import Turn


class Cosmos(Lightcone):
    name = "The Day the Cosmos Fell"
    path = Path.ERUDITION
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level: int = 5, imgWeak = True):
        super().__init__(wearerRole, level)
        self.imgWeak = imgWeak
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("CosmosATK", Pwr.ATK_PERCENT, self.level * 0.02 + 0.14, self.wearerRole))
        return bl, dbl, al, dl

class CosmosRappa(Cosmos):
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        if self.imgWeak:
            bl.append(Buff("CosmosCD", Pwr.CD_PERCENT, self.level * 0.05 + 0.2, self.wearerRole, turns=3, tdType=TickDown.END))
        return bl, dbl, al, dl

    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        if self.imgWeak:
            bl.append(Buff("CosmosCD", Pwr.CD_PERCENT, self.level * 0.05 + 0.2, self.wearerRole, turns=3, tdType=TickDown.END))
        return bl, dbl, al, dl


    