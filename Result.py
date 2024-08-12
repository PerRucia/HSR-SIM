class Result:
    def __init__(self, source: str, atkType: list, eleType: list, broken: bool, turnDmg: float, wbDmg: float):
        self.source = source
        self.atkType = atkType[0]
        self.eleType = eleType
        self.brokenEnemy = broken
        self.turnDmg = turnDmg
        self.wbDmg = wbDmg