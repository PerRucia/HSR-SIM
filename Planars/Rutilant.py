from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Rutilant(Planar):
    name = "Rutilant Arena"

    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("RutilantCR", Pwr.CR_PERCENT, 0.08, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RutilantBonusDMG", Pwr.DMG_PERCENT, 0.20, self.wearerRole, [AtkType.BSC, AtkType.SKL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl