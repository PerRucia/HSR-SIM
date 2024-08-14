from Character import Character
from Lightcones.DanceAtSunset import Sunset
from Relics.WindSoaring import WindSoaringYunli
from Planars.Duran import Duran
from RelicStats import RelicStats
from Buff import Buff
from Result import Result
from Turn import Turn

class Yunli(Character):
    # Standard Character Settings
    name = "Yunli"
    path = "DES"
    element = "PHY"
    scaling = "ATK"
    baseHP = 1358.3
    baseATK = 679.14
    baseDEF = 460.85
    baseSPD = 94
    maxEnergy = 240
    ultCost = 120
    currAV = 0
    rotation = ["E", "A", "A"]
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0}
    
    # Unique Character Properties
    cullActive = False
    
    # Relic Settings
    relicStats = RelicStats(0, 0, 2, 2, 2, 2, 4, 4, 4, 4, 13, 11, "CR%", "ATK%", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str) -> None:
        super().__init__(pos, role)
        self.lightcone = Sunset(role, 1)
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
        bl, dbl, al, dl, *_ = super().useBsc(enemyID)
        return bl, dbl, al, dl, [Turn(self.name, self.role, enemyID, "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "Basic")]
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, *_ = super().useSkl(enemyID)
        return bl, dbl, al, dl, [Turn(self.name, self.role, enemyID, "BLAST", ["SKL"], [self.element], [1.2, 0.6], [20, 10], 30, self.scaling, -1, "Skill")]
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.cullActive = True
        bl, dbl, al, dl, *_ = super().useUlt(enemyID)
        return bl, dbl, al, dl, [Turn(self.name, self.role, enemyID, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "Ult")]
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, *_ = super().useFua(enemyID)
        if self.cullActive:
            self.cullActive = False
            turnList = [Turn(self.name, self.role, enemyID, "BLAST", ["ULT", "FUA"], [self.element], [2.2 , 1.1], [10, 10], 10, self.scaling, 0, "CullMain")]
            for _ in range(6):
                turnList.append(Turn(self.name, self.role, enemyID, "ST", ["ULT", "FUA"], [self.element], [0.72, 0], [2.5, 0], 0, self.scaling, 0, "CullBounce"))
            return bl, dbl, al, dl, turnList
        return bl, dbl, al, dl, [Turn(self.name, self.role, enemyID, "BLAST", ["FUA"], [self.element], [1.2, 0.6], [20, 10], 5, self.scaling, 0, "FUA")]
    
    def useHit(self, enemyID=-1):
        return self.useFua(enemyID)
    
    def ownTurn(self, result: Result):
        return super().ownTurn(result)
    
    def allyTurn(self, turn, result):
        return super().allyTurn(turn, result)
    
    