from Lightcone import Lightcone
from Buff import *
from Misc import *
from Result import Special

class Spring(Lightcone):
    name = "Those Many Springs"
    path = Path.NIHILITY
    baseHP = 952.6
    baseATK = 582.12
    baseDEF = 529.20

    targetStatus = []
    
    def __init__(self, wearerRole, level = 1):
        super().__init__(wearerRole, level)
        self.vulnBuff = level * 0.04 + 0.2
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        ehrBuff = self.level * 0.10 + 0.5
        buffList.append(Buff("SpringEHR", Pwr.EHR_PERCENT, ehrBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        for i in range(len(self.targetStatus)):
            if not self.targetStatus[i]:
                dbl.append(Debuff("SpringVULN", self.wearerRole, Pwr.VULN, self.vulnBuff, enemyID, [AtkType.ALL], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID):
        bl, dbl, al, dl = super().useSkl(enemyID)
        if not self.targetStatus[enemyID]:
            dbl.append(Debuff("SpringVULN", self.wearerRole, Pwr.VULN, self.vulnBuff, enemyID, [AtkType.ALL], 2, 1, False, [0, 0], False))
        adjTargets = []
        if enemyID - 1 >= 0:
            adjTargets.append(enemyID - 1)
        if enemyID + 1 < len(self.targetStatus):
            adjTargets.append(enemyID + 1)
        for adj in adjTargets:
            if not self.targetStatus[adj]:
                dbl.append(Debuff("SpringVULN", self.wearerRole, Pwr.VULN, self.vulnBuff, adj, [AtkType.ALL], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID):
        bl, dbl, al, dl = super().useBsc(enemyID)
        if not self.targetStatus[enemyID]:
            dbl.append(Debuff("SpringVULN", self.wearerRole, Pwr.VULN, self.vulnBuff, enemyID, [AtkType.ALL], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "Jiaoqiu":
            self.targetStatus = special.attr4
        return bl, dbl, al, dl    
        
    
    