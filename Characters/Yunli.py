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
    element = "PHY"
    scaling = "ATK"
    baseHP = 1358.3
    baseATK = 679.14
    baseDEF = 460.85
    baseSPD = 94
    maxEnergy = 240
    ultCost = 120
    currAV = 0
    hasSpecial = True
    rotation = ["E", "A"]
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0}
    
    # Unique Character Properties
    cullActive = False
    aggroMultiplier = 0
    hitMultiplier = 0
    
    # Relic Settings
    relicStats = RelicStats(0, 0, 2, 2, 2, 2, 4, 4, 4, 4, 13, 11, "CR%", "ATK%", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Aeon(role, 5)
        self.relic1 = WindSoaringYunli(role, 4)
        self.relic2 = None
        self.planar = Duran(role)
        self.currEnergy = self.maxEnergy / 2
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.extend([Buff("YunliSelfATK", "ATK%", 0.3, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("YunliSelfCD", "CD%", 1.0, self.role, ["ULT"], 1, 1, "SELF", "PERM"),
                         Buff("YunliTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("YunliTraceHP", "HP%", 0.18, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("YunliTraceCR", "CR%", 0.067, self.role, ["ALL"], 1, 1, "SELF", "PERM")
                         ])
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "YunliBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "BLAST", ["SKL"], [self.element], [1.2, 0.6], [20, 10], 30, self.scaling, -1, "YunliSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.cullActive = True
        bl, dbl, al, dl, *_ = super().useUlt(enemyID)
        return bl, dbl, al, dl, [Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["ULT"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "YunliUlt")]
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, *_ = super().useFua(enemyID)
        if self.cullActive:
            self.fuas = self.fuas - 1
            self.cullActive = False
            turnList = [Turn(self.name, self.role, self.getTargetID(enemyID), "BLAST", ["ULT", "FUA"], [self.element], [2.2 , 1.1], [10, 10], 10, self.scaling, 0, "YunliCullMain")]
            for _ in range(6):
                turnList.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA"], [self.element], [0.72, 0], [2.5, 0], 0, self.scaling, 0, "YunliCullBounce"))
            return bl, dbl, al, dl, turnList
        return bl, dbl, al, dl, [Turn(self.name, self.role, self.getTargetID(enemyID), "BLAST", ["FUA"], [self.element], [1.2, 0.6], [20, 10], 5, self.scaling, 0, "YunliFUA")]
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = self.useFua(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["ALL"], [self.element], [0, 0], [0, 0], 15, self.scaling, 0, "YunliHitERR"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        return super().ownTurn(result)
    
    def allyTurn(self, turn: Result, result: Result):
        return super().allyTurn(turn, result)
    
    def gettotalDMG(self) -> tuple[str, float]:
        ttl = 0
        res = ""
        actMul = self.hitMultiplier + self.aggroMultiplier * (1 - self.hitMultiplier)
        for key, val in self.dmgDct.items():
            if key == "FUA" or key == "ULT":
                ttl += val * actMul
            else:
                ttl += val
        for key, val in self.dmgDct.items():
            res += f"-{key}: {val:.3f} | {val / ttl * 100:.3f}% | DPAV: {val / 5050:.3f}\n"
        return res, ttl
    
    def special(self):
        return "getYunliAggro"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.aggroMultiplier = specialRes.attr1
        self.hasSpecial = False
        tl.append(Turn(self.name, self.role, self.defaultTarget, "BLAST", ["ULT", "FUA"], [self.element], [2.2 , 1.1], [10, 10], 10, self.scaling, 0, "YunliCullMain"))
        for _ in range(6):
            tl.append(Turn(self.name, self.role, self.defaultTarget, "ST", ["ULT", "FUA"], [self.element], [0.72, 0], [2.5, 0], 0, self.scaling, 0, "YunliCullBounce"))
        return bl, dbl, al, dl, tl
    