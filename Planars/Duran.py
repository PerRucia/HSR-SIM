from Buff import Buff
from Planar import Planar

class Duran(Planar):
    name = "Duran, Dynasty of Running Wolves"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("DuranDMG", "DMG%", 0.25, self.wearerRole, ["FUA"], 1, 1, "SELF", "PERM"))
        buffList.append(Buff("DuranCD", "CD%", 0.25, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList