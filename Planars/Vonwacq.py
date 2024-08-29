from Buff import Buff
from Planar import Planar
from Delay import *
from Misc import *

class Vonwacq(Planar):
    name = "Sprightly Vonwacq"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("VonwacqERR", Pwr.ERR_PERCENT, 0.05, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        advList.append(Advance("VonwacqADV", self.wearerRole, 0.4))
        return buffList, debuffList, advList, delayList