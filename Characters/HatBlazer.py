import logging

from Buff import *
from Character import Character
from Delay import *
from Lightcones.MemoriesOfThePast import MotpHMC
from Planars.Kalpagni import KalpagniFirefly
from RelicStats import RelicStats
from Relics.Watchmaker import WatchmakerHMC
from Result import *
from Result import Special
from Turn import Turn

logger = logging.getLogger(__name__)

class HatBlazer(Character):
    # Standard Character Settings
    name = "HarmonyMC"
    path = Path.HARMONY
    element = Element.IMAGINARY 
    scaling = Scaling.ATK
    baseHP = 1086.6
    baseATK = 446.29
    baseDEF = 679.14
    baseSPD = 105
    maxEnergy = 140
    currEnergy = 70
    ultCost = 140
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.SKL: 0, AtkType.BRK: 0, AtkType.SBK: 0} # Adjust accordingly
    
    # Unique Character Properties
    backupDancerTurns = 0
    numEnemies = 0
    firstSkill = True
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 6, rotation = None, targetPrio = Priority.DEFAULT) -> None:
        super().__init__(pos, role, defaultTarget, eidolon, targetPrio)
        self.beStat = None
        self.lightcone = lc if lc else MotpHMC(role)
        self.relic1 = r1 if r1 else WatchmakerHMC(role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else KalpagniFirefly(role)
        self.relicStats = subs if subs else RelicStats(12, 4, 0, 4, 4, 0, 4, 12, 4, 4, 0, 0, Pwr.HP_PERCENT, Pwr.SPD, Pwr.DEF_PERCENT, Pwr.BE_PERCENT)
        self.rotation = rotation if rotation else ["E", "E", "A"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("HMCTech", Pwr.BE_PERCENT, 0.30, Role.ALL, turns=2, tdType=TickDown.END))
        bl.append(Buff("HMCTraceBE", Pwr.BE_PERCENT, 0.373, self.role))
        bl.append(Buff("HMCTraceDMG", Pwr.DMG_PERCENT, 0.144, self.role))
        bl.append(Buff("HMCTraceERS", Pwr.ERS_PERCENT, 0.10, self.role))
        if self.eidolon >= 2:
            bl.append(Buff("HMCE2ERR", Pwr.ERR_PERCENT, 0.25, self.role, turns=3, tdType=TickDown.END))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e5Bonus = 1.1 if self.eidolon >= 5 else 1.0
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Bonus, 0], [10, 0], 20, self.scaling, 1, "HMCBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e3Bonus = 0.55 if self.eidolon >= 3 else 0.5
        sp = 0 if (self.firstSkill and self.eidolon >= 1) else -1
        if self.firstSkill:
            self.firstSkill = False
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.SKL], [self.element], [e3Bonus, 0], [20, 0], 6, self.scaling, sp, "HMCSkill"))
        numHits = 6 if self.eidolon == 6 else 4
        for i in range(numHits):
            tl.append(Turn(self.name, self.role, i % self.numEnemies, Targeting.SINGLE, [AtkType.SKL], [self.element], [e3Bonus, 0], [5, 0], 6, self.scaling, 0, "HMCSkillExtras"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.backupDancerTurns = 3
        e5BE = 0.33 if self.eidolon >= 5 else 0.3
        bl.append(Buff("HMCBackupDancer", Pwr.BE_PERCENT, e5BE, Role.ALL, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, -1, Targeting.NA, [AtkType.ALL], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "HMCUlt"))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if result.brokenEnemy:
            e3ERR = 11 if self.eidolon >= 3 else 10
            bl.append(Buff("HMCWeaknessBreakERR", Pwr.ERR_T, e3ERR * len(result.brokenEnemy), self.role))
            for enemy in result.brokenEnemy:
                dl.append(Delay("HMCBreakDelay", 0.30, enemy.enemyID, True, False))
        if self.backupDancerTurns > 0 and result.enemiesHit and turn.moveName != "HMCUlt" and turn.moveName != "HMCSuperBreak" and result.preHitStatus[result.enemiesHit[0].enemyID]:
            tl.append(Turn(self.name, self.role, result.enemiesHit[0].enemyID, Targeting.STSB, [AtkType.SBK, AtkType.BRK, AtkType.HMCSBK], [self.element], [1.0, 0], [turn.brkSplit[0], 0], 0, self.scaling, 0, "HMCSuperBreak"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if result.brokenEnemy:
            e3ERR = 11 if self.eidolon >= 3 else 10
            bl.append(Buff("HMCWeaknessBreakERR", Pwr.ERR_T, e3ERR * len(result.brokenEnemy), self.role))
            for enemy in result.brokenEnemy:
                dl.append(Delay("HMCBreakDelay", 0.30, enemy.enemyID, True, False))
        if self.backupDancerTurns > 0 and result.enemiesHit:
            if turn.targeting == Targeting.AOE:
                for enemy in result.enemiesHit:
                    if result.preHitStatus[enemy.enemyID]:
                        tl.append(Turn(result.charName, result.charRole, result.enemiesHit[0].enemyID, Targeting.STSB, [AtkType.SBK, AtkType.BRK, AtkType.HMCSBK], [turn.element[0]], [1.0, 0], [turn.brkSplit[0], 0], 0, turn.scaling, 0, "HMCAllySuperBreak"))
            elif turn.targeting == Targeting.SINGLE:
                if result.preHitStatus[result.enemiesHit[0].enemyID]:
                    tl.append(Turn(result.charName, result.charRole, result.enemiesHit[0].enemyID, Targeting.STSB, [AtkType.SBK, AtkType.BRK, AtkType.HMCSBK], [turn.element[0]], [1.0, 0], [turn.brkSplit[0], 0], 0, turn.scaling, 0, "HMCAllySuperBreak"))
            elif turn.targeting == Targeting.BLAST:
                if result.preHitStatus[result.enemiesHit[0].enemyID]: # main target
                    tl.append(Turn(result.charName, result.charRole, result.enemiesHit[0].enemyID, Targeting.STSB, [AtkType.SBK, AtkType.BRK, AtkType.HMCSBK], [turn.element[0]], [1.0, 0], [turn.brkSplit[0], 0], 0, turn.scaling, 0, "HMCAllySuperBreak"))
                for adjEnemy in result.enemiesHit[1:]:
                    if result.preHitStatus[adjEnemy.enemyID]:
                        tl.append(Turn(result.charName, result.charRole, adjEnemy.enemyID, Targeting.STSB, [AtkType.SBK, AtkType.BRK, AtkType.HMCSBK], [turn.element[0]], [1.0, 0], [turn.brkSplit[1], 0], 0, turn.scaling, 0, "HMCAllySuperBreak"))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.backupDancerTurns = max(0, self.backupDancerTurns - 1)
        return super().takeTurn()
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.beStat = specialRes.attr1
        self.numEnemies = len(self.enemyStatus)
        dmgMul = (5 - self.numEnemies) * 0.1 + 0.2
        bl.append(Buff("HMCSuperBrkDMG", Pwr.SBRK_DMG, dmgMul, Role.ALL, [AtkType.HMCSBK]))
        if self.eidolon >= 4:
            bl.append(Buff("HMCE4BuffBE", Pwr.BE_PERCENT, self.beStat * 0.15, Role.TEAM))
        return bl, dbl, al, dl, tl
    