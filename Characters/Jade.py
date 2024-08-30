from Character import Character
from RelicStats import RelicStats
from Lightcones.Breakfast import Breakfast
from Relics.Genius import Genius
from Planars.Duran import Duran
from Buff import *
from Result import *
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Jade(Character):
    # Standard Character Settings
    name = "Jade"
    path = Path.ERUDTION
    element = Element.QUANTUM 
    scaling = Scaling.ATK
    baseHP = 1089.6
    baseATK = 659.74
    baseDEF = 509.36
    baseSPD = 103
    maxEnergy = 140
    currEnergy = 70
    ultCost = 140
    currAV = 0
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.ULT: 0, AtkType.SPECIAL: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    fuaStacks = 0
    ultFuaBoost = 0
    pawnAsset = 15 # 15 stacks from technique
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, debtCollector = Role.DPS, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else Breakfast(role)
        self.relic1 = r1 if r1 else Genius(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Duran(role)
        self.relicStats = subs if subs else RelicStats(0, 2, 0, 2, 4, 0, 4, 4, 4, 4, 10, 14, Pwr.CR_PERCENT, Pwr.ATK_PERCENT, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        self.eidolon = eidolon
        self.debtCollector = debtCollector
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("JadeTraceDMG", Pwr.DMG_PERCENT, 0.224, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JadeTraceATK", Pwr.ATK_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("JadeTraceERS", Pwr.ERS_PERCENT, 0.10, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        al.append(Advance("JadeStart", self.role, 0.5))
        if self.eidolon >= 1:
            bl.append(Buff("JadeE1DMG", Pwr.DMG_PERCENT, 0.32, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 6:
            bl.append(Buff("JadeE6PEN", Pwr.QUAPEN, 0.20, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e5Bonus = 0.09 if self.eidolon >= 5 else 0
        e5Bonus2 = 0.03 if self.eidolon >= 5 else 0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.BSC], [self.element], [0.9 + e5Bonus, 0.3 + e5Bonus2], [10, 5], 20, self.scaling, 1, "JadeBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        if self.role != self.debtCollector:
            bl.append(Buff("DebtCollectorSPD", Pwr.SPD, 30, self.debtCollector, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "JadeSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.ultFuaBoost = 2
        e5Bonus = 0.24 if self.eidolon >= 5 else 0
        e5DMG = 0.08 if self.eidolon >= 5 else 0
        bl.append(Buff("JadeUltFuaBoost", Pwr.DMG_PERCENT, 0.80 + e5DMG, self.role, [AtkType.FUA], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 4:
            bl.append(Buff("JadeE4Shred", Pwr.SHRED, 0.12, self.role, [AtkType.ALL], 3, 1, Role.SELF, TickDown.END))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.ULT], [self.element], [2.4 + e5Bonus, 0], [20, 0],5, self.scaling, 0, "JadeUlt"))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        e3bonus = 0.12 if self.eidolon >= 3 else 0
        e3CD = 0.0024 if self.eidolon >= 3 else 0
        self.fuaStacks = self.fuaStacks - 8
        self.ultFuaBoost = self.ultFuaBoost - 1
        self.pawnAsset = min(50, self.pawnAsset + 5)
        bl.append(Buff("PawnedAssetCD", Pwr.CD_PERCENT, self.pawnAsset * (0.024 + e3CD), self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("PawnedAssetATK", Pwr.ATK_PERCENT, self.pawnAsset * 0.005, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 2 and self.pawnAsset >= 15:
            bl.append(Buff("PawnedAssetE2CR", Pwr.CR_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.ultFuaBoost < 0:
            bl.append(Buff("JadeUltFuaBoost", Pwr.DMG_PERCENT, 0.00, self.role, [AtkType.FUA], 1, 1, Role.SELF, TickDown.PERM))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.FUA], [self.element], [1.2 + e3bonus, 0], [10, 0], 10, self.scaling, 0, "JadeFua"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if result.turnName == "JadeUlt" or result.turnName == "JadeBasic":
            self.fuaStacks = self.fuaStacks + len(result.enemiesHit)
            if self.eidolon == 6:
                e1Bonus = 2 if len(result.enemiesHit) == 1 else (1 if len(result.enemiesHit) == 2 else 0)
                self.fuaStacks = self.fuaStacks + len(result.enemiesHit) + 2 * e1Bonus
        if self.fuaStacks >= 8:
            bl, dbl, al, dl, tl = self.useFua(self.defaultTarget)
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.charRole == self.debtCollector and turn.moveName not in bonusDMG and turn.targeting != Targeting.NA:
            if "Basic" in turn.moveName or "Skill" in turn.moveName:
                self.pawnAsset = min(50, self.pawnAsset + 3)
            e3CD = 0.0024 if self.eidolon >= 3 else 0
            e1Bonus = 2 if len(result.enemiesHit) == 1 else (1 if len(result.enemiesHit) == 2 else 0)
            self.fuaStacks = self.fuaStacks + len(result.enemiesHit) + e1Bonus
            if self.fuaStacks >= 8:
                bl, dbl, al, dl, tl = self.useFua(self.defaultTarget)
            if self.eidolon >= 2 and self.pawnAsset >= 15:
                bl.append(Buff("PawnedAssetE2CR", Pwr.CR_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("PawnedAssetCD", Pwr.CD_PERCENT, self.pawnAsset * (0.024 + e3CD), self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("PawnedAssetATK", Pwr.ATK_PERCENT, self.pawnAsset * 0.005, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
            e3Bonus = 0.02 if self.eidolon >= 3 else 0
            for i in result.enemiesHit:
                tl.append(Turn(self.name, self.role, i, Targeting.SINGLE, [AtkType.SPECIAL], [self.element], [0.25 + e3Bonus, 0], [0, 0], 0, self.scaling, 0, "JadeBonusDMG"))
        return bl, dbl, al, dl, tl
    
    
    