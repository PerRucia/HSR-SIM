from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Belobog(Planar):
    name = "Belobog of the Architects"
    def __init__(self, wearerRole: str, userEHR = 0.50):
        super().__init__(wearerRole)
        self.userEHR = userEHR
        
    def equip(self, enemyID=-1):
        bl, dbl, al, dl = super().equip(enemyID)
        bl.append(Buff("BelobogDEF", Pwr.DEF_PERCENT, 0.15, self.wearerRole))
        if self.userEHR >= 0.5:
            bl.append(Buff("BelobogExtraDEF", Pwr.DEF_PERCENT, 0.15, self.wearerRole))
        return bl, dbl, al, dl