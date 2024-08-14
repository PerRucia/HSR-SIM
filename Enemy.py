# actionOrder = [1,1,2] means single attack, single attack, double attack

class Enemy:
    broken = False
    
    def __init__(self, enemyID: int, level: int, spd: float, toughness: int, actionOrder: list, weakness: list, adjacent: list):
        self.enemyID = enemyID
        self.name = f"Enemy {self.enemyID}"
        self.level = level
        self.spd = spd
        self.toughness = toughness
        self.gauge = self.toughness
        self.actionOrder = actionOrder
        self.weakness = weakness
        self.adjacent = adjacent
        self.currAV = 10000 / self.spd
        self.turn = 0
        self.maxToughnessMul = 0.5 + (self.toughness / 40)
        self.priority = 0
        
    def __str__(self) -> str:
        res = f"Enemy {self.enemyID} | LVL: {self.level} | SPD: {self.spd} | "
        res += f"Weakness: {self.weakness} | Toughness: {self.gauge}"
        return res
    
    def getUniMul(self) -> float:
        return 1.0 if self.broken else 0.9
    
    def redToughness(self, toughness: float) -> bool:
        self.gauge = max(self.gauge - toughness, 0)
        if self.gauge == 0:
            self.broken = True
            return True
        return False
    
    def recover(self):
        if self.broken:
            self.gauge = self.toughness
            self.broken = False
        
    def takeTurn(self) -> int:
        self.recover()
        res = self.turn
        self.turn = self.turn + 1
        return self.actionOrder[res % len(self.actionOrder)]
    
    def isChar(self) -> bool:
        return False
    
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0, self.currAV - reduceValue)
        
    def hasAdj(self) -> bool:
        return len(self.adjacent) > 0
    
    def getRes(self, element) -> float:
        return 0 if element in self.weakness else 0.2
        
        