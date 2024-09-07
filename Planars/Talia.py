from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Talia(Planar):
    name = "Talia: Kingdom of Banditry"
    def __init__(self, wearerRole: str, userSPD = 145):
        super().__init__(wearerRole)
        self.userSPD = userSPD
        
    def equip(self, enemyID=-1):
        bl, dbl, al, dl = super().equip(enemyID)
        bl.append(Buff("TaliaBE", Pwr.BE_PERCENT, 0.16, self.wearerRole))
        if self.userSPD >= 145:
            bl.append(Buff("TaliaExtraBE", Pwr.BE_PERCENT, 0.20, self.wearerRole))
        return bl, dbl, al, dl