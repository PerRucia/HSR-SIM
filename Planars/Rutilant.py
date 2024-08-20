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
        bl.append(Buff("RutilantCR", "CR%", 0.08, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("RutilantBasicDMG", "DMG%", 0.20, self.wearerRole, ["BSC"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("RutilantSkillDMG", "DMG%", 0.20, self.wearerRole, ["SKL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl