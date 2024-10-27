from Buff import *
from Lightcone import Lightcone
from Misc import *


class Shadowed(Lightcone):
    name = "Shadowed by Night"
    path = Path.HUNT
    baseHP = 846.7
    baseATK = 476.28
    baseDEF = 396.90

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
        self.beBuff = self.level * 0.07 + 0.21
        self.spdBuff = self.level * 0.01 + 0.07
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("ShadowedBE", Pwr.BE_PERCENT, self.beBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("ShadowedSPD", Pwr.SPD_PERCENT, self.spdBuff, self.wearerRole, [AtkType.ALL], 2, 1, tdType=TickDown.END,))
        return buffList, debuffList, advList, delayList
    
    def ownTurn(self, turn, result):
        bl, dbl, al, dl = super().ownTurn(turn, result)
        if result.brokenEnemy:
            bl.append(Buff("ShadowedSPD", Pwr.SPD_PERCENT, self.spdBuff, self.wearerRole, [AtkType.ALL], 2, 1, tdType=TickDown.END,))
        return bl, dbl, al, dl
    
    