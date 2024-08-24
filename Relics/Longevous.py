from Relic import Relic
from Buff import Buff
from Misc import *

class Longevous(Relic):
    name = "Longevous Disciple"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("LongevousHP", Pwr.HP_PERCENT, 0.12, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useHit(self, enemyID):
        bl, dbl, al, dl = super().useHit(enemyID)
        if self.setType == 4:
            bl.append(Buff("LongevousCR", Pwr.CR_PERCENT, 0.08, self.wearerRole, ["ALL"], 2, 2, Role.SELF, TickDown.END))
        return bl, dbl, al, dl
