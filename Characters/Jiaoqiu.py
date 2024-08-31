from Character import Character
from Lightcones.Resolution import ResolutionJQ
from Lightcones.Spring import Spring
from Relics.Messenger import Messenger
from Relics.Longevous import Longevous
from Planars.Vonwacq import Vonwacq
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Jiaoqiu(Character):
    # Standard Character Settings
    name = "Jiaoqiu"
    path = Path.NIHILITY
    element = Element.FIRE
    scaling = Scaling.ATK
    baseHP = 1358.3
    baseATK = 601.52
    baseDEF = 509.36
    baseSPD = 98
    maxEnergy = 100
    currEnergy = 50
    ultCost = 100
    currAV = 0
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {AtkType.BSC: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    ehrStat = 0
    maxAshenStacks = 0
    fieldCount = 0
    offTurnCount = 0
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else ResolutionJQ(role)
        self.relic1 = r1 if r1 else Longevous(role, 2)
        self.relic2 = r2 if r2 else Messenger(role, 2, False)
        self.planar = pl if pl else Vonwacq(role)
        self.relicStats = subs if subs else RelicStats(6, 4, 0, 4, 4, 0, 4, 4, 18, 4, 0, 0, Pwr.EHR_PERCENT, Pwr.SPD, Pwr.DMG_PERCENT, Pwr.ERR_PERCENT)
        self.ashenRoastMul = 3.0 if self.eidolon >= 2 else 0
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("JQTraceEHR", Pwr.ERR_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JQTraceDMG", Pwr.DMG_PERCENT, 0.144, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JQTraceSPD", Pwr.SPD, 5.0, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JQStartERR", Pwr.ERR_T, 15, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 1:
            bl.append(Buff("JQE1DMG", Pwr.DMG_PERCENT, 0.4, Role.ALL, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        e3Bonus = 0.1 if self.eidolon >= 3 else 0
        e5Vuln = 0.11 if self.eidolon >= 5 else 0.10
        e6Stacks = 9 if self.eidolon == 6 else 5
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e5Mul = 0.198 if self.eidolon >= 5 else 1.8
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [1.0 + e3Bonus, 0], [10, 0], 20, self.scaling, 1, "JiaoqiuBasic"))
        for _ in range(2 if self.eidolon >= 1 else 1):
            dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, e5Vuln, self.getTargetID(enemyID), [AtkType.ALL], 2, e6Stacks, True, [self.ashenRoastMul + e5Mul, 0], False))
            if self.eidolon == 6:
                dbl.append(Debuff("JQE6AshenPen", self.role, Pwr.PEN, 0.03, enemyID, [AtkType.ALL], 2, e6Stacks))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(self.getTargetID(enemyID))
        e3Bonus1 = 0.15 if self.eidolon >= 3 else 0
        e3bonus2 = 0.09 if self.eidolon >= 3 else 0
        e5Vuln = 0.11 if self.eidolon >= 5 else 0.10
        e5Mul = 0.198 if self.eidolon >= 5 else 1.8
        e6Stacks = 9 if self.eidolon == 6 else 5
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.SKL], [self.element], [1.5 + e3Bonus1, 0.9 + e3bonus2], [20, 10], 30, self.scaling, -1, "JiaoqiuSkill"))
        dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, e5Vuln, self.getTargetID(enemyID), [AtkType.ALL], 2, e6Stacks, True, [self.ashenRoastMul + e5Mul, 0], False))
        if self.eidolon == 6:
                dbl.append(Debuff("JQE6AshenPen", self.role, Pwr.PEN, 0.03, enemyID, [AtkType.ALL], 2, e6Stacks))
        for _ in range(2 if self.eidolon >= 1 else 1):  
            dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, e5Vuln, self.getTargetID(enemyID), [AtkType.ALL], 2, e6Stacks, isDot=True, dotSplit=[self.ashenRoastMul + e5Mul, self.ashenRoastMul + e5Mul], isBlast=True))
            if self.eidolon == 6:
                dbl.append(Debuff("JQE6AshenPen", self.role, Pwr.PEN, 0.03, enemyID, [AtkType.ALL], 2, e6Stacks))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.fieldCount = 3
        self.offTurnCount = 6
        self.currEnergy = self.currEnergy - self.ultCost
        e5Mul = 0.198 if self.eidolon >= 5 else 1.8
        e5Vuln = 0.11 if self.eidolon >= 5 else 0.10
        e5UltVuln = 0.165 if self.eidolon >= 5 else 0.15
        e5DmgMul = 1.08 if self.eidolon >= 5 else 1.0
        e6Stacks = 9 if self.eidolon == 6 else 5
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.ULT], [self.element], [e5DmgMul, 0], [20, 0], 5, self.scaling, 0, "JiaoqiuUlt"))
        dbl.append(Debuff("JQUltVuln", self.role, Pwr.VULN, e5UltVuln, Role.ALL, [AtkType.ULT], 1000, 1, False, [0, 0], False))
        if self.eidolon >= 4:
            dbl.append(Debuff("JQE4Debuff", self.role, Pwr.GENERIC, 0.15, Role.ALL, [AtkType.SPECIAL], 1000))
        for _ in range(2 if self.eidolon >= 1 else 1):
            dbl.append(Debuff("AshenRoasted", Role.ALL, Pwr.VULN, e5Vuln, self.getTargetID(enemyID), [AtkType.ALL], 2, e6Stacks, True, [self.ashenRoastMul + e5Mul, 0], False))
            if self.eidolon == 6:
                dbl.append(Debuff("JQE6AshenPen", self.role, Pwr.PEN, 0.03, enemyID, [AtkType.ALL], 2, e6Stacks))
        for _ in range(self.maxAshenStacks):
            dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, e5Vuln, Role.ALL, [AtkType.ALL], 2, e6Stacks, True, [self.ashenRoastMul + e5Mul, 0], False))
            if self.eidolon == 6:
                dbl.append(Debuff("JQE6AshenPen", self.role, Pwr.PEN, 0.03, enemyID, [AtkType.ALL], 2, e6Stacks))
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)
        self.offTurnCount = max(0, self.offTurnCount - 1)
        e5Mul = 0.198 if self.eidolon >= 5 else 1.8
        e5Vuln = 0.11 if self.eidolon >= 5 else 0.10
        e6Stacks = 9 if self.eidolon == 6 else 5
        if self.offTurnCount > 0:
            dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, e5Vuln, enemyID, [AtkType.ALL], 2, e6Stacks, True, [self.ashenRoastMul + e5Mul, 0], False))
            if self.eidolon == 6:
                dbl.append(Debuff("JQE6AshenPen", self.role, Pwr.PEN, 0.03, enemyID, [AtkType.ALL], 2, e6Stacks))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Jiaoqiu"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.ehrStat = specialRes.attr1
        self.maxAshenStacks = specialRes.attr2
        bonusATKStacks = min(4, (self.ehrStat * 100 - 80) // 15)
        bl.append(Buff(self.name, Pwr.ATK_PERCENT, bonusATKStacks * 0.6, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if specialRes.attr3:
            self.fieldCount = max(0, self.fieldCount - 1) # tick down field stacks at start of turn
        if self.fieldCount == 0: # dispell debuff once field is removed
            dbl.append(Debuff("JQUltVuln", self.role, Pwr.VULN, 0.0, Role.ALL, [AtkType.ULT], 1000, 1, False, [0, 0], False))
        return bl, dbl, al, dl, tl
    
    
    
    