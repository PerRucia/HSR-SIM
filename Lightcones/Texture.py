from Lightcone import Lightcone
from Buff import *

class Texture(Lightcone):
    name = "Texture of Memories"
    path = "PRE"
    baseHP = 1058.4
    baseATK = 423.36
    baseDEF = 529.20

    def __init__(self, wearerRole, level):
        super().__init__(wearerRole, level)
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        ersBuff = self.level * 0.02 + 0.06
        buffList.append(Buff("TextureERS", "ERS%", ersBuff, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return buffList, debuffList, advList, delayList
    
    
    