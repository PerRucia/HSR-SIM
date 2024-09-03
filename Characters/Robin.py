from Character import Character
from Lightcones.ForTomorrowJourney import Journey
from Lightcones.Nightglow import Nightglow
from Lightcones.PoisedToBloom import PoisedToBloom
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
    dmgDct = {AtkType.BSC: 0, AtkType.SPECIAL: 0, AtkType.BRK: 0}
    hasSpecial = True
    
    # Unique Character Properties
    canBeAdv = True
    sameEleTeammates = []
    moonlessMidnight = 0
    atkStat = 0
    canUlt = False
    techErr = True
    
    # Relic Settings
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, eidolon=0, lc = None, r1 = None, r2 = None, pl = None, subs = None, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Journey(role)
        self.relic1 = r1 if r1 else Musketeer(role, 2)
        self.relic2 = r2 if r2 else Prisoner(role, 2)
        self.planar = pl if pl else Lushaka(role, Role.DPS)
        self.relicStats = subs if subs else RelicStats(10, 4, 4, 4, 4, 10, 3, 3, 3, 3, 0, 0, Pwr.ATK_PERCENT, Pwr.ATK_PERCENT, Pwr.ATK_PERCENT, Pwr.ERR_PERCENT)
        self.rotation = rotation if rotation else ["E", "A", "A"]
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("RobinCD", Pwr.CD_PERCENT, 0.23 if self.eidolon >= 5 else 0.2, Role.ALL, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("RobinTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("RobinTraceHP", Pwr.HP_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("RobinTraceSPD", Pwr.SPD, 5, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        advList.append(Advance("RobinStartADV", self.role, 0.25))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e2ERR = 3 if self.eidolon >= 2 else 2
        e5Mul = 1.1 if self.eidolon >= 5 else 1
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Mul, 0], [10, 0], 20 + e2ERR, self.scaling, 1, "RobinBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e3Dmg = 0.55 if self.eidolon >= 3 else 0.5
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "RobinSkill"))
        bl.append(Buff("RobinSklDMG", Pwr.DMG_PERCENT, e3Dmg, Role.ALL, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        self.canBeAdv = False
        self.currAV = 10000 / 90
        self.moonlessMidnight = 8
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        bl.append(Buff("RobinFuaCD", Pwr.CD_PERCENT, 0.25, Role.ALL, [AtkType.FUA], 1, 1, self.role, TickDown.START))
        if self.eidolon >= 1:
            bl.append(Buff("RobinE1Pen", Pwr.PEN, 0.24, Role.ALL, [AtkType.ALL], 1, 1, self.role, TickDown.START))
        if self.eidolon >= 2:
            bl.append(Buff("RobinE2SPD", Pwr.SPD_PERCENT, 0.16, Role.ALL, [AtkType.FUA], 1, 1, self.role, TickDown.START)) 
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RobinUlt"))
        al.append(Advance("RobinUltADV", Role.ALL, 1.0))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        e2ERR = 3 if self.eidolon >= 2 else 2
        e3Mul = 1.296 if self.eidolon >= 3 else 1.2
        if (turn.moveName not in bonusDMG) and (turn.targeting != Targeting.NA):
            if self.canBeAdv: # not in concerto state, only provide extra ERR
                tl.append(Turn(self.name, self.role, turn.targetID, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], e2ERR, self.scaling, 0, "RobinBonusERR"))
            else: # in concerto state, provide both additional dmg and extra ERR
                if self.eidolon == 6 and self.moonlessMidnight > 0:
                    self.moonlessMidnight = self.moonlessMidnight - 1
                    tl.append(Turn(self.name, self.role, result.enemiesHit[0], Targeting.SPECIAL, [AtkType.SPECIAL], [self.element], [e3Mul, 0], [0, 0], e2ERR, self.scaling, 0, "RobinMoonlessMidnight"))
                else:
                    tl.append(Turn(self.name, self.role, result.enemiesHit[0], Targeting.SPECIAL, [AtkType.SPECIAL], [self.element], [e3Mul, 0], [0, 0], e2ERR, self.scaling, 0, "RobinConcertoDMG"))
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
        e3Mul = 0.24332 if self.eidolon >= 3 else 0.228
        e3Flat = 230 if self.eidolon >= 3 else 200
        if self.techErr:
            self.techErr = False
            tl.append(Turn(self.name, self.role, self.defaultTarget, Targeting.NA, [AtkType.BSC], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RobinTechEnergy"))
        if not self.canBeAdv:
            bl.append(Buff("RobinUltBuff", Pwr.ATK, self.atkStat * e3Mul + e3Flat, Role.ALL, [AtkType.ALL], 1, 1, self.role, TickDown.START))
            if self.eidolon >= 4:
                bl.append(Buff("RobinE4ERS", Pwr.ERS_PERCENT, 0.5, Role.ALL, turns=1, tickDown=self.role, tdType=TickDown.START))
        return bl, dbl, al, dl, tl
    
    def handleSpecialEnd(self, specialRes: Special):
        self.canUlt = specialRes.attr1
        return super().handleSpecialEnd(specialRes)
    
    def canUseUlt(self) -> bool:
        if self.currEnergy >= self.ultCost and self.canUlt:
            return True
        return False