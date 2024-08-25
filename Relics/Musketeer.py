from Relic import Relic
from Buff import Buff
from Misc import *
class Musketeer(Relic):
    name = "Musketeer of Wild Wheat"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("MuskATK", Pwr.ATK_PERCENT, 0.12, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            buffList.append(Buff("MuskSPD", Pwr.SPD_PERCENT, 0.06, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
            buffList.append(Buff("MuskATK", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [Move.BSC], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
