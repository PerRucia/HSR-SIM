from Buff import Buff
from Misc import *
from Planar import Planar


class Penacony(Planar):
    name = "Penacony, Land of the Dreams"
    
    def __init__(self, wearerRole: Role, sameEleTeammates: list[Role]):
        super().__init__(wearerRole)
        self.sameEle = sameEleTeammates
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("PenaconyERR", Pwr.ERR_PERCENT, 0.05, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        for role in self.sameEle:
            buffList.append(Buff("PenaconyDMG", Pwr.DMG_PERCENT, 0.1, role, [AtkType.ALL], 1, 1, role, TickDown.PERM))
        return buffList, debuffList, advList, delayList