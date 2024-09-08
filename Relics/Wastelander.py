from Buff import Buff
from Misc import *
from Relic import Relic


class Wastelander(Relic):
    name = "Wastelander of Banditry Desert"
    
    def __init__(self, wearerRole, setType, wearerEle = Element.IMAGINARY):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == Element.IMAGINARY:
            bl.append(Buff("WastelanderDMG", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
    
