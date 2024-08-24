from Relic import Relic
from Buff import Buff
from Misc import *
class Musketeer(Relic):
    name = "Musketeer of Wild Wheat"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("MuskATK", "ATK%", 0.12, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            buffList.append(Buff("MuskSPD", "SPD%", 0.06, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
            buffList.append(Buff("MuskATK", "DMG%", 0.10, self.wearerRole, ["BSC"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
