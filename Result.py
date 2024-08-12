class Result:
    def __init__(self, charName: str, charRole: str, atkType: list, eleType: list, broken: bool, turnDmg: float, wbDmg: float):
        self.charName = charName
        self.charRole = charRole
        self.atkType = atkType[0]
        self.eleType = eleType
        self.brokenEnemy = broken
        self.turnDmg = turnDmg
        self.wbDmg = wbDmg
        
    def __str__(self) -> str:
        return f"DMG: {self.turnDmg} | WB: {self.brokenEnemy} | WB DMG: {self.wbDmg}"