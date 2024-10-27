from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Ascent(Lightcone):
    name = "A Grounded Ascent"
    path = Path.HARMONY
    baseHP = 1164.2
    baseATK = 476.28
    baseDEF = 529.20
    
    procs = 0

    def __init__(self, wearerRole, level=1, targetRole=Role.DPS):
        super().__init__(wearerRole, level)
        self.targetRole = targetRole
    
class AscentSunday(Ascent):  
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        bl.extend(self.addHymm())
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        bl.extend(self.addHymm())
        return bl, dbl, al, dl
        
    def addHymm(self) -> list[Buff]:
        lst = []
        lst.append(Buff("AscentERR", Pwr.ERR_T, self.level * 0.5 + 5.5, self.targetRole))
        lst.append(Buff("AscentHymm", Pwr.DMG_PERCENT, self.level * 0.0225 + 0.1275, self.targetRole, [AtkType.ALL], 2, 3, Role.SELF, tdType=TickDown.END))
        self.procs += 1
        if self.procs % 2 == 0:
            lst.append(Buff("AscentSP", Pwr.SKLPT, 1, self.wearerRole))
        return lst
    
    