from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class SSS(Planar):
    name = "Space Sealing Station"

    def __init__(self, wearerRole: str, wearerSPD: int = 120):
        super().__init__(wearerRole)
        self.wearerSPD = wearerSPD
        
    def equip(self):
        bl, dbl, al, dl, = super().equip()
        if self.wearerSPD >= 120:
            bl.append(Buff("SSSATK", Pwr.ATK_PERCENT, 0.24, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        else:
            bl.append(Buff("SSSATK", Pwr.ATK_PERCENT, 0.12, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl