class Result:
    def __init__(self, charName: str, charRole: str, atkType: list, eleType: list, broken: bool, turnDmg: float, wbDmg: float, errGain: float, turnName: str):
        self.charName = charName
        self.charRole = charRole
        self.atkType = atkType[0]
        self.eleType = eleType
        self.brokenEnemy = broken
        self.turnDmg = turnDmg
        self.wbDmg = wbDmg
        self.errGain = errGain
        self.turnName = turnName
        
    def __str__(self) -> str:
        return f"{self.turnName} | {self.charName} | {self.charRole} | DMG: {self.turnDmg:.3f} | WB: {self.brokenEnemy} | WB DMG: {self.wbDmg:.3f} | Energy: {self.errGain:.3f}"