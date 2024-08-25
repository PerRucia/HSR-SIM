from Lightcone import Lightcone
from Buff import *
from Result import Result
from Misc import *

class InTheNight(Lightcone):
    name = "In The Night"
    path = Path.HUNT
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level = 1, wearerSPD: float = 100):
        super().__init__(wearerRole, level)
        self.bonusStacks = min(6, (wearerSPD - 100) // 10) if wearerSPD >= 100 else 0
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.03 + 0.15
        buffList.append(Buff("InTheNightCR", Pwr.CR_PERCENT, crBuff, self.wearerRole, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        dmgBuff = (self.level * 0.01 + 0.05) * self.bonusStacks
        cdBuff = (self.level * 0.02 + 0.1) * self.bonusStacks
        buffList.append(Buff("InTheNightDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [Move.BSC, Move.SKL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("InTheNightCD", Pwr.CD_PERCENT, cdBuff, self.wearerRole, [Move.ULT], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    