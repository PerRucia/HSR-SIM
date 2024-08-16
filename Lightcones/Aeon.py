from Lightcone import Lightcone
from Buff import Buff

class Aeon(Lightcone):
    name = "On the Fall of an Aeon"
    path = "DES"
    baseHP = 1058.4
    baseATK = 529.20
    baseDEF = 396.90

    def __init__(self, wearerRole, level, uptime):
        super().__init__(wearerRole, level)
        self.uptime = uptime
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        dmgBuff = (self.level * 0.03 + 0.09) * self.uptime
        buffList.append(Buff("AeonDMG", "DMG%", dmgBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self):
        bl, dbl, al, dl = super().useUlt()
        atkBuff = self.level * 0.02 + 0.06
        bl.append(Buff("AeonATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 4, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useSkl(self):
        bl, dbl, al, dl = super().useSkl()
        atkBuff = self.level * 0.02 + 0.06
        bl.append(Buff("AeonATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 4, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self):
        bl, dbl, al, dl = super().useBsc()
        atkBuff = self.level * 0.02 + 0.06
        bl.append(Buff("AeonATK", "ATK%", atkBuff, self.wearerRole, ["ALL"], 1, 4, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    