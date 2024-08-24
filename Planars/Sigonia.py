from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Sigonia(Planar):
    name = "Sigonia, the Unclaimed Desolation"

    def __init__(self, wearerRole: str, uptime: float = 0.5):
        super().__init__(wearerRole)
        self.uptime = uptime
        
    def equip(self):
        bl, dbl, al, dl, = super().equip()
        bl.append(Buff("SigoniaCR", Pwr.CR_PERCENT, 0.04, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("SigoniaCD", Pwr.CD_PERCENT, 0.40 * self.uptime, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl