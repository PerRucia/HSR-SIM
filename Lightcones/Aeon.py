from Lightcone import Lightcone
from Buff import Buff
from Misc import *

class Aeon(Lightcone):
    name = "On the Fall of an Aeon"
    path = Path.DESTRUCTION
    baseHP = 1058.4
    baseATK = 529.20
    baseDEF = 396.90

    def __init__(self, wearerRole, level, uptime: float = 0.5):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBuff = (self.level * 0.03 + 0.09) * self.uptime
        buffList.append(Buff("AeonDMG", "DMG%", dmgBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        atkBuff = self.level * 0.02 + 0.06
        bl.append(Buff("AeonATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 4, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID):
        bl, dbl, al, dl = super().useSkl(enemyID)
        atkBuff = self.level * 0.02 + 0.06
        bl.append(Buff("AeonATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 4, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID):
        bl, dbl, al, dl = super().useBsc(enemyID)
        atkBuff = self.level * 0.02 + 0.06
        bl.append(Buff("AeonATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 4, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    