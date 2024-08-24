from Buff import Buff
from Planar import Planar
from Misc import *

class Keel(Planar):
    name = "Broken Keel"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("KeelEFFRES", "ERS%", 0.10, self.wearerRole, ["ALL"], 1, 1, Role.SELF, "PERM"))
        buffList.append(Buff(f"KeelCD({self.wearerRole.name})", "CD%", 0.10, Role.ALL, ["ALL"], 1, 1, Role.SELF, "PERM"))
        return buffList, debuffList, advList, delayList
    