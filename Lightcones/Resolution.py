from Lightcone import Lightcone
from Buff import *
from Delay import *
from Misc import *

class Resolution(Lightcone):
    name = "Resolution Shines as Pearls of Sweat"
    path = Path.NIHILITY
    baseHP = 952.6
    baseATK = 476.28
    baseDEF = 330.75

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def useBsc(self, enemyID):
        bl, dbl, al, dl = super().useBsc(enemyID)
        shredBuff = self.level * 0.01 + 0.11
        dbl.append(Debuff(f"ResoShred({self.wearerRole.name})", self.wearerRole, Pwr.SHRED, shredBuff, enemyID, [Move.ALL], 1, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
class ResolutionPela(Resolution):

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def useSkl(self, enemyID):
        bl, dbl, al, dl = super().useSkl(enemyID)
        shredBuff = self.level * 0.01 + 0.11
        dbl.append(Debuff(f"ResoShred({self.wearerRole.name})", self.wearerRole, Pwr.SHRED, shredBuff, enemyID, [Move.ALL], 1, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID):
        bl, dbl, al, dl = super().useUlt(enemyID)
        shredBuff = self.level * 0.01 + 0.11
        dbl.append(Debuff(f"ResoShred({self.wearerRole.name})", self.wearerRole, Pwr.SHRED, shredBuff, Role.ALL, [Move.ALL], 1, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
class ResolutionJQ(ResolutionPela):
    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    