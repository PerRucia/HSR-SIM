from Character import Character
from Lightcones.DanceAtSunset import Sunset
from Lightcones.Aeon import Aeon
from Relics.WindSoaring import WindSoaringYunli
from Planars.Duran import Duran
from RelicStats import RelicStats
from Buff import Buff
from Result import *
from Misc import *
from Turn import Turn

class Yunli(Character):
    # Standard Character Settings
    name = "Yunli"
    path = Path.DESTRUCTION
    element = Element.PHYSICAL
    scaling = Scaling.ATK
    baseHP = 1358.3
    baseATK = 679.14
    baseDEF = 460.85
    baseSPD = 94
    maxEnergy = 240
    ultCost = 120
    currAV = 0
    hasSpecial = True
    rotation = ["E"]
    dmgDct = {Move.BSC: 0, Move.FUA: 0, Move.SKL: 0, Move.ULT: 0, Move.BRK: 0}
    
    # Unique Character Properties
    cullActive = False
    skipHit = 0
    hits = 0
    
    # Relic Settings
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else Aeon(role)
        self.relic1 = r1 if r1 else WindSoaringYunli(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Duran(role)
        self.currEnergy = self.maxEnergy / 2
        self.relicStats = subs if subs else RelicStats(0, 0, 2, 2, 2, 2, 4, 4, 4, 4, 13, 11, Pwr.CR_PERCENT, Pwr.ATK_PERCENT, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.extend([Buff("YunliSelfATK", Pwr.ATK_PERCENT, 0.3, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("YunliSelfCD", Pwr.CD_PERCENT, 1.0, self.role, [Move.ULT], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("YunliTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("YunliTraceHP", Pwr.HP_PERCENT, 0.18, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM),
                         Buff("YunliTraceCR", Pwr.CR_PERCENT, 0.067, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM)
                         ])
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.BSC], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "YunliBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.BLAST, [Move.SKL], [self.element], [1.2, 0.6], [20, 10], 30, self.scaling, -1, "YunliSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.cullActive = True
        bl, dbl, al, dl, *_ = super().useUlt(enemyID)
        return bl, dbl, al, dl, [Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "YunliUlt")]
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, *_ = super().useFua(enemyID)
        if self.cullActive:
            self.fuas = self.fuas - 1
            self.cullActive = False
            turnList = [Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.BLAST, [Move.ULT, Move.FUA], [self.element], [2.2 , 1.1], [10, 10], 10, self.scaling, 0, "YunliCullMain")]
            for _ in range(6):
                turnList.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.ULT, Move.FUA], [self.element], [0.72, 0], [2.5, 0], 0, self.scaling, 0, "YunliCullBounce"))
            return bl, dbl, al, dl, turnList
        return bl, dbl, al, dl, [Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.BLAST, [Move.FUA], [self.element], [1.2, 0.6], [20, 10], 5, self.scaling, 0, "YunliFUA")]
    
    def useHit(self, enemyID=-1):
        self.hits = self.hits + 1
        if self.hits / self.skipHit != 0:
            bl, dbl, al, dl, tl = self.useFua(enemyID)
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.ALL], [self.element], [0, 0], [0, 0], 15, self.scaling, 0, "YunliHitERR"))
            return bl, dbl, al, dl, tl
        return super().useHit(enemyID)
    
    def special(self):
        return "Yunli"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.skipHit = round(1 / (1 - specialRes.attr1))
        self.hasSpecial = False
        tl.append(Turn(self.name, self.role, self.defaultTarget, AtkTarget.BLAST, [Move.ULT, Move.FUA], [self.element], [2.2 , 1.1], [10, 10], 10, self.scaling, 0, "YunliCullMain"))
        for _ in range(6):
            tl.append(Turn(self.name, self.role, self.defaultTarget, AtkTarget.SINGLE, [Move.ULT, Move.FUA], [self.element], [0.72, 0], [2.5, 0], 0, self.scaling, 0, "YunliCullBounce"))
        return bl, dbl, al, dl, tl
    