from Buff import *
from Lightcone import Lightcone
from Misc import *
from Result import Special


class Breakfast(Lightcone):
    name = "The Seriousness of Breakfast"
    path = Path.ERUDITION
    baseHP = 846.7
    baseATK = 476.28
    baseDEF = 396.90

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBuff = self.level * 0.03 + 0.09
        buffList.append(Buff("BreakfastDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("BreakfastATK", Pwr.ATK_PERCENT, self.level * 0.01 + 0.04, self.wearerRole, stackLimit=3))
        return buffList, debuffList, advList, delayList

    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        bl.append(Buff("BreakfastATK", Pwr.ATK_PERCENT, self.level * 0.01 + 0.04, self.wearerRole, stackLimit=3))
        return bl, dbl, al, dl

    
    
    