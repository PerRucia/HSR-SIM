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
        
    def findMains(self, query: str):
        return sum([1 for item in [self.body, self.boots, self.sphere, self.rope] if item == query])
    
    def getScalingValue(self, scaling: str) -> tuple[float, float]: # returns Scaling%, ScalingFlat
        if scaling == "HP":
            return self.getHPPercent(), self.getHPFlat()
        elif scaling == "ATK":
            return self.getATKPercent(), self.getATKFlat()
        elif scaling == "DEF":
            return self.getDEFPercent(), self.getDEFFlat()
        return 0, 0
    
    def totalSubRolls(self) -> int:
        return self.spd + self.hpFlat + self.atkFlat + self.defFlat + self.hpPercent + self.atkPercent + self.defPercent + self.be + self.ehr + self.ers + self.cr + self.cd
    
    def getSPD(self) -> float:
        return self.spd * 2.3 + self.findMains("SPD") * 25.032
    
    def getHPFlat(self) -> float:
        return 705.6 + self.hpFlat * 38.103755
    
    def getHPPercent(self) -> float:
        return self.hpPercent * 0.03888 + self.findMains("HP%") * 0.432
    
    def getATKFlat(self) -> float:
        return self.atkFlat * 19.051877 + 352.8
    
    def getATKPercent(self) -> float:
        return self.atkPercent * 0.03888 + self.findMains("ATK%") * 0.432
    
    def getDEFFlat(self) -> float:
        return self.defFlat * 19.051877
    
    def getDEFPercent(self) -> float:
        return self.defPercent * 0.0486 + self.findMains("DEF%") * 0.54
    
    def getBE(self) -> float:
        return self.be * 0.05832 + self.findMains("BE%") * 0.648
    
    def getEHR(self) -> float:
        return self.ehr * 0.03888 + self.findMains("EHR%") * 0.432
    
    def getERS(self) -> float:
        return self.ers * 0.03888
    
    def getCR(self) -> float:
        return self.cr * 0.02916 + self.findMains("CR%") * 0.324 + 0.05
    
    def getCD(self) -> float:
        return self.cd * 0.05832 + self.findMains("CD%") * 0.648 + 0.5
    
    def getDMG(self) -> float:
        return self.findMains("DMG%") * 0.388803
    
        