from Lightcone import Lightcone
from Buff import Buff
from Delay import *
from Misc import *
from Result import Result

class Whereabouts(Lightcone):
    name = "Whereabouts Shoud Dreams Rest"
    path = Path.DESTRUCTION
    baseHP = 1164.2
    baseATK = 476.28
    baseDEF = 529.20    

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self, enemyID=-1):
        bl, dbl, al, dl = super().equip(enemyID)
        beBuff = self.level * 0.1 + 0.5
        bl.append(Buff("WhereaboutsBE", Pwr.BE_PERCENT, beBuff, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl = super().ownTurn(result)
    
    