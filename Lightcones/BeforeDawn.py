from Delay import *
from Buff import *
from Lightcone import Lightcone


class BeforeDawn(Lightcone):
    name = "Before Dawn"
    path = Path.ERUDITION
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("DawnCD", Pwr.CD_PERCENT, self.level * 0.06 + 0.30, self.wearerRole))
        bl.append(Buff("DawnDMG", Pwr.DMG_PERCENT, self.level * 0.03 + 0.15, self.wearerRole, [AtkType.SKL, AtkType.ULT]))
        bl.append(Buff("DawnFuaDMG", Pwr.DMG_PERCENT, self.level * 0.08 + 0.40, self.wearerRole, [AtkType.FUA]))
        return bl, dbl, al, dl

    
    