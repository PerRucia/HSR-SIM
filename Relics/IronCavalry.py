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
        bl.append(Buff("CavalryBE", Pwr.BE_PERCENT, 0.16, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
class CavalryFirefly(Cavalry):
    beStat = 0
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
    
    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "Firefly" and self.setType == 4:
            self.beStat = special.attr2
            brkShred = 0.1 if self.beStat >= 1.5 else 0
            sbrkShred = 0.15 if self.beStat >= 2.5 else 0
            bl.append(Buff("CavalryBRKSHRED", Pwr.SHRED, brkShred, self.wearerRole, [AtkType.BRK]))
            bl.append(Buff("CavalrySBRKSHRED", Pwr.SHRED, sbrkShred, self.wearerRole, [AtkType.SBK]))
        return bl, dbl, al, dl


class CavalryRappa(Cavalry):
    rappaBE = 0

    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)

    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "Rappa" and self.setType == 4:
            self.rappaBE = special.attr1
            brkShred = 0.1 if self.rappaBE >= 1.5 else 0
            sbrkShred = 0.15 if self.rappaBE >= 2.5 else 0
            bl.append(Buff("CavalryBRKSHRED", Pwr.SHRED, brkShred, self.wearerRole, [AtkType.BRK]))
            bl.append(Buff("CavalrySBRKSHRED", Pwr.SHRED, sbrkShred, self.wearerRole, [AtkType.SBK]))
        return bl, dbl, al, dl

class CavalryLingsha(Cavalry):
    lingshaBE = 0

    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)

    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "Lingsha" and self.setType == 4:
            self.lingshaBE = special.attr3
            brkShred = 0.1 if self.lingshaBE >= 1.5 else 0
            sbrkShred = 0.15 if self.lingshaBE >= 2.5 else 0
            bl.append(Buff("CavalryBRKSHRED", Pwr.SHRED, brkShred, self.wearerRole, [AtkType.BRK]))
            bl.append(Buff("CavalrySBRKSHRED", Pwr.SHRED, sbrkShred, self.wearerRole, [AtkType.SBK]))
        return bl, dbl, al, dl
    
    
