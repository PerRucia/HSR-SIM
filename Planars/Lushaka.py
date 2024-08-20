from Buff import Buff
from Planar import Planar
from Delay import *

class Lushaka(Planar):
    name = "Lushaka, the Sunken Seas"
    def __init__(self, wearerRole: str, slot1Role: str = "DPS"):
        super().__init__(wearerRole)
        self.slot1Role = slot1Role
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("LukshakaERR", "ERR%", 0.05, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        buffList.append(Buff("LukshakaATK", "ATK%", 0.15, self.slot1Role, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList