from Buff import Buff
from Planar import Planar
from Delay import *
from Misc import *

class Penacony(Planar):
    name = "Penacony, Land of the Dreams"
    
    def __init__(self, wearerRole: str, sameEleTeammates: list[Role]):
        super().__init__(wearerRole)
        self.sameEle = sameEleTeammates
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PenaconyERR", Pwr.ERR_PERCENT, 0.05, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.END))
        for role in self.sameEle:
            buffList.append(Buff("PenaconyDMG", Pwr.DMG_PERCENT, 0.1, role, ["ALL"], 1, 1, role, TickDown.END))
        return buffList, debuffList, advList, delayList