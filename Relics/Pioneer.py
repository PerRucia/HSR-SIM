from Relic import Relic
from Buff import Buff
from Delay import *
from Misc import *
from Result import Special

class Pioneer(Relic):
    name = "Pioneer Diver of Dead Waters"
    
    targetDebuffs = 0
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.setType == 4:
            bl.append(Buff("PioneerCR", Pwr.CR_PERCENT, 0.04, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
class PioneerRatio(Pioneer):
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)

    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if self.setType == 4:
            bl.append(Buff("PioneerBonusCR", Pwr.CR_PERCENT, 0.04, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
            if special.specialName == "Ratio":
                self.targetDebuffs = special.attr1
                if self.targetDebuffs >= 1:
                    bl.append(Buff("PioneerDMG", Pwr.DMG_PERCENT, 0.12, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
                    if self.targetDebuffs == 2:
                        bl.append(Buff("PioneerCD", Pwr.CD_PERCENT, 0.16, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
                    elif self.targetDebuffs >= 3:
                        bl.append(Buff("PioneerCD", Pwr.CD_PERCENT, 0.24, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
                else:
                    bl.append(Buff("PioneerCD", Pwr.CD_PERCENT, 0.00, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
            
