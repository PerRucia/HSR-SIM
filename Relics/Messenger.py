from Relic import Relic
from Buff import *
from Misc import *

class Messenger(Relic):
    name = "Messenger Traversing Hackerspace"
    
    def __init__(self, wearerRole, setType, allyUlt=False):
        super().__init__(wearerRole, setType)
        self.allyUlt = allyUlt
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("MessengerSPD", Pwr.SPD_PERCENT, 0.06, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.allyUlt:
            bl.append(Buff("MessengerUltSPD", Pwr.SPD_PERCENT, 0.12, Role.ALL, [AtkType.ALL], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
