from Character import Character
from RelicStats import RelicStats
from Lightcones.MemoriesOfThePast import MOTP
from Lightcones.Mirror import Mirror
from Relics.Thief import Thief
from Relics.Messenger import Messenger
from Planars.Lushaka import Lushaka
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class RuanMei(Character):
    # Standard Character Settings
    name = "RuanMei"
    path = Path.HARMONY
    element = Element.ICE
    scaling = Scaling.ATK
    baseHP = 1086.6
    baseATK = 659.74
    baseDEF = 485.10
    baseSPD = 104
    maxEnergy = 130
    currEnergy = 65
    ultCost = 130
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.BRK: 0,  AtkType.SBK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    beStat = 0
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, breakTeam = False, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else MOTP(role)
        self.relic1 = r1 if r1 else Thief(role, 2)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else Messenger(role, 2))
        self.planar = pl if pl else Lushaka(role)
        self.relicStats = subs if subs else RelicStats(10, 4, 0, 4, 4, 0, 4, 14, 4, 4, 0, 0, Pwr.HP_PERCENT, Pwr.SPD, Pwr.DEF_PERCENT, Pwr.ERR_PERCENT)
        self.breakTeam = breakTeam
        self.rotation = rotation if rotation else ["A", "A", "E"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        teamSPD = 0.104 if self.eidolon >= 3 else 0.10
        bl.append(Buff("RuanSPD", Pwr.SPD_PERCENT, teamSPD, Role.ALL))
        bl.append(Buff("RuanTech", Pwr.ERR_T, 30,  self.role))
        bl.append(Buff("RuanDMG", Pwr.DMG_PERCENT, 0.68, Role.ALL, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        bl.append(Buff("RuanWBE", Pwr.WB_EFF, 0.50, Role.ALL, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        bl.append(Buff("RuanTraceBE", Pwr.BE_PERCENT, 0.20,  self.role))
        bl.append(Buff("RuanTraceDEF", Pwr.DEF_PERCENT, 0.225,  self.role))
        bl.append(Buff("RuanTraceSPD", Pwr.SPD, 5, self.role))
        bl.append(Buff("RuanTeamBE", Pwr.BE_PERCENT, 0.20, Role.ALL))
        if self.eidolon >= 2:
            bl.append(Buff("RuanE2ATK", Pwr.ATK_PERCENT, 0.4, Role.ALL, [AtkType.ALL], reqBroken=True))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e5Bonus = 1.1 if self.eidolon >= 5 else 1.0
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Bonus, 0], [10, 0], 25, self.scaling, 1, "RuanBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e5Bonus = 0.352 if self.eidolon >= 5 else 0.32
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "RuanSkill"))
        bl.append(Buff("RuanDMG", Pwr.DMG_PERCENT, e5Bonus + 0.36, Role.ALL, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        bl.append(Buff("RuanWBE", Pwr.WB_EFF, 0.50, Role.ALL, [AtkType.ALL], 3, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        ultTurns = 3 if self.eidolon == 6 else 2
        pen = 0.27 if self.eidolon >= 3 else 0.25
        bl.append(Buff("RuanUltPEN", Pwr.PEN, pen, Role.ALL, [AtkType.ALL], ultTurns, 1, self.role, TickDown.START))
        breakMul = 0.54 if self.eidolon >= 3 else 0.50
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOEBREAK, [AtkType.BRK], [self.element], [breakMul, 0], [0, 0], 5, self.scaling, 0, "RuanUltBreak"))
        if self.eidolon >= 1:
            bl.append(Buff("RuanE1Shred", Pwr.SHRED, 0.20, Role.ALL, [AtkType.ALL], ultTurns, 1, self.role, TickDown.START))
        dl.append(Delay("RuanThanatoplum", 0.1 + self.beStat * 0.2, Role.ALL, True, False))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if result.brokenEnemy and self.eidolon >= 4:
            bl.append(Buff("RuanE4BE", Pwr.BE_PERCENT, 1.0, self.role, turns=4, tdType=TickDown.END))
        for enemyID in result.brokenEnemy:
            breakMul = 1.32 if self.eidolon >= 3 else 1.2
            e6 = 2.0 if self.eidolon == 6 else 0
            tl.append(Turn(self.name, self.role, enemyID, Targeting.STBREAK, [AtkType.BRK], [self.element], [breakMul + e6, 0], [0, 0], 0, self.scaling, 0, "RuanAllyBreak"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if result.brokenEnemy and self.eidolon >= 4:
            bl.append(Buff("RuanE4BE", Pwr.BE_PERCENT, 1.0, self.role, turns=3, tdType=TickDown.END))
        for enemyID in result.brokenEnemy:
            breakMul = 1.32 if self.eidolon >= 3 else 1.2
            e6 = 2.0 if self.eidolon == 6 else 0
            tl.append(Turn(self.name, self.role, enemyID, Targeting.STBREAK, [AtkType.BRK], [self.element], [breakMul + e6, 0], [0, 0], 0, self.scaling, 0, "RuanAllyBreak"))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "RuanMei"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.beStat = specialRes.attr1
        self.enemyStatus = specialRes.attr2
        return bl, dbl, al, dl, tl
    
    def bestEnemy(self, enemyID) -> int:
        if all(x == self.enemyStatus[0] for x in self.enemyStatus) or not self.breakTeam: # all enemies have the same toughness, choose default target
            return self.defaultTarget if enemyID == -1 else enemyID
        return self.enemyStatus.index(min(self.enemyStatus)) if enemyID == -1 else enemyID

    
    
    