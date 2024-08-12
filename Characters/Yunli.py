from Character import Character
from Lightcones.DanceAtSunset import Sunset
from Relics.WindSoaring import WindSoaring
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
    currEnergy = 240 / 2
    currAV = 0
    rotation = ["E", "A", "A"]
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0}
    
    # Unique Character Properties
    cullActive = False
    
    # Relic Settings
    relicStats = RelicStats(0, 0, 2, 2, 2, 2, 4, 4, 4, 4, 12, 12, "CR%", "ATK%", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str) -> None:
        super().__init__(pos, role)
        self.lightcone = Sunset(role, 1)
        self.relic1 = WindSoaring(role, 4)
        self.relic2 = None
        self.planar = Duran(role)
        
    def equip(self):
        buffList, debuffList, advList = super().equip()
        buffList.extend([Buff("YunliSelfATK", "ATK%", 0.3, self.role, ["ALL"], 1000, 1, "SELF"),
                         Buff("YunliSelfCD", "CD%", 1.0, self.role, ["ULT"], 1000, 1, "SELF"),
                         Buff("YunliTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1000, 1, "SELF"),
                         Buff("YunliTraceHP", "HP%", 0.18, self.role, ["ALL"], 1000, 1, "SELF"),
                         Buff("YunliTraceCR", "CR%", 0.067, self.role, ["ALL"], 1000, 1, "SELF")
                         ])
        return buffList, debuffList, advList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, *_ = super().useBsc(enemyID)
        return bl, dbl, al, Turn(self.name, self.role, -1, "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1)
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, *_ = super().useSkl(enemyID)
        return bl, dbl, al, Turn(self.name, self.role, -1, "BLAST", ["SKL"], [self.element], [1.2, 0.6], [20, 10], 30, self.scaling, -1)
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.cullActive = True
        bl, dbl, al, *_ = super().useSkl(enemyID)
        return bl, dbl, al, Turn(self.name, self.role, -1, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling, 0)
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, *_ = super().useFua(enemyID)
        if self.cullActive:
            self.cullActive = False
            return bl, dbl, al, Turn(self.name, self.role, enemyID, "BLAST", ["ULT", "FUA"], [self.element], [6.52 , 1.1], [25, 10], 10, self.scaling, 0)
        return bl, dbl, al, Turn(self.name, self.role, enemyID, "BLAST", ["FUA"], [self.element], [1.2, 0.6], [20, 10], 5, self.scaling, 0)
    
    def useHit(self, enemyID=-1):
        return self.useFua(enemyID)
    
    def ownTurn(self, result: Result):
        return super().ownTurn(result)
    
    def allyTurn(self, turn, result):
        return super().allyTurn(turn, result)
    
    