from Character import Character
from Lightcones.Swordplay import Swordplay
from Lightcones.Blissful import BlissfulMoze
from Relics.Duke import DukeMoze
from Planars.Duran import Duran
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Result, Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Moze(Character):
    # Standard Character Settings
    name = "Moze"
    path = Path.HUNT
    element = Element.LIGHTNING
    scaling = "ATK"
    baseHP = 811.4
    baseATK = 546.84
    baseDEF = 352.80
    baseSPD = 111
    maxEnergy = 120
    currEnergy = 60 + 20 # additional energy from E1
    ultCost = 120
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BONUS":0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    charge = 0
    canBeAdv = True
    fuaRegainSP = True
    cntr = 0
    canUlt = False
    hasSpecial = True
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 17, 7, "CR%", "ATK%", "DMG%", "ATK%")
    
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Swordplay(role)
        self.relic1 = DukeMoze(role, 4)
        self.relic2 = None
        self.planar = Duran(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        al.append(Advance("MozeBattleStart", self.role, 0.30))
        bl.append(Buff("MozeTraceCD", "CD%", 0.373, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("MozeTraceATK", "ATK%", 0.18, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        bl.append(Buff("MozeTraceHP", "HP%", 0.10, self.role, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["BSC"], [self.element], [1.1, 0], [10, 0], 20, self.scaling, 1, "MozeBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        self.charge = 9 # reset charge count
        self.canBeAdv = False # enter departed state
        self.currAV = 1000
        dbl.append(Debuff("MozePreyCD", self.role, "CD%", 0.40, self.getTargetID(enemyID), ["ALL"], 1000, 1, False, [0, 0], False)) # 40% CD from E2
        dbl.append(Debuff("MozePreyVULN", self.role, "VULN", 0.25, self.getTargetID(enemyID), ["FUA"], 1000, 1, False, [0, 0], False)) 
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["SKL"], [self.element], [1.65, 0], [20, 0], 30, self.scaling, -1, "MozeSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        spRegen = 1 if self.fuaRegainSP else 0
        if spRegen == 1:
            self.fuaRegainSP = False
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["ULT", "FUA", "DUKEULT"], [self.element], [2.916, 0], [30, 0], 5, self.scaling, 0, "MozeULT"))
        self.fuas = self.fuas + 1
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["FUA", "DUKEFUA"], [self.element], [1.76 + 0.25, 0], [10, 0], 10, self.scaling, spRegen, "MozeUltFUA"))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        spRegen = 1 if self.fuaRegainSP else 0
        if spRegen == 1:
            self.fuaRegainSP = False
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), "ST", ["FUA", "DUKEFUA"], [self.element], [1.76 + 0.25, 0], [10, 0], 10, self.scaling, spRegen, "MozeFUA"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if turn.moveType != "NA" and turn.moveName not in bonusDMG:
            self.charge = self.charge - 1
            if self.charge < 9 and self.charge % 3 == 0 and not self.canBeAdv: #0, 3, 6, use Fua
                bl, dbl, al, dl, tl = self.useFua(result.enemiesHit[0])
            if self.charge >= 0:
                tl.append(Turn(self.name, self.role, result.enemiesHit[0], "ST", ["BONUS"], [self.element], [0.33, 0], [0, 0], 2, self.scaling, 0, "MozeBonusDMG"))
            if self.charge == 0 and not self.canBeAdv: # charge reaches 0 while in departed state
                self.canBeAdv = True # exit departed state
                self.currAV = 10000 / self.currSPD # rest AV to his current speed
                al.append(Advance("MozeDepartedADV", self.role, 0.20))
                dbl.append(Debuff("MozePreyVULN", self.role, "VULN", 0.00, self.getTargetID(result.enemiesHit[0]), ["FUA"], 1000, 1, False, [0, 0], False)) 
                dbl.append(Debuff("MozePrey", self.role, "CD%", 0.00, self.getTargetID(result.enemiesHit[0]), ["ALL"], 1000, 1, False, [0, 0], False)) # remove 40% CD when not in departed state
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if result.turnName == "MozeULT":
            bl.append(Buff("MozeUltBuff", "DMG%", 0.30, self.role, ["ALL"], 2, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def reduceAV(self, reduceValue: float):
        if self.canBeAdv:
            self.currAV = max(0, self.currAV - reduceValue)
    
    def takeTurn(self) -> str:
        self.fuaRegainSP = True
        return super().takeTurn()
    
    def special(self):
        return "MozeCheckRobin"
    
    def handleSpecialStart(self, specialRes: Special):
        self.canUlt = specialRes.attr1
        return super().handleSpecialEnd(specialRes)
    
    def canUseUlt(self) -> bool:
        if self.canUlt and self.currEnergy >= self.ultCost:
            return True
        else:
            return False
    
    