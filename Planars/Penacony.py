from Buff import Buff
from Planar import Planar
from Delay import *

class Penacony(Planar):
    name = "Penacony, Land of the Dreams"
    
    def __init__(self, wearerRole: str, sameEleTeammates: list[str]):
        super().__init__(wearerRole)
        self.sameEle = sameEleTeammates
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PenaconyERR", "ERR%", 0.05, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        for role in self.sameEle:
            buffList.append(Buff("PenaconyDMG", "DMG%", 0.1, role, ["ALL"], 1, 1, role, "PERM"))
        return buffList, debuffList, advList, delayList