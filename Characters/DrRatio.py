import logging

from Buff import *
from Character import Character
from Lightcones.Cruising import Cruising
from Planars.Duran import Duran
from RelicStats import RelicStats
from Relics.Pioneer import PioneerRatio
from Result import *
from Result import Special
from Turn import Turn

logger = logging.getLogger(__name__)

class DrRatio(Character):
    # Standard Character Settings
    name = "DrRatio"
    path = Path.HUNT
    element = Element.IMAGINARY 
    scaling = Scaling.ATK
    baseHP = 1047.8
    baseATK = 776.16
    baseDEF = 460.85
    baseSPD = 103
    maxEnergy = 140
    currEnergy = 70
    ultCost = 140
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    targetDebuffs = 0
    wisemanFolly = 0
    canUlt = False
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Cruising(role)
        self.relic1 = r1 if r1 else PioneerRatio(role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else Duran(role)
        self.relicStats = subs if subs else RelicStats(4, 2, 0, 2, 4, 0, 4, 4, 4, 4, 8, 12, Pwr.CR_PERCENT, Pwr.SPD, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        self.rotation = rotation if rotation else ["E"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        dbl.append(Debuff("RatioTech", self.role, Pwr.SPD_PERCENT, 0.15, Role.ALL, [AtkType.ALL], 2, 1, False, [0, 0], False))
        bl.append(Buff("RatioTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RatioTraceCR", Pwr.CR_PERCENT, 0.12, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RatioTraceDEF", Pwr.DEF_PERCENT, 0.125, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon == 6:
            bl.append(Buff("RatioE6DMG", Pwr.DMG_PERCENT, 0.5, self.role, [AtkType.FUA], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Bonus = 0.1 if self.eidolon >= 3 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [1.0 + e3Bonus, 0], [10, 0], 20, self.scaling, 1, "RatioBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e4Bonus = 15 if self.eidolon >= 4 else 0
        e5Bonus = 0.15 if self.eidolon >= 5 else 0
        e5Bonus2 = 0.27 if self.eidolon >= 5 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.SKL], [self.element], [1.5 + e5Bonus, 0], [20, 0], 30, self.scaling, -1, "RatioSkill"))
        dbl.append(Debuff("RatioSkillDebuff", self.role, Pwr.ERS_PERCENT, 0.10, self.getTargetID(enemyID), [AtkType.ALL], 2, 1, False, [0, 0], False))
        self.fuas = self.fuas + 1
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [2.7 + e5Bonus2, 0], [10, 0], 5 + e4Bonus, self.scaling, 0, "RatioSkillFua"))
        if self.eidolon >= 2:
            for _ in range(min(4, self.targetDebuffs)):
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [0.2, 0], [0, 0], 0, self.scaling, 0, "RatioE2Bonus"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.wisemanFolly = 3 if self.eidolon == 6 else 2
        e3Bonus = 0.192 if self.eidolon >= 3 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.ULT], [self.element], [2.4 + e3Bonus, 0], [30, 0], 5, self.scaling, 0, "RatioUlt"))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        e4Bonus = 15 if self.eidolon >= 4 else 0
        e5Bonus2 = 0.27 if self.eidolon >= 5 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [2.7 + e5Bonus2, 0], [10, 0], 5 + e4Bonus, self.scaling, 0, "RatioFua"))
        if self.eidolon >= 2:
            for _ in range(int(min(4, self.targetDebuffs))):
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [0.2, 0], [0, 0], 0, self.scaling, 0, "RatioE2Bonus"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if self.wisemanFolly > 0:
            if turn.moveName not in bonusDMG and turn.targeting != Targeting.NA:
                self.wisemanFolly = max(0, self.wisemanFolly - 1)
                bl, dbl, al, dl, tl = self.useFua(result.enemiesHit[0])
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Ratio"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "Ratio":
            self.targetDebuffs = specialRes.attr1
            self.canUlt = specialRes.attr2
            critStacks = min(6.0, self.targetDebuffs)
            crBonus = 0.1 if self.eidolon >= 1 else 0
            cdBonus = 0.2 if self.eidolon >= 1 else 0
            bl.append(Buff("RatioNumDeBuffsCR", Pwr.CR_PERCENT, 0.025 * critStacks + crBonus, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("RatioNumDeBuffsCD", Pwr.CR_PERCENT, 0.05 * critStacks + cdBonus, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            if self.targetDebuffs >= 3:
                dmgStacks = min(5.0, self.targetDebuffs)
                bl.append(Buff("RatioNumDeBuffsDMG", Pwr.DMG_PERCENT, 0.10 * dmgStacks, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl, tl
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False
    
    
    
    