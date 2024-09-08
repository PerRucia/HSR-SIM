from Buff import Buff
from Misc import *
from Relic import Relic


class Watchmaker(Relic):
    name = "Watch, Master of Dream Machinations"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("WatchBE", Pwr.BE_PERCENT, 0.16, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
class WatchmakerHMC(Watchmaker):
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.setType == 4:
            bl.append(Buff("WatchUltBE", Pwr.BE_PERCENT, 0.3, Role.ALL, turns=2, tdType=TickDown.END))
        return bl, dbl, al, dl
