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
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0}
    
    # Unique Character Properties
    cullActive = False
    skipHit = 0
    hits = 0
    
    # Relic Settings
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Sunset(role)
        self.relic1 = r1 if r1 else WindSoaringYunli(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Duran(role)
        self.currEnergy = self.maxEnergy / 2
        self.relicStats = subs if subs else RelicStats(0, 2, 0, 2, 4, 0, 4, 4, 4, 4, 12, 12, Pwr.CR_PERCENT, Pwr.ATK_PERCENT, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("YunliSelfATK", Pwr.ATK_PERCENT, 0.3, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("YunliUltCD", Pwr.CD_PERCENT, 1.08 if self.eidolon >= 3 else 1.0, self.role, [AtkType.ULT], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("YunliTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("YunliTraceHP", Pwr.HP_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("YunliTraceCR", Pwr.CR_PERCENT, 0.067, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))      
        if self.eidolon >= 1:
            bl.append(Buff("YunliE1DMG", Pwr.DMG_PERCENT, 0.20, self.role, atkType=[AtkType.ULT]))
        if self.eidolon >= 2:
            bl.append(Buff("YunliE2Shred", Pwr.SHRED, 0.20, self.role, atkType=[AtkType.FUA]))
        if self.eidolon == 6:
            bl.append(Buff("YunliE6CR", Pwr.CR_PERCENT, 0.15, self.role, atkType=[AtkType.ULT]))
            bl.append(Buff("YunliE6Pen", Pwr.PHYPEN, 0.20, self.role, atkType=[AtkType.ULT]))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        e3Mul = 1.1 if self.eidolon >= 3 else 1.0
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Mul, 0], [10, 0], 20, self.scaling, 1, "YunliBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e5Mul = 1.32 if self.eidolon >= 5 else 1.2
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.SKL], [self.element], [e5Mul, e5Mul / 2], [20, 10], 30, self.scaling, -1, "YunliSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.cullActive = True
        bl, dbl, al, dl, *_ = super().useUlt(enemyID)
        return bl, dbl, al, dl, [Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "YunliUlt")]
    
    def useFua(self, enemyID=-1):
        e3Mul = 2.376 if self.eidolon >= 3 else 2.2
        e3Mul2 = 0.7776 if self.eidolon >= 3 else 0.72
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        if self.cullActive:
            self.fuas = self.fuas - 1
            self.cullActive = False
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.ULT, AtkType.FUA], [self.element], [e3Mul, e3Mul / 2], [10, 10], 10, self.scaling, 0, "YunliCullMain"))
            numHits = 9 if self.eidolon >= 1 else 6
            for _ in range(numHits):
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.ULT, AtkType.FUA], [self.element], [e3Mul2, 0], [2.5, 0], 0, self.scaling, 0, "YunliCullBounce"))
            if self.eidolon >= 4:
                bl.append(Buff("YunliE4ERS", Pwr.ERS_PERCENT, 0.4, self.role, turns=1, tdType=TickDown.END))
        else:
            e5Mul = 1.32 if self.eidolon >= 5 else 1.2
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.FUA], [self.element], [e5Mul, e5Mul / 2], [20, 10], 5, self.scaling, 0, "YunliFUA"))
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        self.hits = self.hits + 1
        if self.hits / self.skipHit != 0:
            bl, dbl, al, dl, tl = self.useFua(enemyID)
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 15, self.scaling, 0, "YunliHitERR"))
            return bl, dbl, al, dl, tl
        return super().useHit(enemyID)
    
    def special(self):
        return "Yunli"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.skipHit = round(1 / (1 - specialRes.attr1))
        self.hasSpecial = False
        tl.append(Turn(self.name, self.role, self.defaultTarget, Targeting.BLAST, [AtkType.ULT, AtkType.FUA], [self.element], [2.2 , 1.1], [10, 10], 10, self.scaling, 0, "YunliCullMain"))
        for _ in range(6):
            tl.append(Turn(self.name, self.role, self.defaultTarget, Targeting.SINGLE, [AtkType.ULT, AtkType.FUA], [self.element], [0.72, 0], [2.5, 0], 0, self.scaling, 0, "YunliCullBounce"))
        return bl, dbl, al, dl, tl
    