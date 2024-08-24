from Lightcone import Lightcone
from Buff import *
from Result import Result
from Misc import *

class Subscribe(Lightcone):
    name = "Subscribe for More!"
    path = Path.HUNT
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBUff = self.level * 0.06 + 0.18
        buffList.append(Buff("SubscribeDMG", "DMG%", dmgBUff, self.wearerRole, ["BSC", "SKL"], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    