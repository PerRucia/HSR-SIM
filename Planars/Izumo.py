from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Izumo(Planar):
    name = "Izumo Gensei and Takama Divine Realm"

    def __init__(self, wearerRole: str, sharedPath: bool = True):
        super().__init__(wearerRole)
        self.sharedPath = sharedPath
        
    def equip(self):
        bl, dbl, al, dl, = super().equip()
        bl.append(Buff("IzumoATK", Pwr.ATK_PERCENT, 0.12, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.sharedPath:
            bl.append(Buff("IzumoCR", Pwr.CR_PERCENT, 0.12, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl