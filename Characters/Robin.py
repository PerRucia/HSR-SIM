from Character import Character
from Lightcones.ForTomorrowJourney import Journey
from Lightcones.Nightglow import Nightglow
from Relics.Musketeer import Musketeer
from Relics.Prisoner import Prisoner
from Planars.Lushaka import Lushaka
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import Buff
from Result import Result, Special
from Turn import Turn
from Delay import *
from Misc import *

class Robin(Character):
    # Standard Character Settings
    name = "Robin"
    path = Path.HARMONY
    element = Element.PHYSICAL
    scaling = Scaling.ATK
    baseHP = 1280.7
    baseATK = 640.33
    baseDEF = 485.10
    baseSPD = 102
    maxEnergy = 160
    ultCost = 160
    currEnergy = 80
    currAV = 0
    rotation = ["E", "A", "A"]
    dmgDct = {"BSC": 0, "ULT": 0, "BREAK": 0}
    hasSpecial = True
    
    # Unique Character Properties
    canBeAdv = True
    sameEleTeammates = []
    atkStat = 0
    canUlt = False
    techErr = True
    
    # Relic Settings
    relicStats = RelicStats(14, 5, 6, 3, 7, 6, 6, 0, 0, 5, 0, 0, "ATK%", "ATK%", "ATK%", "ERR%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, eidolon=0) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Journey(role)
        self.relic1 = Musketeer(role, 2)
        self.relic2 = Prisoner(role, 2)
        self.planar = Lushaka(role, Role.DPS)
        self.eidolon = eidolon
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("RobinCD", "CD%", 0.2, Role.ALL, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("RobinTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("RobinTraceHP", "HP%", 0.18, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("RobinTraceSPD", "SPD", 5, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        advList.append(Advance("RobinStartADV", self.role, 0.25))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e2ERR = 1 if self.eidolon >= 2 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["BSC"], [self.element], [1.0, 0], [10, 0], 22 + e2ERR, self.scaling, 1, "RobinBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, ["SKL"], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "RobinSkill"))
        bl.append(Buff("RobinSklDMG", "DMG%", 0.5, Role.ALL, ["ALL"], 3, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.canBeAdv = False
        self.currAV = 10000 / 90
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        bl.append(Buff("RobinFuaCD", "CD%", 0.25, Role.ALL, ["FUA"], 1, 1, self.role, TickDown.START))
        if self.eidolon >= 1:
            bl.append(Buff("RobinE1Pen", "PEN", 0.24, Role.ALL, ["ALL"], 1, 1, self.role, TickDown.START))
        if self.eidolon >= 2:
            bl.append(Buff("RobinE2SPD", "SPD%", 0.16, Role.ALL, ["FUA"], 1, 1, self.role, TickDown.START)) 
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, ["ULT"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RobinUlt"))
        al.append(Advance("RobinUltADV", Role.ALL, 1.0))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        e2ERR = 1 if self.eidolon >= 2 else 0
        if (turn.moveName not in bonusDMG) and (turn.moveType != AtkTarget.NA):
            if self.canBeAdv: # not in concerto state, only provide extra ERR
                tl.append(Turn(self.name, self.role, turn.targetID, AtkTarget.NA, ["ULT"], [self.element], [0, 0], [0, 0], 2 + e2ERR, self.scaling, 0, "RobinBonusERR"))
            else: # in concerto state, provide both additional dmg and extra ERR
                tl.append(Turn(self.name, self.role, result.enemiesHit[0], AtkTarget.NA, ["ULT"], [self.element], [1.2, 0], [0, 0], 2 + e2ERR, self.scaling, 0, "RobinConcertoDMG"))
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
    
    def handleSpecialStart(self, special: Special):
        self.atkStat = special.attr1        
        bl, dbl, al, dl, tl = super().handleSpecialStart(special)
        if self.techErr:
            self.techErr = False
            tl.append(Turn(self.name, self.role, self.defaultTarget, AtkTarget.NA, ["BSC"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RobinTechEnergy"))
        if not self.canBeAdv:
            bl.append(Buff("RobinUltBuff", "ATK", self.atkStat * 0.228 + 200, Role.ALL, ["ALL"], 1, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def handleSpecialEnd(self, specialRes: Special):
        self.canUlt = specialRes.attr1
        return super().handleSpecialEnd(specialRes)
    
    def canUseUlt(self) -> bool:
        if self.currEnergy >= self.ultCost and self.canUlt:
            return True
        return False