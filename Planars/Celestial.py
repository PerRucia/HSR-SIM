from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Celestial(Planar):
    name = "Celestial Differentiator"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self, enemyID=-1):
        bl, dbl, al, dl = super().equip(enemyID)
        bl.append(Buff("CelestialCD", Pwr.CD_PERCENT, 0.16, self.wearerRole))
        bl.append(Buff("CelestialCR", Pwr.CR_PERCENT, 0.60, self.wearerRole))
        return bl, dbl, al, dl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().ownTurn(turn, result)
        bl.append(Buff("CelestialCR", Pwr.CR_PERCENT, 0, self.wearerRole))
        return bl, dbl, al, dl