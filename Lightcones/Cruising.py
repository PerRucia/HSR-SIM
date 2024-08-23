from Lightcone import Lightcone
from Buff import Buff

class Cruising(Lightcone):
    name = "Cruising in the Stellar Sea"
    path = "HUN"
    baseHP = 952.6
    baseATK = 529.2
    baseDEF = 463.05

    def __init__(self, wearerRole, level: int = 5, uptime: float = 0.5):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = (self.level * 0.02 + 0.06) + (self.level * 0.02 + 0.06) * self.uptime
        buffList.append(Buff("CruisingCR", "CR%", crBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        atkBuff = (self.level * 0.05 + 0.15) * self.uptime
        buffList.append(Buff("CruisingATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList

    

    