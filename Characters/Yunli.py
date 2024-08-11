from Character import Character
from Lightcones.DanceAtSunset import Sunset
from Relics.WindSoaring import WindSoaring
from Planars.Duran import Duran
from Buff import Buff
from Turn import Turn

class Yunli(Character):
    name = "Yunli"
    path = "DES"
    element = "PHY"
    scaling = "ATK"
    baseHP = 1358.3
    baseATK = 679.14
    baseDEF = 460.85
    baseSPD = 94
    maxEnergy = 240
    currEnergy = 240 / 2
    cullActive = False
    
    def __init__(self, pos: int, role: str) -> None:
        super().__init__(pos, role)
        self.lightcone = Sunset(role, 1)
        self.relic1 = WindSoaring(role, 4)
        self.relic2 = None
        self.planar = Duran(role)
        
    def equip(self):
        buffList, debuffList, advList, spdList = super().equip()
        buffList.extend([Buff("YunliSelfATK", "ATK%", 0.3, self.role, ["ALL"], 1000, 1),
                         Buff("YunliSelfCD", "CD%", 1.0, self.role, ["ULT"], 1000, 1),
                         Buff("YunliTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1000, 1),
                         Buff("YunliTraceHP", "HP%", 0.18, self.role, ["ALL"], 1000, 1),
                         Buff("YunliTraceCR", "CR%", 0.067, self.role, ["ALL"], 1000, 1)
                         ])
        return buffList, debuffList, advList, spdList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, sl, *_ = super().useBsc(enemyID)
        return bl, dbl, al, sl, Turn(self.name, -1, "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 20, self.scaling)
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, sl, *_ = super().useSkl(enemyID)
        return bl, dbl, al, sl, Turn(self.name, -1, "BLAST", ["SKL"], [self.element], [1.2, 0.6], [20, 10], 30, self.scaling)
    
    def useUlt(self, enemyID=-1):
        self.cullActive = True
        bl, dbl, al, sl, *_ = super().useSkl(enemyID)
        return bl, dbl, al, sl, Turn(self.name, -1, "NA", [], [self.element], [0, 0], [0, 0], 5, self.scaling)
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, sl, *_ = super().useFua(enemyID)
        if self.cullActive:
            self.cullActive = False
            return bl, dbl, al, sl, Turn(self.name, enemyID, "BLAST", ["FUA", "ULT"], [self.element], [6.52 , 1.1], [25, 10], 10, self.scaling)
        return bl, dbl, al, sl, Turn(self.name, enemyID, "BLAST", ["FUA"], [self.element], [1.2, 0.6], [20, 10], 5, self.scaling)
    
    def useHit(self, enemyID=-1):
        return self.useFua(enemyID)
    
    def allyTurn(self, turn, result):
        return super().allyTurn(turn, result)
    
    