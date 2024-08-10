from Relic import Relic
from Buff import Buff

class WindSoaring(Relic):
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        buff_lst = []
        buff_lst.append(Buff("WindSoaringATK", "ATK%", 0.12, self.wearerRole, ["ALL"], 1000, 1))
        if self.setType == 4:
            buff_lst.append(Buff("WindSoaringCR", "CR%", 0.06, self.wearerRole, ["ALL"], 1000, 1))
        return buff_lst, [], [], []
    
    def useFua(self):
        if self.setType == 4:
            buff_lst = [Buff("WindSoaringDMG", "DMG%", 0.36, self.wearerRole, ["ULT"], 1, 1)]
            return buff_lst, [], [], []
        return super().useFua()