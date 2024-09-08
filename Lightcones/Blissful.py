from Buff import *
from Lightcone import Lightcone
from Result import Result
from Turn import *


# noinspection DuplicatedCode
class Blissful(Lightcone):
    name = "Worrisome, Blissful"
    path = Path.HUNT
    baseHP = 1058.4
    baseATK = 582.12
    baseDEF = 463.05

    def __init__(self, wearerRole, level: int = 1, defaultTarget: int = 0):
        super().__init__(wearerRole, level)
        self.defaultTarget = defaultTarget    
    
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        crBuff = self.level * 0.03 + 0.15
        buffList.append(Buff("BlissfulCR", Pwr.CR_PERCENT, crBuff, self.wearerRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        dmgBuff = self.level * 0.05 + 0.25
        buffList.append(Buff("BlissfulDMG", Pwr.DMG_PERCENT, dmgBuff, self.wearerRole, [AtkType.FUA], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl = super().useFua(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl


# noinspection DuplicatedCode
class BlissfulTopaz(Blissful):
    def __init__(self, wearerRole, level: int = 1, defaultTarget: int = 0):
        super().__init__(wearerRole, level)
        self.defaultTarget = defaultTarget
          
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl = super().useBsc(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().ownTurn(turn, result)
        if result.turnName == "NumbyGoGo":
            cdBuff = self.level * 0.02 + 0.10
            dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl


# noinspection DuplicatedCode
class BlissfulFeixiao(Blissful):
    def __init__(self, wearerRole, level: int = 1, defaultTarget: int = 0):
        super().__init__(wearerRole, level)
        self.defaultTarget = defaultTarget
          
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl


# noinspection DuplicatedCode
class BlissfulMoze(Blissful):
    def __init__(self, wearerRole, level: int = 1, defaultTarget: int = 0):
        super().__init__(wearerRole, level)
        self.defaultTarget = defaultTarget
          
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl = super().useSkl(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl = super().useUlt(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl = super().useFua(enemyID)
        cdBuff = self.level * 0.02 + 0.10
        dbl.append(Debuff(f"BlissfulTame{self.wearerRole.name}", self.wearerRole, Pwr.CD_PERCENT, cdBuff, self.defaultTarget, [AtkType.ALL], 1000, 2, False, [0, 0], False))
        return bl, dbl, al, dl
    
    