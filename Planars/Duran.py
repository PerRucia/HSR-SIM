from Buff import Buff
from Planar import Planar

class Duran(Planar):
    name = "Duran, Dynasty of Running Wolves"
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def equip(self):
        buff_lst = [Buff("DuranDMG", "DMG%", 0.25, self.wearerRole, ["FUA"], 1000, 1)]
        buff_lst.append(Buff("DuranCD", "CD%", 0.25, self.wearerRole, ["ALL"], 1000, 1))
        return buff_lst, [], [], []