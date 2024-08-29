from Lightcone import Lightcone
from Buff import *
from Misc import *

class Texture(Lightcone):
    name = "Texture of Memories"
    path = Path.PRESERVATION
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 529.20

    def __init__(self, wearerRole, level=5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        ersBuff = self.level * 0.02 + 0.06
        buffList.append(Buff("TextureERS", Pwr.ERS_PERCENT, ersBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    
    