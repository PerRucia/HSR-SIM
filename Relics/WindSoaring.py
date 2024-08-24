from Relic import Relic
from Buff import Buff
from Misc import *

class WindSoaring(Relic):
    name = "The Wind-Soaring Valorous"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buff_lst = [(Buff("WindSoaringATK", Pwr.ATK_PERCENT, 0.12, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))]
        if self.setType == 4:
            buff_lst.append(Buff("WindSoaringCR", Pwr.CR_PERCENT, 0.06, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buff_lst, [], [], []
    
    def useFua(self, enemyID):
        buffList, debuffList, advList, delayList = super().useFua(enemyID)
        if self.setType == 4:
            buffList.append(Buff("WindSoaringDMG", Pwr.DMG_PERCENT, 0.36, self.wearerRole, ["ULT"], 1, 1, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList

class WindSoaringYunli(Relic):
    name = "The Wind-Soaring Valorous"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buff_lst = [(Buff("WindSoaringATK", Pwr.ATK_PERCENT, 0.12, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))]
        if self.setType == 4:
            buff_lst.append(Buff("WindSoaringCR", Pwr.CR_PERCENT, 0.06, self.wearerRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return buff_lst, [], [], []
    
    def useFua(self, enemyID):
        buffList, debuffList, advList, delayList = super().useFua(enemyID)
        if self.setType == 4:
            buffList.append(Buff("WindSoaringDMG", Pwr.DMG_PERCENT, 0.36, self.wearerRole, ["ULT"], 1, 1, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList
    
    def useUlt(self, enemyID):
        buffList, debuffList, advList, delayList = super().useUlt(enemyID)
        if self.setType == 4:
            buffList.append(Buff("WindSoaringDMG", Pwr.DMG_PERCENT, 0.36, self.wearerRole, ["ULT"], 1, 1, Role.SELF, TickDown.END))
        return buffList, debuffList, advList, delayList