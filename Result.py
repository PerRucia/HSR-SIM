class Result:
    def __init__(self, charName: str, charRole: str, atkType: list, eleType: list, broken: bool, turnDmg: float, wbDmg: float, errGain: float, turnName: str, enemiesHit: list[int], preHitStatus: list[bool]):
        self.charName = charName
        self.charRole = charRole
        self.atkType = atkType
        self.eleType = eleType
        self.brokenEnemy = broken
        self.turnDmg = turnDmg
        self.wbDmg = wbDmg
        self.errGain = errGain
        self.turnName = turnName
        self.enemiesHit = enemiesHit
        self.preHitStatus = preHitStatus
        
    def __str__(self) -> str:
        return f"{self.turnName} | {self.charName} | {self.charRole.name} | DMG: {self.turnDmg:.3f} | Enemies Hit: {self.enemiesHit} | Enemies Broken: {self.brokenEnemy} | WB DMG: {self.wbDmg:.3f} | Energy: {self.errGain:.3f}"
    
class Special:
    def __init__(self, name: str, attr1=None, attr2=None, attr3=None, attr4=None):
        self.specialName = name
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3
        self.attr4 = attr4
        
    def __str__(self) -> str:
        return f"{self.specialName} | Attr1: {self.attr1} | Attr2: {self.attr2} | Attr3: {self.attr3} | Attr4: {self.attr4}"