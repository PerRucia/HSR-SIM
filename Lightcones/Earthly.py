from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Delay import *

class Earthly(Lightcone):
    name = "Earthly Escapade"
    path = Path.HARMONY
    baseHP = 1164.2
    baseATK = 529.20
    baseDEF = 463.05

    def __init__(self, wearerRole, level = 1):
        super().__init__(wearerRole, level)
    
    def equip(self, enemyID=-1):
        bl, dbl, al, dl = super().equip(enemyID)
        cd = self.level * 0.07 + 0.25
        teamCR = self.level * 0.01 + 0.09
        teamCD = self.level * 0.07 + 0.21
        bl.append(Buff("EarthlyCD", Pwr.CD_PERCENT, cd, self.wearerRole))
        bl.append(Buff("EarthlyTeamCR", Pwr.CR_PERCENT, teamCR, Role.ALL))
        bl.append((Buff("EarthlyTeamCD", Pwr.CD_PERCENT, teamCD, Role.ALL)))
        return bl, dbl, al, dl
    
    