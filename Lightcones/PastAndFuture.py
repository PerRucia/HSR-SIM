from Lightcone import Lightcone
from Buff import *
from Result import Result
from Misc import *

class PastAndFuture(Lightcone):
    name = "Past and Future"
    path = Path.HARMONY
    baseHP = 952.6
    baseATK = 423.36
    baseDEF = 396.90

    def __init__(self, wearerRole, level=5, targetRole: str = "DPS"):
        super().__init__(wearerRole, level)
        self.targetRole = targetRole
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        bl.append(Buff("PNFSkillBuff", "DMG%", self.level * 0.04 + 0.12, self.targetRole, ["ALL"], 1, 1, self.targetRole, "END"))
        return bl, dbl, al, dl
    
    