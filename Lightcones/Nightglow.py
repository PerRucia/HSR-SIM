from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Nightglow(Lightcone):
    name = "Flowing Nightglow"
    path = Path.HARMONY
    baseHP = 952.6
    baseATK = 635.04
    baseDEF = 463.05

    def __init__(self, wearerRole, level=1):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        err = (self.level * 0.005 + 0.025) * 5
        buffList.append(Buff("NightglowERR", "ERR%", err, self.wearerRole, ["ALL"], 1, 1, Role.SELF, "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        atk = self.level * 0.12 + 0.36
        dmg = self.level * 0.04 + 0.20
        buffList.append(Buff("NightglowATK", "ATK%", atk, self.wearerRole, ["ALL"], 1, 1, Role.SELF, "END"))
        buffList.append(Buff("NightglowDMG", "DMG%", dmg, Role.ALL, ["ALL"], 1, 1, Role.SELF, "END"))
        return buffList, debuffList, advList, delayList    
    