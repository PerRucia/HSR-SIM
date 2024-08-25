from Character import Character
from Lightcones.Resolution import ResolutionJQ
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
    dmgDct = {Move.BSC: 0, Move.SKL: 0, Move.ULT: 0, Move.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    ehrStat = 0
    maxAshenStacks = 0
    fieldCount = 0
    offTurnCount = 0
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else ResolutionJQ(role, 5)
        self.relic1 = r1 if r1 else Longevous(role, 2)
        self.relic2 = r2 if r2 else Messenger(role, 2, False)
        self.planar = pl if pl else Vonwacq(role)
        self.relicStats = subs if subs else RelicStats(8, 2, 2, 2, 2, 2, 2, 2, 18, 8, 0, 0, Pwr.EHR_PERCENT, Pwr.SPD, Pwr.DMG_PERCENT, Pwr.ERR_PERCENT)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("JQTraceEHR", Pwr.ERR_PERCENT, 0.28, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JQTraceDMG", Pwr.DMG_PERCENT, 0.144, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JQTraceSPD", Pwr.SPD, 5.0, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JQStartERR", Pwr.ERR_T, 15, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.BSC], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "JiaoqiuBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.BLAST, [Move.SKL], [self.element], [1.5, 0.9], [20, 10], 30, self.scaling, -1, "JiaoqiuSkill"))
        dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, 0.10, self.getTargetID(enemyID), [Move.ALL], 2, 5, True, [1.8, 1.8], True))
        dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, 0.10, self.getTargetID(enemyID), [Move.ALL], 2, 5, True, [1.8, 0], False))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.fieldCount = 3
        self.offTurnCount = 6
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.AOE, [Move.ULT], [self.element], [1.0, 0], [20, 0], 5, self.scaling, 0, "JiaoqiuUlt"))
        dbl.append(Debuff("JQUltVuln", self.role, Pwr.VULN, 0.15, Role.ALL, [Move.ULT], 1000, 1, False, [0, 0], False))
        for _ in range(self.maxAshenStacks):
            dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, 0.10, Role.ALL, [Move.ALL], 2, 5, True, [1.8, 0], False))
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)
        self.offTurnCount = max(0, self.offTurnCount - 1)
        if self.offTurnCount > 0:
            dbl.append(Debuff("AshenRoasted", self.role, Pwr.VULN, 0.10, enemyID, [Move.ALL], 2, 5, True, [1.8, 1.8], False))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Jiaoqiu"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.ehrStat = specialRes.attr1
        self.maxAshenStacks = specialRes.attr2
        bonusATKStacks = min(4, (self.ehrStat * 100 - 80) // 15)
        bl.append(Buff(self.name, Pwr.ATK_PERCENT, bonusATKStacks * 0.6, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if specialRes.attr3:
            self.fieldCount = max(0, self.fieldCount - 1) # tick down field stacks at start of turn
        if self.fieldCount == 0: # dispell debuff once field is removed
            dbl.append(Debuff("JQUltVuln", self.role, Pwr.VULN, 0.0, Role.ALL, [Move.ULT], 1000, 1, False, [0, 0], False))
        return bl, dbl, al, dl, tl
    
    
    
    