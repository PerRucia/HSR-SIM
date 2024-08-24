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
        bl.append(Buff("RutilantCR", "CR%", 0.08, self.wearerRole, ["ALL"], 1, 1, Role.SELF, "PERM"))
        bl.append(Buff("RutilantBonusDMG", "DMG%", 0.20, self.wearerRole, ["BSC", "SKL"], 1, 1, Role.SELF, "PERM"))
        return bl, dbl, al, dl