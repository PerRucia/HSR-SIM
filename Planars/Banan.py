from Buff import Buff
from Misc import *
from Planar import Planar


class Banan(Planar):
    name = "The Wondrous BananAmusement Park"
    def __init__(self, wearerRole: Role, summon = True):
        super().__init__(wearerRole)
        self.summon = summon
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("BananCD", Pwr.CD_PERCENT, 0.16, self.wearerRole))
        if self.summon:
            bl.append(Buff("BananSummonCD", Pwr.CD_PERCENT, 0.32, self.wearerRole))
        return bl, dbl, al, dl