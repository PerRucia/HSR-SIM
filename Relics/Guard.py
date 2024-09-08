from Buff import Buff
from Misc import *
from Relic import Relic


class Guard(Relic):
    name = "Guard of Wuthering Snow"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        if self.setType == 4:
            bl.append(Buff("GuardERR", Pwr.ERR_T, 5, self.wearerRole))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        if self.setType == 4:
            bl.append(Buff("GuardERR", Pwr.ERR_T, 5, self.wearerRole))
        return bl, dbl, al, dl
    
