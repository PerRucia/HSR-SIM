from Relic import Relic
from Buff import Buff
from Delay import *
from Result import Result

class Thief(Relic):
    name = "Thief of Shooting Meteor"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("ThiefBE", "BE%", 0.16, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, debuffList, advList, delayList
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl = super().ownTurn(result)
        if self.setType == 4 and result.brokenEnemy:
            bl.append(Buff("ThiefEnergy", "ERR_T", 3.0, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
