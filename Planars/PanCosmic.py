from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class PanCosmic(Planar):
    name = "Pan-Cosmic Commericla Enterprise"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        bl, dbl, al, dl = super().equip(enemyID)
        bl.append(Buff("PanCosmicEHR", Pwr.EHR_PERCENT, 0.10, self.wearerRole))
        return bl, dbl, al, dl