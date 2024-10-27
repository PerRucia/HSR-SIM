import logging

from Character import Character
from RelicStats import RelicStats
from Result import *
from Buff import *
from Lightcones.BeforeDawn import BeforeDawn
from Relics.Duke import DukeJY
from Planars.Banan import Banan
from Turn import Turn

logger = logging.getLogger(__name__)

class Jingyuan(Character):
    # Standard Character Settings
    name = "JingYuan"
    path = Path.ERUDITION
    element = Element.LIGHTNING 
    scaling = Scaling.ATK
    baseHP = 1164.2
    baseATK = 698.54
    baseDEF = 485.10
    baseSPD = 99
    maxEnergy = 130
    currEnergy = 65
    ultCost = 130
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSummon = True

    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, rotation = None, targetPrio = Priority.DEFAULT) -> None:
        super().__init__(pos, role, defaultTarget, eidolon, targetPrio)
        self.lightcone = lc if lc else BeforeDawn(self.role, level=1)
        self.relic1 = r1 if r1 else DukeJY(self.role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else Banan(self.role, summon=True)
        # Fast JY build RelicStats(6, 2, 0, 2, 4, 0, 4, 4, 4, 4, 7, 11, Pwr.CR_PERCENT, Pwr.SPD_PERCENT, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        # Base SPD JY build RelicStats(0, 2, 0, 2, 4, 0, 4, 4, 4, 4, 13, 11, Pwr.CR_PERCENT, Pwr.ATK_PERCENT, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        self.relicStats = subs if subs else RelicStats(0, 2, 0, 2, 4, 0, 4, 4, 4, 4, 13, 11, Pwr.CR_PERCENT, Pwr.ATK_PERCENT, Pwr.DMG_PERCENT, Pwr.ATK_PERCENT)
        self.eidolon = eidolon
        self.rotation = rotation if rotation else ["E"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("JYTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL]))
        bl.append(Buff("JYTraceCR", Pwr.CR_PERCENT, 0.12, self.role, [AtkType.ALL]))
        bl.append(Buff("JYTraceDEF", Pwr.DEF_PERCENT, 0.125, self.role, [AtkType.ALL]))
        bl.append(Buff("JYStartEnergy", Pwr.ERR_F, 15, self.role, [AtkType.SPECIAL]))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Mul = 1.1 if self.eidolon >= 3 else 1.0
        tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Mul, 0], [10, 0], 20, self.scaling, 1, "JingYuanBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e5Mul = 1.1 if self.eidolon >= 5 else 1.0
        bl.append(Buff("JYSkillCR", Pwr.CR_PERCENT, 0.10, self.role, [AtkType.ALL], 2, tdType=TickDown.END))
        tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.AOE, [AtkType.SKL], [self.element], [e5Mul, 0], [10, 0], 30, self.scaling, -1, "JingYuanSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        e3Mul = 2.16 if self.eidolon >= 3 else 2.0
        tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.AOE, [AtkType.ULT], [self.element], [e3Mul, 0], [20, 0], 5, self.scaling, 0, "JingYuanUlt"))
        self.currEnergy = self.currEnergy - self.ultCost
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if "LightningLordGoGo" in result.turnName:
            llStacks = int(result.turnName[-2:])
            self.useFua(-1)
            cdBoost = 0.25 if llStacks >= 6 else 0
            bl.append(Buff("JingyuanFuaCD", Pwr.CD_PERCENT, cdBoost, self.role, [AtkType.FUA]))
            if self.eidolon >= 2:
                bl.append(Buff("JingyuanE2DMG", Pwr.DMG_PERCENT, 0.20, self.role, [AtkType.BSC, AtkType.SKL, AtkType.ULT], 2, tdType=TickDown.END))
            e4ERR = 2 if self.eidolon >= 4 else 0
            e5Mul = 0.726 if self.eidolon >= 5 else 0.66
            if self.eidolon == 6:
                bl.append(Buff("JingyuanE6Vuln", Pwr.VULN, 0.324, self.role, [AtkType.FUA]))
            for i in range(llStacks):
                name = "JingYuanFuaFirst" if i == 0 else "JingYuanFuaExtras"
                e1Div = 2 if self.eidolon >= 1 else 4
                tl.append(Turn(self.name, self.role, i % len(self.enemyStatus), Targeting.BLAST, [AtkType.FUA], [self.element], [e5Mul, e5Mul / e1Div], [5, 0], e4ERR, self.scaling, 0, name))
        return bl, dbl, al, dl, tl
    
    