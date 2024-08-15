from Relic import Relic
from Buff import *

class Prisoner(Relic):
    name = "Prisoner in Deep Confinement"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PrisonerATK", "ATK%", 0.12, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        if self.setType == 4:
            debuffList.append(Debuff("PrisonerSHRED", self.wearerRole, "SHRED", 0.18, "ALL", ["ALL"], 1000, 1, False, False))
        return buffList, debuffList, advList, delayList
