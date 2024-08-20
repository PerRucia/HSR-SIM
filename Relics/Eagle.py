from Relic import Relic
from Buff import Buff
from Delay import *

class Eagle(Relic):
    name = "Eagle of Twilight Line"
    
    def __init__(self, wearerRole, setType, wearerEle: str = "WIN"):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == "WIN":
            bl.append(Buff("EagleDMG", "DMG%", 0.10, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.setType == 4:
            al.append(Advance(f"EagleAdv-{self.wearerRole}", self.wearerRole, 0.25))
        return bl, dbl, al, dl
