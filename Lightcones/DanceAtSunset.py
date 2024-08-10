from Lightcone import Lightcone
from Buff import Buff

class Sunset(Lightcone):
    name = "Dance at Sunset"
    path = "DES"
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        cdBuff = self.level * 0.06 + 0.3
        buff_lst = [Buff("SunsetCD", "CD%", cdBuff, self.wearerRole, ["ALL"], 1000, 1)]
        return buff_lst, [], [], []
    
    def useUlt(self):
        buff_lst, debuff_lst = super().useUlt()
        dmgBuff = self.level * 0.06 + 0.3
        buff_lst.append(Buff("SunsetDMG", "DMG%", dmgBuff, self.wearerRole, ["ULT", "FUA"], 2, 2))
        return buff_lst, debuff_lst, [], []
    
    