from Buff import Buff
from Planar import Planar
from Delay import *

class KalpagniGallagher(Planar):
    name = "Forge of the Kalpagni Lantern"
    def __init__(self, wearerRole: str, fireWeakEnemies: bool = True):
        super().__init__(wearerRole)
        self.fireWeakEnemies = fireWeakEnemies
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("KalpagniSPD", "SPD%", 0.06, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID):
        bl, dbl, al, dl = super().useBsc(enemyID)
        if self.fireWeakEnemies:
            bl.append(Buff("KalpagniBE", "BE%", 0.40, self.wearerRole, ["ALL"], 1, 1, "SELF", "END"))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.fireWeakEnemies:
            bl.append(Buff("KalpagniBE", "BE%", 0.40, self.wearerRole, ["ALL"], 1, 1, "SELF", "END"))
        return bl, dbl, al, dl