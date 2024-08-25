from Character import Character
from Lightcones.Swordplay import Swordplay
from Lightcones.Cruising import Cruising
from Lightcones.Blissful import BlissfulTopaz
from Relics.Duke import DukeTopaz
from Planars.Duran import Duran
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Result, Special
from Turn import Turn
from Misc import *
from Delay import *

class Topaz(Character):
    # Standard Character Settings
    name = "Topaz"
    path = Path.HUNT
    element = Element.FIRE
    scaling = Scaling.ATK
    baseHP = 931.4
    baseATK = 620.93
    baseDEF = 412.33
    baseSPD = 110
    maxEnergy = 130
    currEnergy = 65
    ultCost = 130
    currAV = 0
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {Move.BSC: 0, Move.FUA: 0, Move.SKL: 0, Move.ULT: 0, Move.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSummon = True
    hasSpecial = True
    foundFire = False
    numbyRole = Role.NUMBY
    windfallCount = 0
    firstNumby = True
    canUlt = False
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 13, 11, Pwr.CR_PERCENT, Pwr.SPD, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, eidolon: int = 0, lc = None, r1 = None, r2 = None, pl = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else Swordplay(role)
        self.relic1 = r1 if r1 else DukeTopaz(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else Duran(role)
        self.eidolon = eidolon
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("TopazTraceDMG", Pwr.DMG_PERCENT, 0.224, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("TopazTraceCR", Pwr.CR_PERCENT, 0.12, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("TopazTraceHP", Pwr.HP_PERCENT, 0.10, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("WindfallCD", Pwr.CD_PERCENT, 0.25, self.role, [Move.TOPAZULT], 1, 1, Role.SELF, TickDown.PERM))
        dbl.append(Debuff("ProofOfDebt", self.role, Pwr.VULN, 0.5, self.defaultTarget, [Move.FUA], 1000, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.BSC, Move.FUA], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "TopazBasic"))
        if self.eidolon >= 1:
            dbl.append(Debuff("DebtorCD", self.role, Pwr.CD_PERCENT, 0.25, self.getTargetID(enemyID), [Move.FUA], 1000, 2, False, [0, 0], False))
        al.append(Advance("AdvanceNumby", self.numbyRole, 0.5))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        al.append(Advance("AdvanceNumby", self.numbyRole, 0.5))
        if self.eidolon >= 1:
            dbl.append(Debuff("DebtorCD", self.role, Pwr.CD_PERCENT, 0.25, self.getTargetID(enemyID), [Move.FUA], 1000, 2, False, [0, 0], False))
        if self.windfallCount > 0:
            self.windfallCount = self.windfallCount - 1
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.SKL, Move.FUA, Move.TOPAZULT], [self.element], [3.0, 0], [20, 0], 40, self.scaling, -1, "TopazEnhancedSkill"))
        else:
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.SKL, Move.FUA, Move.TOPAZFUA], [self.element], [1.5, 0], [20, 0], 30, self.scaling, -1, "TopazSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.windfallCount = 2
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.ALL], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "TopazULT"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if (turn.moveName not in bonusDMG) and (self.windfallCount > 0) and (self.defaultTarget in result.enemiesHit):
            al.append(Advance("AdvanceWindFallNumby", self.numbyRole, 0.5))
        elif (Move.FUA in turn.atkType) and (turn.moveName not in bonusDMG) and (self.defaultTarget in result.enemiesHit):
            if self.eidolon >= 1:
                dbl.append(Debuff("DebtorCD", self.role, Pwr.CD_PERCENT, 0.25, self.defaultTarget, [Move.FUA], 1000, 2, False, [0, 0], False))
            al.append(Advance("AdvanceNumby", self.numbyRole, 0.5))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if result.turnName == "NumbyGoGo":
            errGain = 60 if self.firstNumby else 0
            self.firstNumby = False
            self.fuas = self.fuas + 1
            if self.eidolon >= 1:
                dbl.append(Debuff("DebtorCD", self.role, Pwr.CD_PERCENT, 0.25, self.defaultTarget, [Move.FUA], 1000, 2, False, [0, 0], False))
            if self.windfallCount > 0:
                self.windfallCount = self.windfallCount - 1
                tl.append(Turn(self.name, self.role, self.defaultTarget, AtkTarget.SINGLE, [Move.FUA, Move.TOPAZULT], [self.element], [3.0, 0], [20, 0], errGain + 10, self.scaling, 0, "TopazEnhancedFUA"))
            else:
                tl.append(Turn(self.name, self.role, self.defaultTarget, AtkTarget.SINGLE, [Move.FUA, Move.TOPAZFUA], [self.element], [1.5, 0], [20, 0], errGain, self.scaling, 0, "TopazFUA"))
        return bl, dbl, al, dl, tl    
    
    def special(self):
        if not self.foundFire:
            self.foundFire = True
            return "TopazFireCheck"
        else:
            return "TopazUltCheck"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "TopazFireCheck":
            if specialRes.attr1:
                bl.append(Buff("TopazFireDMG", Pwr.DMG_PERCENT, 0.15, self.defaultTarget, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        else:
            self.canUlt = specialRes.attr1
        return bl, dbl, al, dl, tl
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False


    
    
    
    