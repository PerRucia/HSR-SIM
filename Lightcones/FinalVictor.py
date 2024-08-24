from Lightcone import Lightcone
from Buff import *
from Result import Result
from Misc import *

class FinalVictorFeixiao(Lightcone):
    name = "Final Victor"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
        self.cdBuff = (self.level * 0.01 + 0.07) * 0.75
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        atkBuff = self.level * 0.02 + 0.10
        buffList.append(Buff("FinalVictorATK", Pwr.ATK_PERCENT, atkBuff, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        for _ in range(3):
            bl.append(Buff("FinalVictorCD", Pwr.CD_PERCENT, self.cdBuff, self.wearerRole, ["ALL"], 1, 4, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        for _ in range(4):
            bl.append(Buff("FinalVictorCD", Pwr.ATK_PERCENT, self.cdBuff, self.wearerRole, ["ALL"], 1, 4, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        for _ in range(4):
            bl.append(Buff("FinalVictorCD", Pwr.ATK_PERCENT, self.cdBuff, self.wearerRole, ["ALL"], 1, 4, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    