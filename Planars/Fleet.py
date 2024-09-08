from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Fleet(Planar):
    name = "Fleet of the Ageless"
    def __init__(self, wearerRole: str, userSPD = 120):
        super().__init__(wearerRole)
        self.userSPD = userSPD
        
    def equip(self):
        bl, dbl, al, dl = super().equip(enemyID)
        bl.append(Buff("FleetHP", Pwr.HP_PERCENT, 0.12, self.wearerRole))
        if self.userSPD >= 120:
            bl.append(Buff("FleetATK", Pwr.ATK_PERCENT, 0.08, Role.ALL))
        return bl, dbl, al, dl