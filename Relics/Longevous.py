from Relic import Relic
from Buff import Buff

class Longevous(Relic):
    name = "Longevous Disciple"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("LongevousHP", "HP%", 0.12, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useHit(self):
        bl, dbl, al, dl = super().useHit()
        if self.setType == 4:
            bl.append(Buff("LongevousCR", "CR%", 0.08, self.wearerRole, ["ALL"], 2, 2, "SELF", "END"))
        return bl, dbl, al, dl
