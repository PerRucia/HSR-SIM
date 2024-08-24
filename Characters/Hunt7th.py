from Character import Character
from Lightcones.Swordplay import Swordplay
from Relics.Musketeer import Musketeer
from Planars.Rutilant import Rutilant
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Result, Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Hunt7th(Character):
    # Standard Character Settings
    name = "HuntM7"
    path = Path.HUNT
    element = Element.IMAGINARY
    scaling = Scaling.ATK
    baseHP = 1058.4
    baseATK = 564.48
    baseDEF = 441.00
    baseSPD = 102
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    rotation = ["A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "EBSC": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    firstTurn = True
    masterElement = element
    ultEnhanced = False
    charges = 3
    fuaTrigger = True
    advanced = False
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(4, 0, 2, 2, 2, 2, 3, 3, 3, 3, 17, 7, "CR%", "SPD", "DMG%", "ATK%")
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, masterRole: str = Role.DPS) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = Swordplay(role, 5)
        self.relic1 = Musketeer(role, 4)
        self.relic2 = None
        self.planar = Rutilant(role)
        self.masterRole = masterRole
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        al.append(Advance("H7StartAdv", self.role, 0.25))
        bl.append(Buff("H7enhancedBasicCD", "CD%", 0.5, self.role, ["UltEBSC"], 1, 1, Role.SELF, TickDown.END)) # e6 buff
        bl.append(Buff("H7enhancedBasicDMG", "DMG%", 0.88, self.role, ["EBSC"], 1, 1, Role.SELF, TickDown.PERM)) # e6 buff
        bl.append(Buff("H7TraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("H7TraceCD", "CD%", 0.24, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("H7TraceDEF", "DEF%", 0.125, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        if self.charges >= 7:
            self.charges = self.charges - 7
            bl.append(Buff("H7MasterBuffCD", "CD%", 0.60, self.masterRole, ["ALL"], 2, 1, self.masterRole, TickDown.END))
            bl.append(Buff("H7MasterBuffBE", "BE%", 0.36, self.masterRole, ["ALL"], 2, 1, self.masterRole, TickDown.END))
            if self.ultEnhanced:
                self.ultEnhanced = False
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["EBSC", "BSC", "UltEBSC"], [self.element, self.masterElement], [1.1, 0], [5, 0], 35, self.scaling, 0, "H7UltEnhancedBSC"))
                for _ in range(4):
                    tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["EBSC", "BSC", "UltEBSC"], [self.element, self.masterElement], [1.1, 0], [5, 0], 0, self.scaling, 0, "H7UltEnhancedBSCExtras"))
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["EBSC", "BSC", "UltEBSC"], [self.element, self.masterElement], [2.1472, 0], [9.76, 0], 0, self.scaling, 0, "H7UltEnhancedBSCExtras"))
            else:
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["EBSC", "BSC"], [self.element, self.masterElement], [1.1, 0], [5, 0], 35, self.scaling, 0, "H7EnhancedBSC"))
                for _ in range(2):
                    tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["EBSC", "BSC"], [self.element, self.masterElement], [1.1, 0], [5, 0], 0, self.scaling, 0, "H7EnhancedBSCExtras"))
                tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["EBSC", "BSC"], [self.element, self.masterElement], [1.2936, 0], [5.88, 0], 0, self.scaling, 0, "H7EnhancedBSCExtras"))
        else:
            self.charges = min(10, self.charges + 1)
            logger.warning(f"ALERT: H7 gained 1 charge from MarchBasic | Total: {self.charges}")
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["BSC"], [self.element, self.masterElement], [1.1, 0], [10, 0], 25, self.scaling, 1, "H7Basic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        extraErr = 30 if self.firstTurn else 0
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        bl.append(Buff("H7MasterSPD", "SPD%", 0.108, self.masterRole, ["ALL"], 1, 1, Role.SELF, TickDown.PERM)) # e1 buff
        bl.append(Buff("H7SelfSPD", "SPD%", 0.10, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, ["ALL"], [self.element, self.masterElement], [0, 0], [0, 0], 35 + extraErr, self.scaling, -1, "H7Skill")) # e4 energy buff 30 + 5
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.ultEnhanced = True
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["ULT"], [self.element, self.masterElement], [2.592, 0], [30, 0], 5, self.scaling, 0, "H7Ult"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if self.charges >= 7 and not self.advanced:
            self.advanced = True
            al.append(Advance("H7EnhancedADV", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if (turn.charRole == self.masterRole) and (turn.moveName not in bonusDMG) and (turn.moveType != AtkTarget.NA) and (not self.firstTurn):
            self.charges = min(10, self.charges + 1)
            logger.warning(f"ALERT: H7 gained 1 charge from {turn.moveName} | Total: {self.charges}")
            if self.fuaTrigger and (not "FUA" in turn.atkType):
                self.charges = min(10, self.charges + 1)
                logger.warning(f"ALERT: H7 gained 1 charge from MarchFUA | Total: {self.charges}")
                self.fuaTrigger = False
                self.fuas = self.fuas + 1
                tl.append(Turn(self.name, self.role, result.enemiesHit[0], AtkTarget.SINGLE, ["FUA"], [self.element, self.masterElement], [0.6, 0], [1, 0], 5, self.scaling, 0, "MarchFUA"))
        if self.charges >= 7 and not self.advanced:
            self.advanced = True
            al.append(Advance("H7EnhancedADV", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        res = super().takeTurn()
        self.fuaTrigger = True
        self.advanced = False
        if self.firstTurn:
            self.firstTurn = False
            return "E"
        return res
    
    def special(self):
        self.hasSpecial = False
        return "H7Special"
    
    def handleSpecialStart(self, specialRes: Special):
        self.masterElement = specialRes.attr1
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        bl.append(Buff("MarchBonusERR", "ERR_T", 30, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl, tl
    
    
    