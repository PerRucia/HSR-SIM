from Relic import Relic
from Buff import Buff
from Misc import *
from Result import Special

class Cavalry(Relic):
    name = "Iron Cavalry Against the Scourge"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("CavalryBE", Pwr.BE_PERCENT, 0.16, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
class CavalryFirefly(Cavalry):
    beStat = 0
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
    
    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "Firefly":
            self.beStat = special.attr1
            brkShred = 0.1 if self.beStat >= 1.5 else 0
            sbrkShred = 0.15 if self.beStat >= 2.5 else 0
            bl.append(Buff("CavalryBRKSHRED", Pwr.SHRED, brkShred, self.wearerRole, [Move.BRK], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("CavalrySBRKSHRED", Pwr.SHRED, sbrkShred, self.wearerRole, [Move.SBK], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
