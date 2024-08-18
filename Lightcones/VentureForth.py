from Lightcone import Lightcone
from Buff import Buff

class VentureForth(Lightcone):
    name = "I Venture Forth to Hunt"
    path = "HUN"
    baseHP = 952.6
    baseATK = 635.04
    baseDEF = 463.05

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.025 + 0.125
        buffList.append(Buff("VentureCR", "CR%", crBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useFua(self):
        bl, dbl, al, dl = super().useFua()
        shredBuff = self.level * 0.03 + 0.24
        dbl.append(Buff("VentureSHRED", "SHRED", shredBuff, self.wearerRole, ["ULT"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl
    
class VentureForthFeixiao(Lightcone):
    name = "I Venture Forth to Hunt"
    path = "HUN"
    baseHP = 952.6
    baseATK = 635.04
    baseDEF = 463.05

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.025 + 0.125
        buffList.append(Buff("VentureCR", "CR%", crBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useFua(self):
        bl, dbl, al, dl = super().useFua()
        shredBuff = self.level * 0.03 + 0.24
        bl.append(Buff("VentureSHRED", "SHRED", shredBuff, self.wearerRole, ["ULT"], 2, 2, "SELF", "END"))
        return bl, dbl, al, dl
    
    def useUlt(self):
        bl, dbl, al, dl = super().useUlt()
        shredBuff = self.level * 0.03 + 0.24
        bl.append(Buff("VentureSHRED", "SHRED", shredBuff, self.wearerRole, ["ULT"], 2, 2, "SELF", "END"))
        return bl, dbl, al, dl
    
    
    