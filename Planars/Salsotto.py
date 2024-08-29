from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Salsotto(Planar):
    name = "Inert Salsotto"

    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        bl, dbl, al, dl, = super().equip()
        bl.append(Buff("SalsottoCR", Pwr.CR_PERCENT, 0.08, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("SalsottoDMG", Pwr.DMG_PERCENT, 0.15, self.wearerRole, [AtkType.ULT, AtkType.FUA], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl