from Relic import Relic
from Buff import Buff
from Delay import *
from Misc import *

class Thunder(Relic):
    name = "Band of Sizzling Thunder"
    
    def __init__(self, wearerRole, setType, wearerEle = Element.LIGHTNING):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == Element.LIGHTNING:
            bl.append(Buff("BandDMG", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        if self.setType == 4:
            bl.append(Buff("BandATK", Pwr.ATK_PERCENT, 0.20, self.wearerRole, turns=2, tdType=TickDown.END))
        return bl, dbl, al, dl
    
    
