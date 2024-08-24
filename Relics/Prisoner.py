from Relic import Relic
from Buff import *
from Misc import *

class Prisoner(Relic):
    name = "Prisoner in Deep Confinement"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PrisonerATK", Pwr.ATK_PERCENT, 0.12, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            debuffList.append(Debuff("PrisonerSHRED", self.wearerRole, Pwr.SHRED, 0.18, Role.ALL, ["ALL"], 1000, 1, False, [0, 0], False))
        return buffList, debuffList, advList, delayList
