from Lightcone import Lightcone
from Buff import Buff
from Misc import *


# noinspection PyDefaultArgument
class PoisedToBloom(Lightcone):
    name = "Poised to Bloom"
    path = Path.HARMONY
    baseHP = 952.6
    baseATK = 423.36
    baseDEF = 396.90

    def __init__(self, wearerRole, level=5, samePathRoles = [Role.DPS, Role.SUBDPS]):
        super().__init__(wearerRole, level)
        self.samePathRoles = samePathRoles
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        atkBuff = self.level * 0.04 + 0.12
        buffList.append(Buff("BloomATK", Pwr.ATK_PERCENT, atkBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        for role in self.samePathRoles:
            buffList.append(Buff("BloomCD", Pwr.CD_PERCENT, self.level * 0.04 + 0.12, role))
        return buffList, debuffList, advList, delayList
    
    