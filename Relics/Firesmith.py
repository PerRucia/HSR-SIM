from Buff import Buff
from Misc import *
from Relic import Relic


class Firesmith(Relic):
    name = "Firesmith of Lava-Forging"
    
    def __init__(self, wearerRole, setType, wearerEle = Element.FIRE):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == Element.FIRE:
            bl.append(Buff("FiresmithDMG", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            bl.append(Buff("FiresmithSkillDMG", Pwr.DMG_PERCENT, 0.12, self.wearerRole, atkType=[AtkType.SKL]))
        return bl, debuffList, advList, delayList
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        if self.setType == 4:
            bl.append(Buff("FiresmithUltDMG", Pwr.DMG_PERCENT, 0.12, self.wearerRole, turns=1, tdType=TickDown.END))
        return bl, dbl, al, dl
    
