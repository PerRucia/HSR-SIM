from Buff import Buff
from Misc import *
from Relic import Relic


class Champion(Relic):
    name = "Champion of Streetwise Boxing"
    
    def __init__(self, wearerRole, setType, wearerEle = Element.PHYSICAL):
        super().__init__(wearerRole, setType)
        self.wearerEle = wearerEle
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        if self.wearerEle == Element.PHYSICAL:
            bl.append(Buff("ChampionDMG", Pwr.DMG_PERCENT, 0.10, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        if self.setType == 4:
            bl.append(Buff("ChampionATK", Pwr.ATK_PERCENT, 0.05, self.wearerRole, stackLimit=5))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        if self.setType == 4:
            bl.append(Buff("ChampionATK", Pwr.ATK_PERCENT, 0.05, self.wearerRole, stackLimit=5))
        return bl, dbl, al, dl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl = super().useHit(enemyID)
        if self.setType == 4:
            bl.append(Buff("ChampionATK", Pwr.ATK_PERCENT, 0.05, self.wearerRole, stackLimit=5))
        return bl, dbl, al, dl
    
    
