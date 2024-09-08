from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Banan(Planar):
    name = "The Wondrous BananAmousement Park"
    def __init__(self, wearerRole: str, summon = True):
        super().__init__(wearerRole)
        self.summon = summon
        
    def equip(self):
        bl, dbl, al, dl = super().equip(enemyID)
        bl.append(Buff("BananCD", Pwr.CD_PERCENT, 0.16, self.wearerRole))
        if self.summon:
            bl.append(Buff("BananSummonCD", Pwr.CD_PERCENT, 0.32, self.wearerRole))
        return bl, dbl, al, dl