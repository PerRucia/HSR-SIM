from Lightcone import Lightcone
from Buff import Buff

class Swordplay(Lightcone):
    name = "Swordplay"
    path = "HUN"
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBuff = (self.level * 0.02 + 0.06) * 5
        buffList.append(Buff("SwordplayDMG", "DMG%", dmgBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList

    

    