from Relic import Relic
from Buff import *
from Misc import *

class Sacerdos(Relic):
    name = "Sacerdos' Relieved Ordeal"
    
    def __init__(self, wearerRole, setType, targetRole = Role.DPS):
        super().__init__(wearerRole, setType)
        self.targetRole = targetRole
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("SacerdosSPD", Pwr.SPD_PERCENT, 0.06, self.wearerRole, [AtkType.ALL]))
        return bl, dbl, al, dl

class SacerdosSunday(Sacerdos):
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        if self.setType == 4:
            bl.append(Buff(f"SacerdosCD{self.wearerRole.name}", Pwr.CD_PERCENT, 0.18, self.targetRole, [AtkType.ALL], 2, 2, self.targetRole, TickDown.END))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.setType == 4:
            bl.append(Buff(f"SacerdosCD{self.wearerRole.name}", Pwr.CD_PERCENT, 0.18, self.targetRole, [AtkType.ALL], 2, 2, self.targetRole, TickDown.END))
        return bl, dbl, al, dl