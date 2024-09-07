from Relic import Relic
from Buff import Buff
from Delay import *
from Misc import *

class Glacial(Relic):
    name = "Hunter of Glacial Forest"
    
    def __init__(self, wearerRole, setType, wearerEle = Element.ICE):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == Element.ICE:
            bl.append(Buff("GalcialDMG", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.setType == 4:
            bl.append(Buff("GlacialCD", Pwr.CD_PERCENT, 0.25, self.wearerRole, turns=2, tdType=TickDown.END))
        return bl, dbl, al, dl
    
