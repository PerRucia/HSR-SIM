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
    scaling = "ATK"
    baseHP = 931.4
    baseATK = 620.93
    baseDEF = 412.33
    baseSPD = 110
    maxEnergy = 130
    currEnergy = 65
    ultCost = 130
    currAV = 0
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSummon = True
    hasSpecial = True
    foundFire = False
    numbyRole = "Numby"
    windfallCount = 0
    firstNumby = True
    canUlt = False
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    # CruisingBuild: RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 8, 16, "CR%", "SPD", "DMG%", "ATK%")
    # SwordplayBuild: RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 13, 11, "CR%", "SPD", "DMG%", "ATK%")
    # BronyaBuild: RelicStats(3, 0, 2, 2, 2, 2, 3, 3, 3, 3, 13, 11, "CR%", "SPD", "DMG%", "ATK%")
    relicStats = RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 13, 11, "CR%", "SPD", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, eidolon: int = 0) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Swordplay(role)
        self.relic1 = DukeTopaz(role, 4)
        self.relic2 = None
        self.planar = Duran(role)
        self.eidolon = eidolon
        if self.lightcone.name == "Swordplay":
            self.relicStats = RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 13, 11, "CR%", "SPD", "DMG%", "ATK%")
        else:
            self.relicStats = RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 8, 16, "CR%", "SPD", "DMG%", "ATK%")
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("TopazTraceDMG", "DMG%", 0.224, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("TopazTraceCR", "CR%", 0.12, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("TopazTraceHP", "HP%", 0.10, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("WindfallCD", "CD%", 0.25, self.role, ["TOPAZULT"], 1, 1, "SELF", "PERM"))
        dbl.append(Debuff("ProofOfDebt", self.role, "VULN", 0.5, self.defaultTarget, ["FUA"], 1000, 1, False, [0, 0], False))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC", "FUA"], [self.element], [1.0, 0], [10, 0], 20, self.scaling, 1, "TopazBasic"))
        if self.eidolon >= 1:
            dbl.append(Debuff("DebtorCD", self.role, "CD%", 0.25, self.getTargetID(enemyID), ["FUA"], 1000, 2, False, [0, 0], False))
        al.append(Advance("AdvanceNumby", self.numbyRole, 0.5))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        al.append(Advance("AdvanceNumby", self.numbyRole, 0.5))
        if self.eidolon >= 1:
            dbl.append(Debuff("DebtorCD", self.role, "CD%", 0.25, self.getTargetID(enemyID), ["FUA"], 1000, 2, False, [0, 0], False))
        if self.windfallCount > 0:
            self.windfallCount = self.windfallCount - 1
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["SKL", "FUA", "TOPAZULT"], [self.element], [3.0, 0], [20, 0], 40, self.scaling, -1, "TopazEnhancedSkill"))
        else:
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["SKL", "FUA", "TOPAZFUA"], [self.element], [1.5, 0], [20, 0], 30, self.scaling, -1, "TopazSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.windfallCount = 2
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "NA", ["ALL"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "TopazUlt"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if (turn.moveName not in bonusDMG) and (self.windfallCount > 0) and (self.defaultTarget in result.enemiesHit):
            al.append(Advance("AdvanceWindFallNumby", self.numbyRole, 0.5))
        elif ("FUA" in turn.atkType) and (turn.moveName not in bonusDMG) and (self.defaultTarget in result.enemiesHit):
            if self.eidolon >= 1:
                dbl.append(Debuff("DebtorCD", self.role, "CD%", 0.25, self.defaultTarget, ["FUA"], 1000, 2, False, [0, 0], False))
            al.append(Advance("AdvanceNumby", self.numbyRole, 0.5))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if result.turnName == "NumbyGoGo":
            errGain = 60 if self.firstNumby else 0
            self.firstNumby = False
            self.fuas = self.fuas + 1
            if self.eidolon >= 1:
                dbl.append(Debuff("DebtorCD", self.role, "CD%", 0.25, self.defaultTarget, ["FUA"], 1000, 2, False, [0, 0], False))
            if self.windfallCount > 0:
                self.windfallCount = self.windfallCount - 1
                tl.append(Turn(self.name, self.role, self.defaultTarget, "ST", ["FUA", "TOPAZULT"], [self.element], [3.0, 0], [20, 0], errGain + 10, self.scaling, 0, "TopazEnhancedFUA"))
            else:
                tl.append(Turn(self.name, self.role, self.defaultTarget, "ST", ["FUA", "TOPAZFUA"], [self.element], [1.5, 0], [20, 0], errGain, self.scaling, 0, "TopazFUA"))
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
                bl.append(Buff("TopazFireDMG", "DMG%", 0.15, self.defaultTarget, ["ALL"], 1, 1, "SELF", "PERM"))
        else:
            self.canUlt = specialRes.attr1
        return bl, dbl, al, dl, tl
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False


    
    
    
    