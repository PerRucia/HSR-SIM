from Lightcone import Lightcone
from Buff import *
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
        bl.append(Buff("WhereaboutsBE", Pwr.BE_PERCENT, beBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
class WhereaboutsFF(Whereabouts):
    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
        self.vulnBuff = level * 0.04 + 0.2
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl = super().ownTurn(result)
        for enemyID in result.brokenEnemy:
            dbl.append(Debuff("RoutedVULN", self.wearerRole, Pwr.VULN, self.vulnBuff, enemyID, [AtkType.BRK], 2, 1, False, [0, 0], False))
            dbl.append(Debuff("RoutedSPD", self.wearerRole, Pwr.SPD, -0.2, enemyID, [AtkType.ALL], 2, 1, False, [0, 0], False))
        for enemyID in result.enemiesHit:
            if result.preHitStatus[enemyID]:
                dbl.append(Debuff("RoutedVULN", self.wearerRole, Pwr.VULN, self.vulnBuff, enemyID, [AtkType.BRK], 2, 1, False, [0, 0], False))
                dbl.append(Debuff("RoutedSPD", self.wearerRole, Pwr.SPD, -0.2, enemyID, [AtkType.ALL], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl