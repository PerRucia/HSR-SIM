from Lightcone import Lightcone
from Buff import *
from Result import Result

class Blissful(Lightcone):
    name = "Worrisome, Blissful"
    path = "HUN"
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level: int = 1, defaultTarget: int = 0):
        super().__init__(wearerRole, level)
        self.defaultTarget = defaultTarget    
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.03 + 0.15
        buffList.append(Buff("BlissfulCR", "CR%", crBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        dmgBuff = self.level * 0.05 + 0.25
        buffList.append(Buff("BlissfulDMG", "DMG%", dmgBuff, self.wearerRole, ["FUA"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    def useFua(self, enemyID):
        bl, dbl, al, dl = super().useFua(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
class BlissfulTopaz(Blissful): 
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl = super().ownTurn(result)
        if result.turnName == "NumbyGoGo":
            cdBuff = self.level * 0.02 + 0.10
            dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
class BlissfulFeixiao(Blissful):
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
class BlissfulMoze(Blissful):
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl = super().useFua(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole}", self.wearerRole, "CD%", cdBuff, self.defaultTarget, ["ALL"], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    