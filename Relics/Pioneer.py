from Relic import Relic
from Buff import *
from Result import *

class Pioneer(Relic):
    name = "Pioneer Diver of Dead Waters"
    
    targetDebuffs = 0
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        if self.setType == 4:
            bl.append(Buff("PioneerCR", "CR%", 0.04, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "FeixiaoStartFUA" or special.specialName == "FeixiaoCheckRobin":
            self.targetDebuffs = min(3.0, special.attr2)
        if self.targetDebuffs >= 1:
            bl.append(Buff("PioneerDMG", "DMG%", 0.12, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        else:
            bl.append(Buff("PioneerDMG", "DMG%", 0.00, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        if self.setType == 4:
            if self.targetDebuffs <= 2:
                bl.append(Buff("PioneerCD", "CD%", 0.00, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
            elif self.targetDebuffs == 2:
                bl.append(Buff("PioneerCD", "CD%", 0.08, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
            elif self.targetDebuffs >= 3:
                bl.append(Buff("PioneerCD", "CD%", 0.12, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    

