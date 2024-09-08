from Buff import Buff
from Misc import *
from Planar import Planar


class Talia(Planar):
    name = "Talia: Kingdom of Banditry"
    def __init__(self, wearerRole: Role, userSPD = 145):
        super().__init__(wearerRole)
        self.userSPD = userSPD
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("TaliaBE", Pwr.BE_PERCENT, 0.16, self.wearerRole))
        if self.userSPD >= 145:
            bl.append(Buff("TaliaExtraBE", Pwr.BE_PERCENT, 0.20, self.wearerRole))
        return bl, dbl, al, dl