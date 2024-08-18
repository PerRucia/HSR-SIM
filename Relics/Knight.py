from Relic import Relic
from Buff import Buff

class Knight(Relic):
    name = "Knight of Purity Palace"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("KnightRelicDEF", "DEF%", 0.15, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
