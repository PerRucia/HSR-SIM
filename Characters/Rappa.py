import logging

from scipy.stats import false_discovery_control

from Character import Character
from RelicStats import RelicStats
from Lightcones.Ninjutsu import Ninjitsu
from Lightcones.Calculus import CalculusRappa, Calculus
from Lightcones.Passkey import Passkey
from Relics.IronCavalry import CavalryRappa
from Planars.Talia import Talia
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
    baseATK = 640.33
    baseDEF = 460.85
    baseSPD = 102
    maxEnergy = 160
    currEnergy = 160 / 2
    ultCost = 160
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.EBSC: 0, AtkType.SKL: 0, AtkType.BRK: 0, AtkType.SBK: 0, AtkType.TECH: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    atkStat = 0
    enemyStatus = []
    sealformBasics = 0
    tech = True
    canUlt = False
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, rotation = None, targetPrio = Priority.BROKEN) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Ninjitsu(role, 3)
        self.relic1 = r1 if r1 else CavalryRappa(role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else Talia(role)
        self.relicStats = subs if subs else RelicStats(7, 4, 0, 4, 4, 5, 4, 12, 4, 4, 0, 0, Pwr.ATK_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.BE_PERCENT)
        self.eidolon = eidolon
        self.rotation = rotation if rotation else ["E"] # overridden by class-specific takeTurn method
        self.targetPrio = targetPrio

    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("RappaTraceATK", Pwr.ATK_PERCENT, 0.28, self.role))
        bl.append(Buff("RappaTraceSPD", Pwr.SPD, 9, self.role))
        bl.append(Buff("RappaTraceBE", Pwr.BE_PERCENT, 0.133, self.role))
        if self.eidolon >= 1:
            bl.append(Buff("RappaE1Shred", Pwr.SHRED, 0.15, self.role, atkType=[AtkType.EBSC]))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        if self.sealformBasics:
            self.sealformBasics = max(0, self.sealformBasics - 1)
            omniBreakMod = 1.0 if self.eidolon >= 2 else 0.5
            e5Mul = 0.85 if self.eidolon >= 5 else 0.80
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLASTSB, [AtkType.SBK, AtkType.BRK], [self.element], [0.6, 0.6], [10, 5], 0, self.scaling, 0, "RappaEBASB"))
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.EBSC, AtkType.BSC], [self.element], [e5Mul, e5Mul / 2], [10, 5], 5, self.scaling, 0, "RappaEBAP1", True, omniBreakMod))
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLASTSB, [AtkType.SBK, AtkType.BRK], [self.element], [0.6, 0.6], [10, 5], 0, self.scaling, 0, "RappaEBASB"))
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.BLAST, [AtkType.EBSC, AtkType.BSC], [self.element], [e5Mul, e5Mul / 2], [10, 5], 5, self.scaling, 0, "RappaEBAP1", True, omniBreakMod))
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOESB, [AtkType.SBK, AtkType.BRK], [self.element], [0.6, 0.6], [5, 0], 0, self.scaling, 0, "RappaEBASB"))
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.EBSC, AtkType.BSC], [self.element], [e5Mul, 0], [5, 0], 10, self.scaling, 0, "RappaEBAP2", True, omniBreakMod))
        else:
            e5Mul = 1.1 if self.eidolon >= 5 else 1.0
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Mul, 0], [10, 0], 20, self.scaling, 1, "RappaBasic"))
        if not self.sealformBasics:
            bl.append(Buff("SealformWBE", Pwr.WB_EFF, 0.0, self.role))
            bl.append(Buff("SealformBE", Pwr.BE_PERCENT, 0.0, self.role))
            if self.eidolon >= 1:
                bl.append(Buff("RappaE1ERR", Pwr.ERR_T, 20, self.role))
            if self.eidolon >= 4:
                bl.append(Buff("SealformE4SPD", Pwr.SPD_PERCENT, 0.0, Role.ALL))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e3Mul = 1.32 if self.eidolon >= 3 else 1.2
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.SKL], [self.element], [e3Mul, 0], [10, 0], 30, self.scaling, -1, "RappaSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.sealformBasics = 3
        bl.append(Buff("SealformWBE", Pwr.WB_EFF, 0.5, self.role))
        baseBE = 0.34 if self.eidolon >= 5 else 0.3
        bl.append(Buff("SealformBE", Pwr.BE_PERCENT, baseBE + 0.2 if self.eidolon >= 2 else 0, self.role))
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RappaUlt"))
        if self.eidolon >= 4:
            bl.append(Buff("SealformE4SPD", Pwr.SPD_PERCENT, 0.12, Role.ALL))
        bl, dbl, al, dl, tl = self.extendLists(bl, dbl, al, dl, tl, *self.useBsc(enemyID))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        tl.extend(self.talentTurns(result))
        vulnBuff = min(12, (self.atkStat - 2000) // 100) * 0.01 + 0.03
        for enemy in result.brokenEnemy:
            dbl.append(Debuff("RappaBrkVuln", self.role, Pwr.VULN, vulnBuff, enemy.enemyID, [AtkType.BRK], 2, 1))
        return bl, dbl, al, dl, tl

    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        tl.extend(self.talentTurns(result))
        vulnBuff = min(12, (self.atkStat - 2000) // 100) * 0.01 + 0.03
        for enemy in result.brokenEnemy:
            dbl.append(Debuff("RappaBrkVuln", self.role, Pwr.VULN, vulnBuff, enemy.enemyID, [AtkType.BRK], 2, 1))
        return bl, dbl, al, dl, tl

    def talentTurns(self, result: Result) -> list[Turn]:
        tl = []
        e3Mul = 1.92 if self.eidolon >= 3 else 1.8
        e6Mul = 1.2 if self.eidolon == 6 else 0
        for enemy in result.brokenEnemy:
            errGain = 2 if enemy.enemyType == EnemyType.ADD else 10
            tl.append(Turn(self.name, self.role, enemy.enemyID, Targeting.SINGLE, [AtkType.SPECIAL], [self.element], [0, 0], [0, 0], errGain, self.scaling, 0, "RappaTalentERR"))
            if self.eidolon < 6:
                for adjID in enemy.adjacent:
                    tl.append(Turn(self.name, self.role, adjID, Targeting.SINGLE, [AtkType.BRK], [self.element], [e3Mul + e6Mul, 0], [0, 0], 0, self.scaling, 0, "RappaTalentBDMG"))
                    if not result.preHitStatus[adjID]:
                        tl.append(Turn(self.name, self.role, adjID, Targeting.SINGLE, [AtkType.SPECIAL], [self.element], [0, 0], [10, 0], 0, self.scaling, 0, "RappaTalentTRD"))
            else:
                for i in range(len(self.enemyStatus)):
                    if i == enemy.enemyID:
                        continue
                    tl.append(Turn(self.name, self.role, i, Targeting.SINGLE, [AtkType.BRK], [self.element], [e3Mul + e6Mul, 0], [0, 0], 0, self.scaling, 0, "RappaTalentBDMG"))
                    if not result.preHitStatus[i]:
                        tl.append(Turn(self.name, self.role, i, Targeting.SINGLE, [AtkType.SPECIAL], [self.element], [0, 0], [10, 0], 0, self.scaling, 0, "RappaTalentTRD"))
        return tl

    def special(self):
        return "Rappa"

    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "Rappa":
            self.atkStat = specialRes.attr1
            self.enemyStatus = specialRes.attr3
            self.canUlt = specialRes.attr2
        if self.tech:
            self.tech = False
            tl.append(Turn(self.name, self.role, 0, Targeting.AOE, [AtkType.SPECIAL], [self.element], [0, 0], [20 if specialRes.attr4 else 30, 0], 20, self.scaling, 0, "RappaTech", omniBreak=True, omniBreakMod=1.0))
            for i in range(len(self.enemyStatus)):
                tl.append(Turn(self.name, self.role, i, Targeting.BLASTBREAK, [AtkType.TECH, AtkType.BRK], [self.element], [2.0, 1.8], [0, 0], 0, self.scaling, 0, "RappaTechDMG"))
        return bl, dbl, al, dl, tl

    def takeTurn(self) -> str:
        return "A" if self.sealformBasics else "E"

    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt and not self.sealformBasics else False

    def bestEnemy(self, enemyID) -> int:
        if self.targetPrio == Priority.DEFAULT:
            return self.getTargetID(enemyID)
        if all(x == self.enemyStatus[0] for x in self.enemyStatus):
            return self.defaultTarget if enemyID == -1 else enemyID
        chooseEnemy = min(self.enemyStatus) if self.targetPrio == Priority.BROKEN else max(self.enemyStatus)
        return self.enemyStatus.index(chooseEnemy) if enemyID == -1 else enemyID
    