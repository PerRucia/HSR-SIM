from Buff import Buff
from Planar import Planar
from Delay import *
from Misc import *

class Kalpagni(Planar):
    name = "Forge of the Kalpagni Lantern"
    def __init__(self, wearerRole, fireWeakEnemies: bool = True):
        super().__init__(wearerRole)
        self.fireWeakEnemies = fireWeakEnemies
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("KalpagniSPD", Pwr.SPD_PERCENT, 0.06, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList

class KalpagniGallagher(Kalpagni):
    def __init__(self, wearerRole, fireWeakEnemies: bool = True):
        super().__init__(wearerRole)
        self.fireWeakEnemies = fireWeakEnemies
        
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        bl.append(Buff("KalpagniBE", Pwr.BE_PERCENT, 0.4, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        bl.append(Buff("KalpagniBE", Pwr.BE_PERCENT, 0.4, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
    
class KalpagniFirefly(Kalpagni):
    def __init__(self, wearerRole, fireWeakEnemies: bool = True):
        super().__init__(wearerRole)
        self.fireWeakEnemies = fireWeakEnemies
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        bl.append(Buff("KalpagniBE", Pwr.BE_PERCENT, 0.4, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl

    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        bl.append(Buff("KalpagniBE", Pwr.BE_PERCENT, 0.4, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl