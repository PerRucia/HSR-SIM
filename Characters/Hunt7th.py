import logging

from Buff import *
from Character import Character
from Delay import *
from Lightcones.Swordplay import Swordplay
from Planars.Rutilant import Rutilant
from RelicStats import RelicStats
from Relics.Musketeer import Musketeer
from Result import Result, Special
from Turn import Turn

logger = logging.getLogger(__name__)

class Hunt7th(Character):
    # Standard Character Settings
    name = "HuntM7"
    path = Path.HUNT
    element = Element.IMAGINARY
    scaling = Scaling.ATK
    baseHP = 1058.4
    baseATK = 564.48
    baseDEF = 441.00
    baseSPD = 102
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.EBSC: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    firstTurn = True
    masterElement = element
    ultEnhanced = False
    charges = 3
    fuaTrigger = True
    advanced = False
    
    ecount = 0
    ucount = 0
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, masterRole = Role.DPS, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 6, rotation = None, targetPrio = Priority.DEFAULT) -> None:
        super().__init__(pos, role, defaultTarget, eidolon, targetPrio)
        self.lightcone = lc if lc else Swordplay(role, 5)
        self.relic1 = r1 if r1 else Musketeer(role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else Rutilant(role)
        self.masterRole = masterRole
        self.relicStats = subs if subs else RelicStats(10, 2, 0, 2, 4, 0, 4, 4, 4, 4, 10, 4, Pwr.CR_PERCENT, Pwr.SPD, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        self.rotation = rotation if rotation else ["A"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        al.append(Advance("H7StartAdv", self.role, 0.25))
        if self.eidolon == 6:
            bl.append(Buff("H7enhancedBasicCD", Pwr.CD_PERCENT, 0.5, self.role, [AtkType.UEBSC], 1, 1, Role.SELF, TickDown.PERM)) # e6 buff
        bl.append(Buff("H7enhancedBasicDMG", Pwr.DMG_PERCENT, 0.88 if self.eidolon >= 5 else 0.8, self.role, [AtkType.EBSC], 1, 1, Role.SELF, TickDown.PERM)) # e6 buff
        bl.append(Buff("H7TraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("H7TraceCD", Pwr.CD_PERCENT, 0.24, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("H7TraceDEF", Pwr.DEF_PERCENT, 0.125, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3basic = 1.1 if self.eidolon >= 3 else 1.0
        e3bonus = 0.22 if self.eidolon >= 3 else 0.2
        e3enhanced = 0.88 if self.eidolon >= 3 else 0.8
        eMul = e3bonus + e3enhanced
        if self.charges >= 7:
            self.charges = self.charges - 7
            bl.append(Buff("H7MasterBuffCD", Pwr.CD_PERCENT, 0.60, self.masterRole, [AtkType.ALL], 2, 1, self.masterRole, TickDown.END))
            bl.append(Buff("H7MasterBuffBE", Pwr.BE_PERCENT, 0.36, self.masterRole, [AtkType.ALL], 2, 1, self.masterRole, TickDown.END))
            if self.ultEnhanced:
                self.ultEnhanced = False
                self.ucount += 1
                chance = 0.8 + 0.8**2 + 0.8**3
                # print("UltEBSC", self.ucount)
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.EBSC, AtkType.BSC, AtkType.UEBSC], [self.element, self.masterElement], [eMul, 0], [5, 0], 35, self.scaling, 0, "H7UltEnhancedBSC"))
                for _ in range(4):
                    tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.EBSC, AtkType.BSC, AtkType.UEBSC], [self.element, self.masterElement], [eMul, 0], [5, 0], 0, self.scaling, 0, "H7UltEnhancedBSCExtras"))
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.EBSC, AtkType.BSC, AtkType.UEBSC], [self.element, self.masterElement], [chance * eMul, 0], [9.76, 0], 0, self.scaling, 0, "H7UltEnhancedBSCExtras"))
            else:
                self.ecount += 1
                chance = 0.6 + 0.6**2 + 0.6**3
                # print("EBSC", self.ecount)
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.EBSC, AtkType.BSC], [self.element, self.masterElement], [eMul, 0], [5, 0], 35, self.scaling, 0, "H7EnhancedBSC"))
                for _ in range(2):
                    tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.EBSC, AtkType.BSC], [self.element, self.masterElement], [eMul, 0], [5, 0], 0, self.scaling, 0, "H7EnhancedBSCExtras"))
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.EBSC, AtkType.BSC], [self.element, self.masterElement], [chance * eMul, 0], [5.88, 0], 0, self.scaling, 0, "H7EnhancedBSCExtras"))
        else:
            self.charges = min(10, self.charges + 1)
            logger.warning(f"ALERT: H7 gained 1 charge from MarchBasic | Total: {self.charges}")
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element, self.masterElement], [e3basic + e3bonus, 0], [10, 0], 25, self.scaling, 1, "H7Basic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        extraErr = 30 if self.firstTurn else 0
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e3SPD = 0.108 if self.eidolon >= 3 else 0.10
        bl.append(Buff("H7MasterSPD", Pwr.SPD_PERCENT, e3SPD, self.masterRole, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 1:
            bl.append(Buff("H7SelfSPD", Pwr.SPD_PERCENT, 0.10, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        tl.append(Turn(self.name, self.role, -1, Targeting.NA, [AtkType.ALL], [self.element, self.masterElement], [0, 0], [0, 0], 35 + extraErr, self.scaling, -1, "H7Skill")) # e4 energy buff 30 + 5
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.ultEnhanced = True
        e5Mul = 2.592 if self.eidolon >= 5 else 2.4
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.ULT], [self.element, self.masterElement], [e5Mul, 0], [30, 0], 5, self.scaling, 0, "H7Ult"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if self.charges >= 7 and not self.advanced:
            self.advanced = True
            al.append(Advance("H7EnhancedADV", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if (turn.charRole == self.masterRole) and (turn.moveName not in bonusDMG) and (turn.targeting != Targeting.NA) and (not self.firstTurn):
            self.charges = min(10, self.charges + 1)
            logger.warning(f"ALERT: H7 gained 1 charge from {turn.moveName} | Total: {self.charges}")
            if self.fuaTrigger and (not AtkType.FUA in turn.atkType) and self.eidolon >= 2:
                self.charges = min(10, self.charges + 1)
                logger.warning(f"ALERT: H7 gained 1 charge from MarchFUA | Total: {self.charges}")
                self.fuaTrigger = False
                self.fuas = self.fuas + 1
                tl.append(Turn(self.name, self.role, result.enemiesHit[0].enemyID, Targeting.SINGLE, [AtkType.FUA], [self.element, self.masterElement], [0.6, 0], [1, 0], 5, self.scaling, 0, "MarchFUA"))
        if self.charges >= 7 and not self.advanced:
            self.advanced = True
            al.append(Advance("H7EnhancedADV", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        res = super().takeTurn()
        self.fuaTrigger = True
        self.advanced = False
        if self.firstTurn:
            self.firstTurn = False
            return "E"
        return res
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.masterElement = specialRes.attr1
        if self.firstTurn:
            bl.append(Buff("MarchBonusERR", Pwr.ERR_T, 30, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl, tl
    
    
    