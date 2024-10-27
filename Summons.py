from Buff import *
from Delay import *
from Result import *
from Turn import Turn


class Summon:
    name = "Summon"
    element = None
    currSPD = 100
    currAV = 10000 / currSPD
    currEnergy = 0
    maxEnergy = 0
    
    def __init__(self, ownerRole: Role, role: Role) -> None:
        self.ownerRole = ownerRole
        self.role = role
        self.priority = 0
        
    @staticmethod
    def isChar() -> bool:
        return True

    @staticmethod
    def isSummon() -> bool:
        return True

    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        return [], [], [], [], []
    
    def standardAVred(self, av: float):
        self.currAV = max(0.0, self.currAV - av)
        
    def reduceAV(self, reduceValue: float):
        self.currAV = max(0.0, self.currAV - reduceValue)
        
    def allyTurn(self, turn: Turn, result: Result)-> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        return [], [], [], [], []
        
class Numby(Summon):
    name = "Numby"
    element = Element.FIRE
    scaling = Scaling.ATK
    currSPD = 80
    currAV = 10000 / currSPD
    
    def __init__(self, ownerRole: Role, role: Role) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, "NumbyGoGo"))
        return bl, dbl, al, dl, tl
    
class Fuyuan(Summon):
    name = "Fuyuan"
    element = Element.FIRE
    scaling = Scaling.ATK
    currSPD = 90
    currAV = 10000 / currSPD
    
    def __init__(self, ownerRole: Role, role: Role) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, "FuyuanGoGo"))
        return bl, dbl, al, dl, tl
    
class DeHenshin(Summon):
    name = "de-Henshin!"
    element = Element.FIRE
    scaling = Scaling.ATK
    currSPD = 1
    currAV = 10000
    
    def __init__(self, ownerRole: Role, role: Role) -> None:
        super().__init__(ownerRole, role)
        
    def takeTurn(self) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        self.currAV = 10000
        bl, dbl, al, dl, tl = super().takeTurn()
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, self.name))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay], list[Turn]]:
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveName == "FireflyUlt":
            self.currAV = 10000 / 70
        return bl, dbl, al, dl, tl
    
class LightningLord(Summon):
    name = "LightningLord"
    element = Element.LIGHTNING
    scaling = Scaling.ATK
    currSPD = 90 # max of 130 at 10 stacks
    currAV = 10000 / currSPD
    stacks = 6
    
    def __init__(self, ownerRole: Role, role: Role) -> None:
        super().__init__(ownerRole, role)
    
    def takeTurn(self):
        bl, dbl, al, dl, tl = super().takeTurn()
        paddedStacks = "0" + str(self.stacks) if self.stacks < 10 else str(self.stacks)
        tl.append(Turn(self.name, self.ownerRole, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 0, self.scaling, 0, f"LightningLordGoGo{paddedStacks}"))
        self.adjSpeed(60)
        self.stacks = 3
        return bl, dbl, al, dl, tl
        
    def allyTurn(self, turn, result):
        addStacks = 2 if turn.moveName == "JingYuanSkill" else (3 if turn.moveName == "JingYuanUlt" else 0)
        self.stacks = min(10, self.stacks + addStacks)
        self.adjSpeed(self.stacks * 10 + 30)
        return super().allyTurn(turn, result)

    def adjSpeed(self, spd):
        if spd == 60:
            self.currSPD = 60
            self.currAV = 10000 / self.currSPD
        else:
            self.currAV = self.currAV * (self.currSPD / spd)
            self.currSPD = spd