from Character import Character
from Lightcones.MemoriesOfThePast import MOTP
from Relics.Messenger import Messenger
from Relics.Thief import Thief
from Planars.Lushaka import Lushaka
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Result, Special
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
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {Move.BSC: 0, Move.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    beStat = 0
    hasSpecial = True
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(6, 2, 3, 4, 7, 6, 4, 10, 0, 8, 0, 0, Pwr.DEF_PERCENT, Pwr.SPD, Pwr.HP_PERCENT, Pwr.ERR_PERCENT)
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else MOTP(role, 5)
        self.relic1 = r1 if r1 else Thief(role, 2)
        self.relic2 = r2 if r2 else Messenger(role, 2, False)
        self.planar = pl if pl else Lushaka(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("RuanMeiTechERR", Pwr.ERR_T, 30, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RuanMeiWBE", Pwr.WB_EFF, 0.50, Role.ALL, [Move.ALL], 3, 1, self.role, TickDown.START))
        bl.append(Buff("RuanMeiDMG", Pwr.DMG_PERCENT, 0.68, Role.ALL, [Move.ALL], 3, 1, self.role, TickDown.START))
        bl.append(Buff("RuanMeiSPD", Pwr.SPD_PERCENT, 0.10, Role.ALL, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RuanTraceBE", Pwr.BE_PERCENT, 0.373, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RuanTraceDEF", Pwr.DEF_PERCENT, 0.225, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RuanTraceSPD", Pwr.SPD, 5, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("RuanTeamBE", Pwr.BE_PERCENT, 0.20, Role.ALL, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.BSC], [self.element], [1.0, 0], [10, 0], 25, self.scaling, 1, "RuanMeiBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.SKL], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "RuanMeiSkill"))
        bl.append(Buff("RuanMeiWBE", Pwr.WB_EFF, 0.50, Role.ALL, [Move.ALL], 3, 1, self.role, TickDown.START))
        bl.append(Buff("RuanMeiDMG", Pwr.DMG_PERCENT, 0.68, Role.ALL, [Move.ALL], 3, 1, self.role, TickDown.START))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "RuanMeiUlt"))
        bl.append(Buff("RuanMeiPEN", Pwr.PEN, 0.25, Role.ALL, [Move.ALL], 2, 1, self.role, TickDown.START))
        dl.append(Delay("Thanatoplum", 0.1 + self.beStat * 0.2, Role.ALL, True, False))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        if result.brokenEnemy:
            tl.append(Turn(self.name, self.role, result.enemiesHit[0], AtkTarget.STBREAK, [Move.BRK], [self.element], [1.2, 0], [0, 0], 0, self.scaling, 0, "RuanMeiBreakBonus"))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "CheckRuanMeiBE"
    
    def handleSpecialStart(self, specialRes: Special):
        self.beStat = specialRes.attr1
        return super().handleSpecialEnd(specialRes)
    
    
    