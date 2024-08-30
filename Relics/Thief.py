from Relic import Relic
from Buff import Buff
from Delay import *
from Result import Result
from Misc import *
from Turn import *

class Thief(Relic):
    name = "Thief of Shooting Meteor"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("ThiefBE", Pwr.BE_PERCENT, 0.16, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().ownTurn(turn, result)
        if self.setType == 4 and result.brokenEnemy:
            bl.append(Buff("ThiefEnergy", Pwr.ERR_T, 3.0, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
