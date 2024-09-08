from Buff import Buff
from Misc import *
from Planar import Planar


class PanCosmic(Planar):
    name = "Pan-Cosmic Commercial Enterprise"
    def __init__(self, wearerRole: Role):
        super().__init__(wearerRole)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("PanCosmicEHR", Pwr.EHR_PERCENT, 0.10, self.wearerRole))
        return bl, dbl, al, dl