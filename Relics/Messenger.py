from Relic import Relic
from Buff import *
from Misc import *

class Messenger(Relic):
    name = "Messenger Traversing Hackerspace"
    
    def __init__(self, wearerRole, setType, allyUlt):
        super().__init__(wearerRole, setType)
        self.allyUlt = allyUlt
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("MessengerSPD", "SPD%", 0.06, self.wearerRole, ["ALL"], 1, 1, Role.SELF, "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.allyUlt:
            bl.append(Buff("MessengerUltSPD", "SPD%", 0.12, "ALL", ["ALL"], 1, 1, Role.SELF, "END"))
        return bl, dbl, al, dl
