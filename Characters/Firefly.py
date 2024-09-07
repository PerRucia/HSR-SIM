from Character import Character
from RelicStats import RelicStats
from Lightcones.Whereabouts import WhereaboutsFF
from Relics.IronCavalry import CavalryFirefly
from Planars.Kalpagni import KalpagniFirefly
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Firefly(Character):
    # Standard Character Settings
    name = "Firefly"
    path = Path.DESTRUCTION
    element = Element.FIRE 
    scaling = Scaling.ATK
    baseHP = 815.0
    baseATK = 523.91
    baseDEF = 776.16
    baseSPD = 104
    maxEnergy = 240
    currEnergy = 120
    ultCost = 240
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.SKL: 0, AtkType.SBK: 0, AtkType.BRK: 0, AtkType.TECH: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    hasSummon = True
    tech = True
    
    atkStat = 0
    beStat = 0
    enhancedState = False
    e2Counter = 0
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else WhereaboutsFF(role)
        self.relic1 = r1 if r1 else CavalryFirefly(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else KalpagniFirefly(role)
        self.relicStats = subs if subs else RelicStats(7, 4, 0, 4, 4, 0, 4, 27, 4, 4, 0, 0, Pwr.ATK_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.BE_PERCENT)
        self.rotation = rotation if rotation else ["E"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("FireflyTraceBE", Pwr.BE_PERCENT, 0.373, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("FireflyTraceERS", Pwr.ERS_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("FireflyTraceSPD", Pwr.SPD, 5, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        if self.enhancedState:
            superBrkScale = 0.50 if self.beStat >= 3.6 else (0.35 if self.beStat >= 2.0 else 0)
            e3Scg = 2.2 if self.eidolon >= 3 else 2.0
            for _ in range(4):
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.STSB, [AtkType.SBK, AtkType.BRK], [self.element], [superBrkScale, 0], [15 * 0.15, 0], 0, self.scaling, 0, "SamBasicSB"))
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Scg * 0.15, 0], [15 * 0.15, 0], 0, self.scaling, 0, "SamBasic", True, 0.55))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.STSB, [AtkType.SBK, AtkType.BRK], [self.element], [superBrkScale, 0], [15 * 0.4, 0], 0, self.scaling, 0, "SamBasicSB"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Scg * 0.4, 0], [15 * 0.4, 0], 0, self.scaling, 1, "SamBasicFinal", True, 0.55))
        else:
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "FireflyBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        if self.eidolon >= 1:
            bl.append(Buff("FireflyE1Shred", Pwr.SHRED, 0.15, self.role, tdType=TickDown.END))
        if self.enhancedState:
            spUsed = 0 if self.eidolon >= 1 else 1
            scgMain = self.beStat * 0.2 + (2.2 if self.eidolon >= 3 else 2.0)
            scgAdj = self.beStat * 0.1 + (1.1 if self.eidolon >= 3 else 1.0)
            superBrkScale = 0.50 if self.beStat >= 3.6 else (0.35 if self.beStat >= 2.0 else 0)
            for _ in range(4):
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLASTSB, [AtkType.SBK, AtkType.BRK], [self.element], [superBrkScale, superBrkScale], [30 * 0.15, 10 * 0.15], 0, self.scaling, 0, "SamSkillSB"))
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLAST, [AtkType.SKL], [self.element], [scgMain * 0.15, scgAdj * 0.15], [30 * 0.15, 10 * 0.15], 0, self.scaling, 0, "SamSkill", True, 0.55))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLASTSB, [AtkType.SBK, AtkType.BRK], [self.element], [superBrkScale, superBrkScale], [30 * 0.4, 10 * 0.4], 0, self.scaling, 0, "SamSkillSB"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLAST, [AtkType.SKL], [self.element], [scgMain * 0.4, scgAdj * 0.4], [30 * 0.4, 10 * 0.4], 0, self.scaling, -spUsed, "SamSkillFinal", True, 0.55))
        else:
            e3Err = 0.62 if self.eidolon >= 3 else 0.6
            e3Scg = 2.2 if self.eidolon >= 3 else 2.0
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.SKL], [self.element], [e3Scg * 0.4, 0], [20 * 0.4, 0], 0, self.scaling, 0, "FireflySkillP1"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.SKL], [self.element], [e3Scg * 0.6, 0], [20 * 0.6, 0], 30, self.scaling, -1, "FireflySkillP2"))
            bl.append(Buff("FireSkillERR", Pwr.ERR_F, self.ultCost * e3Err, self.role, [AtkType.SPECIAL], 1, 1, Role.SELF, TickDown.PERM))
            al.append(Advance("FireflySkill", self.role, 0.25))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.enhancedState = True
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "FireflyUlt"))
        brkBoost = 0.22 if self.eidolon >= 5 else 0.2
        spdBoost = 66 if self.eidolon >= 5 else 60
        wbeBoost = 1.0 if self.eidolon == 6 else 0.5
        bl.append(Buff("SamBrkDmgBoost", Pwr.BRK_DMG, brkBoost, self.role, [AtkType.BRK], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("SamSPDBoost", Pwr.SPD, spdBoost, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("SamWBEBoost", Pwr.WB_EFF, wbeBoost, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        al.append(Advance("FireflyUlt", self.role, 1.0))
        if self.eidolon == 6:
            bl.append(Buff("SamE6Pen", Pwr.FIRPEN, 0.2, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if result.turnName == "de-Henshin!":
            self.enhancedState = False
            bl.append(Buff("SamBrkDmgBoost", Pwr.BRK_DMG, 0, self.role, [AtkType.BRK], 1, 1, Role.SELF, TickDown.PERM)) # disable all ult buffs
            bl.append(Buff("SamSPDBoost", Pwr.SPD, 0, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("SamWBEBoost", Pwr.WB_EFF, 0, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            if self.eidolon == 6:
                bl.append(Buff("SamE6Pen", Pwr.FIRPEN, 0, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        elif self.eidolon >= 2 and self.e2Counter == 0 and self.enhancedState:
            if result.brokenEnemy:
                self.e2Counter = 2
                al.append(Advance("FireflyE2Adv", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.e2Counter = max(0, self.e2Counter - 1)
        return super().takeTurn()
    
    def canUseUlt(self) -> bool:
        return False if self.enhancedState else super().canUseUlt()
    
    def special(self):
        return "Firefly"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.atkStat = specialRes.attr1
        bonusBE = max(0, (self.atkStat - 1800) // 10) * 0.008
        self.beStat = specialRes.attr2
        bl.append(Buff("FireflyBEConversion", Pwr.BE_PERCENT, bonusBE, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.tech:
            self.tech = False
            tl.append(Turn(self.name, self.role, 0, Targeting.AOE, [AtkType.TECH], [self.element], [2.0, 0], [20 * 2/3, 0], 0, self.scaling, 0, "FireflyTech"))
        self.enemyStatus = specialRes.attr3
        return bl, dbl, al, dl, tl
    
    def bestEnemy(self, enemyID) -> int:
        if all(x == self.enemyStatus[0] for x in self.enemyStatus): # all enemies have the same toughness, choose default target
            return self.defaultTarget if enemyID == -1 else enemyID
        return self.enemyStatus.index(min(self.enemyStatus)) if enemyID == -1 else enemyID
    
    