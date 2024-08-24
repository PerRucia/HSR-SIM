from Buff import Buff
from Planar import Planar
from Misc import *

class Keel(Planar):
    name = "Broken Keel"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("KeelEFFRES", Pwr.ERS_PERCENT, 0.10, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff(f"KeelCD({self.wearerRole.name})", Pwr.CD_PERCENT, 0.10, Role.ALL, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    