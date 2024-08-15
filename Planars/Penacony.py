from Buff import Buff
from Planar import Planar
from Delay import *

class Penacony(Planar):
    name = "Penacony, Land of the Dreams"
    
    def __init__(self, wearerRole: str, dpsEle: str, selfEle: str):
        super().__init__(wearerRole)
        self.dpsEle = dpsEle
        self.selfEle = selfEle
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PenaconyERR", "ERR%", 0.05, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        if self.dpsEle == self.selfEle:
            buffList.append(Buff("PenaconyDMG", "DMG%", 0.1, "DPS", ["ALL"], 1, 1, "DPS", "PERM"))
        return buffList, debuffList, advList, delayList