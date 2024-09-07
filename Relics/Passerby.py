from Relic import Relic
from Buff import *
from Misc import *

class Passerby(Relic):
    name = "Passerby of Wandering Cloud"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PasserbyOGH", Pwr.OGH_PERCENT, 0.10, self.wearerRole))
        if self.setType == 4:
            buffList.append(Buff("PasserbySP", Pwr.SKLPT, 1, self.wearerRole))
        return buffList, debuffList, advList, delayList
    
