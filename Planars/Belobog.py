from Buff import Buff
from Misc import *
from Planar import Planar


class Belobog(Planar):
    name = "Belobog of the Architects"
    def __init__(self, wearerRole: Role, userEHR = 0.50):
        super().__init__(wearerRole)
        self.userEHR = userEHR
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("BelobogDEF", Pwr.DEF_PERCENT, 0.15, self.wearerRole))
        if self.userEHR >= 0.5:
            bl.append(Buff("BelobogExtraDEF", Pwr.DEF_PERCENT, 0.15, self.wearerRole))
        return bl, dbl, al, dl