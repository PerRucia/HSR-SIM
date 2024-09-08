from Buff import *
from Character import Character
from Lightcones.ConcertForTwo import ConcertForTwo
from Planars.Keel import Keel
from RelicStats import RelicStats
from Relics.Knight import Knight
from Relics.Messenger import Messenger
from Result import *
from Result import Special
from Turn import Turn


class Aventurine(Character):
    # Standard Character Settings
    name = "Aventurine"
    path = Path.PRESERVATION
    element = Element.IMAGINARY
    scaling = Scaling.DEF
    baseHP = 1203.0
    baseATK = 446.29
    baseDEF = 654.88
    baseSPD = 106
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    baseDefStat = 0
    bbPerHit = 0
    fuaTrigger = 3
    blindBetStacks = 0

    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, eidolon = 0, lc = None, r1 = None, r2 = None, pl = None, subs = None, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else ConcertForTwo(role) 
        self.relic1 = r1 if r1 else Knight(role, 2)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else Messenger(role, 2, False))
        self.planar = pl if pl else Keel(role)
        body = Pwr.CD_PERCENT if self.lightcone.name == "Inherently Unjust Destiny" else Pwr.DEF_PERCENT
        self.relicStats = subs if subs else RelicStats(6, 2, 2, 0, 4, 4, 6, 4, 4, 4, 12, 0, body, Pwr.SPD, Pwr.DEF_PERCENT, Pwr.DEF_PERCENT) # 6 spd default
        self.rotation = rotation if rotation else ["A"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("AvenTraceDEF", Pwr.DEF_PERCENT, 0.35, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("AvenTraceDMG", Pwr.DMG_PERCENT, 0.144, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("AvenTraceERS", Pwr.ERS_PERCENT, 0.10, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 1:
            bl.append(Buff("AvenE1CD", Pwr.CD_PERCENT, 0.20, Role.ALL, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("AvenTeamERS", Pwr.ERS_PERCENT, 0.55 if self.eidolon >= 5 else 0.5, Role.ALL))
        if self.eidolon == 6:
            bl.append(Buff("AvenE6DMG", Pwr.DMG_PERCENT, 1.5, self.role))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Mul = 1.1 if self.eidolon >= 3 else 1.0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Mul, 0], [10, 0], 20, self.scaling, 1, "AvenBasic"))
        if self.eidolon >= 2:
            dbl.append(Debuff("AvenE2PEN", self.role, Pwr.PEN, 0.12, self.getTargetID(enemyID), [AtkType.ALL], 3))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 30, self.scaling, -1, "AvenSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        e3Mul = 2.916 if self.eidolon >= 3 else 2.7
        e3Debuff = 0.162 if self.eidolon >= 3 else 0.15
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.ULT], [self.element], [e3Mul, 0], [30, 0], 5, self.scaling, 0, "AvenUlt"))
        self.currEnergy = self.currEnergy - self.ultCost
        self.blindBetStacks = min(self.blindBetStacks + 4, 10)
        if self.blindBetStacks >= 7:
            self.extendLists(bl, dbl, al, dl, tl, *self.useFua())
        dbl.append(Debuff("AvenUltCD", self.role, Pwr.CD_PERCENT, e3Debuff, self.getTargetID(enemyID), [AtkType.ALL], 3, 1, False, [0, 0], False))
        return bl, dbl, al, dl, tl
    
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        self.blindBetStacks = self.blindBetStacks - 7
        numHits = 9 if self.eidolon >= 4 else 6
        e5Mul = 0.275 if self.eidolon >= 5 else 0.25
        if self.eidolon >= 4:
            bl.append(Buff("AvenE4DEF", Pwr.DEF_PERCENT, 0.4, self.role, turns=2, tdType=TickDown.END))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [e5Mul, 0], [10/3, 0], 1, self.scaling, 0, "AvenFUA"))
        for _ in range(numHits):
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [e5Mul, 0], [10/3, 0], 1, self.scaling, 0, "AvenFUAExtras"))
        return bl, dbl, al, dl, tl
    
    def useHit(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useHit(enemyID)
        self.blindBetStacks = min(10, self.blindBetStacks + self.bbPerHit)
        if self.blindBetStacks >= 7:
            self.extendLists(bl, dbl, al, dl, tl, *self.useFua())
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if (AtkType.FUA in turn.atkType) and (turn.moveName not in bonusDMG) and (self.fuaTrigger > 0):
            self.fuaTrigger = self.fuaTrigger - 1
            self.blindBetStacks = min(10, self.blindBetStacks + 1)
            if self.blindBetStacks >= 7:
                self.extendLists(bl, dbl, al, dl, tl, *self.useFua())
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.fuaTrigger = 3
        return super().takeTurn()
    
    def special(self):
        self.hasSpecial = False
        return "getAvenDEF"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        if specialRes.specialName == "getAvenDEF":
            self.baseDefStat = specialRes.attr1
            self.bbPerHit = specialRes.attr2
            crBuff = min((self.baseDefStat - 1600) // 100, 24)
            bl.append(Buff("AvenBonusCR", Pwr.CR_PERCENT, 0.02 * crBuff, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl, tl
    
    
    