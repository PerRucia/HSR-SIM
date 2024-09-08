from Misc import *

class RelicStats:
    def __init__(self, spd, hpF, atkF, defF, hpP, atkP, defP, be, ehr, ers, cr, cd, bodyMain, bootMain, sphereMain, ropeMain):
        self.spd = spd
        self.hpFlat = hpF
        self.atkFlat = atkF
        self.defFlat = defF
        self.hpPercent = hpP
        self.atkPercent = atkP
        self.defPercent = defP
        self.be = be
        self.ehr = ehr
        self.ers = ers
        self.cr = cr
        self.cd = cd
        self.body = bodyMain
        self.boots = bootMain
        self.sphere = sphereMain
        self.rope = ropeMain
        
    def findMains(self, query: Pwr):
        return sum([1 for item in [self.body, self.boots, self.sphere, self.rope] if item == query])
    
    def getScalingValue(self, scaling: str) -> tuple[float, float]: # returns Scaling%, ScalingFlat
        if scaling == Scaling.HP:
            return self.getHPPercent(), self.getHPFlat()
        elif scaling == Scaling.ATK:
            return self.getATKPercent(), self.getATKFlat()
        elif scaling == Scaling.DEF:
            return self.getDEFPercent(), self.getDEFFlat()
        return 0, 0
    
    def totalSubRolls(self) -> int:
        return self.spd + self.hpFlat + self.atkFlat + self.defFlat + self.hpPercent + self.atkPercent + self.defPercent + self.be + self.ehr + self.ers + self.cr + self.cd
    
    def getSPD(self) -> float:
        return self.spd * 2.3 + self.findMains(Pwr.SPD) * 25.032
    
    def getHPFlat(self) -> float:
        return 705.6 + self.hpFlat * 38.103755
    
    def getHPPercent(self) -> float:
        return self.hpPercent * 0.03888 + self.findMains(Pwr.HP_PERCENT) * 0.432
    
    def getATKFlat(self) -> float:
        return self.atkFlat * 19.051877 + 352.8
    
    def getATKPercent(self) -> float:
        return self.atkPercent * 0.03888 + self.findMains(Pwr.ATK_PERCENT) * 0.432
    
    def getDEFFlat(self) -> float:
        return self.defFlat * 19.051877
    
    def getDEFPercent(self) -> float:
        return self.defPercent * 0.0486 + self.findMains(Pwr.DEF_PERCENT) * 0.54
    
    def getBE(self) -> float:
        return self.be * 0.05832 + self.findMains(Pwr.BE_PERCENT) * 0.648
    
    def getEHR(self) -> float:
        return self.ehr * 0.03888 + self.findMains(Pwr.EHR_PERCENT) * 0.432
    
    def getERS(self) -> float:
        return self.ers * 0.03888
    
    def getCR(self) -> float:
        return self.cr * 0.02916 + self.findMains(Pwr.CR_PERCENT) * 0.324 + 0.05
    
    def getCD(self) -> float:
        return self.cd * 0.05832 + self.findMains(Pwr.CD_PERCENT) * 0.648 + 0.5
    
    def getDMG(self) -> float:
        return self.findMains(Pwr.DMG_PERCENT) * 0.388803
    
    def getERR(self) -> float:
        return self.findMains(Pwr.ERR_PERCENT) * 0.194394
    
    def getOGH(self) -> float:
        return self.findMains(Pwr.OGH_PERCENT) * 0.345606 
        