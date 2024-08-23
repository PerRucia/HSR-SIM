from Lightcone import Lightcone
from Buff import Buff

class Journey(Lightcone):
    name = "For Tomorrow's Journey"
    path = "HAR"
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        atkBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("JourneyATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        dmgBuff = self.level * 0.03 + 0.15
        buffList.append(Buff("JourneyUltDMG", "DMG%", dmgBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "END"))
        return buffList, debuffList, advList, delayList    
    