from Character import Character
from Lightcones.ForTomorrowJourney import Journey
from Relics.Musketeer import Musketeer
from Relics.Prisoner import Prisoner
from Planars.Penacony import Penacony
from RelicStats import RelicStats
from Buff import Buff
from Result import Result, Special
from Turn import Turn
from Delay import *

class Robin(Character):
    # Standard Character Settings
    name = "Robin"
    path = "HAR"
    element = "PHY"
    scaling = "ATK"
    baseHP = 1280.7
    baseATK = 640.33
    baseDEF = 485.10
    baseSPD = 102
    maxEnergy = 160
    ultCost = 160
    currEnergy = 85
    currAV = 0
    rotation = ["E", "A"]
    dmgDct = {"BSC": 0, "ULT": 0, "BREAK": 0}
    hasSpecial = True
    
    # Unique Character Properties
    canBeAdv = True
    sameEleTeammates = ["DPS"]
    atkStat = 0
    
    # Relic Settings
    relicStats = RelicStats(11, 5, 6, 3, 7, 6, 6, 0, 0, 5, 0, 0, "ATK%", "ATK%", "ATK%", "ERR%")
    
    def __init__(self, pos: int, role: str) -> None:
        super().__init__(pos, role)
        self.lightcone = Journey(role, 5)
        self.relic1 = Musketeer(role, 2)
        self.relic2 = Prisoner(role, 2)
        self.planar = Penacony(role, self.sameEleTeammates)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.extend([Buff("RobinCD", "CD%", 0.2, "ALL", ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("RobinTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("RobinTraceHP", "HP%", 0.18, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("RobinTraceSPD", "SPD", 5, self.role, ["ALL"], 1, 1, "SELF", "PERM")
                         ])
        advList.append(Advance("RobinStartADV", self.role, 0.25))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "ST", ["BSC"], [self.element], [1.0, 0], [10, 0], 22, self.scaling, 1, "RobinBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "NA", ["SKL"], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "RobinSkill"))
        bl.append(Buff("RobinSklDMG", "DMG%", 0.5, "ALL", ["ALL"], 3, 1, "SELF", "START"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.canBeAdv = False
        self.currAV = 10000 / 90
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "NA", ["ULT"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RobinUlt"))
        al.append(Advance("RobinUltADV", "ALL", 1.0))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        concertoFilter = ["TYAllyBonus", "TYBeneBonus", "YunliCullBounce"]
        if (turn.moveName not in concertoFilter) and (turn.moveType != "NA"):
            if self.canBeAdv: # not in concerto state, only provide extra ERR
                tl.append(Turn(self.name, self.role, turn.targetID, "NA", ["ULT"], self.element, [0, 0], [0, 0], 2, self.scaling, 0, "RobinBonusERR"))
            else: # in concerto state, provide both additional dmg and extra ERR
                tl.append(Turn(self.name, self.role, turn.targetID, "NA", ["ULT"], self.element, [1.2, 0], [0, 0], 2, self.scaling, 0, "RobinConcertoDMG"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        return bl, dbl, al, dl, tl
    
    def reduceAV(self, reduceValue: float):
        if self.canBeAdv:
            self.currAV = max(0, self.currAV - reduceValue)
    
    def takeTurn(self) -> str:
        self.canBeAdv = True
        return super().takeTurn()
    
    def special(self):
        return "updateRobinATK"
    
    def handleSpecial(self, special: Special):
        self.atkStat = special.attr1
        bl, dbl, al, dl = super().handleSpecial(special)
        if not self.canBeAdv:
            bl.append(Buff("RobinUltBuff", "ATK", self.atkStat * 0.228 + 200, "ALL", ["ALL"], 1, 1, self.role, "START"))
        return bl, dbl, al, dl