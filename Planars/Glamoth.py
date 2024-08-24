from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Glamoth(Planar):
    name = "Firmament Frontline: Glamoth"

    def __init__(self, wearerRole: str, wearerSPD: int = 120):
        super().__init__(wearerRole)
        self.wearerSPD = wearerSPD
        
    def equip(self):
        bl, dbl, al, dl, = super().equip()
        bl.append(Buff("GlamothATK", Pwr.ATK_PERCENT, 0.24, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        if self.wearerSPD >= 160:
            bl.append(Buff("GlamothDMG", Pwr.DMG_PERCENT, 0.18, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        elif self.wearerSPD >= 135:
            bl.append(Buff("GlamothDMG", Pwr.DMG_PERCENT, 0.12, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl