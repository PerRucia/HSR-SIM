import logging

from Character import Character
from Planars import KalpagniRappa
from RelicStats import RelicStats
from Lightcones.Ninjutsu import Ninjitsu
from Relics.IronCavalry import CavalryRappa
from Planars.Talia import Talia
from Relics.NoSet import NoSet
from Result import *
from Turn import Turn
from Buff import *
from Delay import *

logger = logging.getLogger(__name__)

class Rappa(Character):
    # Standard Character Settings
    name = "Rappa"
    path = Path.ERUDITION
    element = Element.IMAGINARY
    scaling = Scaling.ATK
    baseHP = 1086.60
    baseATK = 717.948
    baseDEF = 460.85
    baseSPD = 96
    maxEnergy = 140
    currEnergy = 140 / 2
    ultCost = 140
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.EBSC: 0, AtkType.SKL: 0, AtkType.BRK: 0, AtkType.SBK: 0, AtkType.TECH: 0} # Adjust accordingly
    
    # Unique Character Properties
    atkStat = 0
    sealformBasics = 0
    tech = True
    canUlt = False
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, rotation = None, targetPrio = Priority.BROKEN) -> None:
        super().__init__(pos, role, defaultTarget, eidolon, targetPrio)
        self.lightcone = lc if lc else Ninjitsu(role)
        self.relic1 = r1 if r1 else CavalryRappa(role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else KalpagniRappa(role, True)
        self.relicStats = subs if subs else RelicStats(10, 4, 0, 4, 4, 5, 4, 9, 4, 4, 0, 0, Pwr.ATK_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.BE_PERCENT)
        self.rotation = rotation if rotation else ["E"] # overridden by class-specific takeTurn method
        self.charges = 5 if self.eidolon == 6 else 0

    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("RappaTraceATK", Pwr.ATK_PERCENT, 0.28, self.role))
        bl.append(Buff("RappaTraceSPD", Pwr.SPD, 9, self.role))
        bl.append(Buff("RappaTraceBE", Pwr.BE_PERCENT, 0.133, self.role))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        if self.sealformBasics:
            self.sealformBasics = max(0, self.sealformBasics - 1)
            e2TRD = 15 if self.eidolon >= 2 else 10
            e5Mul = 1.08 if self.eidolon >= 5 else 1.00
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLASTSB, [AtkType.SBK, AtkType.BRK], [self.element], [0.6, 0.6], [e2TRD, 5], 0, self.scaling, 0, "RappaEBASB"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLAST, [AtkType.EBSC, AtkType.BSC], [self.element], [e5Mul, e5Mul / 2], [e2TRD, 5], 5, self.scaling, 0, "RappaEBAP1", True, 0.5))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLASTSB, [AtkType.SBK, AtkType.BRK], [self.element], [0.6, 0.6], [e2TRD, 5], 0, self.scaling, 0, "RappaEBASB"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.BLAST, [AtkType.EBSC, AtkType.BSC], [self.element], [e5Mul, e5Mul / 2], [e2TRD, 5], 5, self.scaling, 0, "RappaEBAP1", True, 0.5))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.AOESB, [AtkType.SBK, AtkType.BRK], [self.element], [0.6, 0.6], [5, 0], 0, self.scaling, 0, "RappaEBASB"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.AOE, [AtkType.EBSC, AtkType.BSC], [self.element], [e5Mul, 0], [5, 0], 10, self.scaling, 0, "RappaEBAP2", True, 0.5))
        else:
            e5Mul = 1.1 if self.eidolon >= 5 else 1.0
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Mul, 0], [10, 0], 20, self.scaling, 1, "RappaBasic"))
        if not self.sealformBasics:
            bl.append(Buff("SealformWBE", Pwr.WB_EFF, 0.0, self.role))
            bl.append(Buff("SealformBE", Pwr.BE_PERCENT, 0.0, self.role))
            if self.eidolon >= 1:
                bl.append(Buff("RappaE1ERR", Pwr.ERR_T, 20, self.role))
                bl.append(Buff("SealformE1Shred", Pwr.SHRED, 0.0, self.role))
            if self.eidolon >= 4:
                bl.append(Buff("SealformE4SPD", Pwr.SPD_PERCENT, 0.0, Role.ALL))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e3Mul = 1.32 if self.eidolon >= 3 else 1.2
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.AOE, [AtkType.SKL], [self.element], [e3Mul, 0], [10, 0], 30, self.scaling, -1, "RappaSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.sealformBasics = 3
        bl.append(Buff("SealformWBE", Pwr.WB_EFF, 0.5, self.role))
        baseBE = 0.34 if self.eidolon >= 5 else 0.3
        bl.append(Buff("SealformBE", Pwr.BE_PERCENT, baseBE + 0.2 if self.eidolon >= 2 else 0, self.role))
        tl.append(Turn(self.name, self.role, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RappaUlt"))
        if self.eidolon >= 1:
            bl.append(Buff("SealformE1Shred", Pwr.SHRED, 0.15, self.role))
        if self.eidolon >= 4:
            bl.append(Buff("SealformE4SPD", Pwr.SPD_PERCENT, 0.12, Role.ALL))
        bl, dbl, al, dl, tl = self.extendLists(bl, dbl, al, dl, tl, *self.useBsc(enemyID))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        vulnBuff = min(8, (self.atkStat - 2400) // 100) * 0.01 + 0.02
        for enemy in result.brokenEnemy:
            self.charges = min(15 if self.eidolon == 6 else 10, self.charges + 1)
            tl.extend(self.checkEnemyType(enemy))
            dbl.append(Debuff("RappaBrkVuln", self.role, Pwr.VULN, vulnBuff, enemy.enemyID, [AtkType.BRK], 2, 1))
        if self.sealformBasics == 0 and turn.moveName == "RappaEBAP2": # trigger talent
            e3Base = 0.66 if self.eidolon >= 3 else 0.6
            e3Bonus = (0.55 if self.eidolon >= 3 else 0.5) * self.charges
            trd = self.charges
            self.charges = 5 if self.eidolon == 6 else 0
            tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.AOESB, [AtkType.SBK], [self.element], [e3Base + e3Bonus, 0], [trd + 2, 0], 0, self.scaling, 0, "RappaTalentSBK"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.AOEBREAK, [AtkType.BRK], [self.element], [e3Base + e3Bonus, 0], [0, 0], 0, self.scaling, 0, "RappaTalentBRK"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.AOE, [AtkType.SPECIAL], [self.element], [0, 0], [trd + 2, 0], 0, self.scaling, 0, "RappaTalentTRD"))
        return bl, dbl, al, dl, tl

    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        vulnBuff = min(8, (self.atkStat - 2400) // 100) * 0.01 + 0.02
        for enemy in result.brokenEnemy:
            self.charges = min(15 if self.eidolon == 6 else 10, self.charges + 1)
            tl.extend(self.checkEnemyType(enemy))
            dbl.append(Debuff("RappaBrkVuln", self.role, Pwr.VULN, vulnBuff, enemy.enemyID, [AtkType.BRK], 2, 1))
        return bl, dbl, al, dl, tl
    
    def checkEnemyType(self, enemy: Enemy):
        if enemy.enemyType == EnemyType.ADD:
            return []
        return [Turn(self.name, self.role, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 10, self.scaling, 0, "RappaBreakERR")]

    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "Rappa":
            self.atkStat = specialRes.attr1
        if self.tech:
            self.tech = False
            tl.append(Turn(self.name, self.role, 0, Targeting.AOE, [AtkType.SPECIAL], [self.element], [0, 0], [20 if specialRes.attr2 else 30, 0], 20, self.scaling, 0, "RappaTech", omniBreak=True, omniBreakMod=1.0))
            for i in range(len(self.enemyStatus)):
                tl.append(Turn(self.name, self.role, i, Targeting.BLASTBREAK, [AtkType.TECH, AtkType.BRK], [self.element], [2.0, 1.8], [0, 0], 0, self.scaling, 0, "RappaTechDMG"))
        return bl, dbl, al, dl, tl

    def takeTurn(self) -> str:
        return "A" if self.sealformBasics else "E"

    def canUseUlt(self) -> bool:
        return super().canUseUlt() if not self.sealformBasics else False
    