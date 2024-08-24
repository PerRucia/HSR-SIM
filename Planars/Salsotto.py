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
        bl.append(Buff("SalsottoCR", "CR%", 0.08, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("SalsottoDMG", "DMG%", 0.15, self.wearerRole, ["ULT", "FUA"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl