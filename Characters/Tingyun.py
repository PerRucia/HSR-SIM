from Character import Character
from Lightcones.MemoriesOfThePast import MOTP
from Relics.Musketeer import Musketeer
from Planars.Vonwacq import Vonwacq
from RelicStats import RelicStats
from Buff import Buff
from Result import Result
from Turn import Turn
from Misc import *

class Tingyun(Character):
    # Standard Character Settings
    name = "Tingyun"
    path = Path.HARMONY
    element = Element.LIGHTNING
    scaling = Scaling.ATK
    baseHP = 846.70
    baseATK = 529.20
    baseDEF = 396.90
    baseSPD = 112
    maxEnergy = 130
    ultCost = 130
    currEnergy = 130
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.SPECIAL: 0, AtkType.BRK: 0}
    
    # Unique Character Properties
    
    # Relic Settings
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 6, beneTarget = None, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else MOTP(role, 5)
        self.relic1 = r1 if r1 else Musketeer(role, 4)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else None)
        self.planar = pl if pl else Vonwacq(role)
        self.relicStats = subs if subs else RelicStats(14, 2, 0, 2, 4, 10, 4, 4, 4, 4, 0, 0, Pwr.ATK_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.ERR_PERCENT)
        self.beneTarget = beneTarget if beneTarget else Role.DPS
        self.rotation = rotation if rotation else ["E", "A", "A"]
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.append(Buff("TingyunBasicDMG", Pwr.DMG_PERCENT, 0.4, self.role, [AtkType.BSC], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("TingyunTraceATK", Pwr.ATK_PERCENT, 0.28, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("TingyunTraceDEF", Pwr.DEF_PERCENT, 0.225, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        buffList.append(Buff("TingyunTraceDMG", Pwr.DMG_PERCENT, 0.08, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Mul = 1.1 if self.eidolon >= 3 else 1.0
        e5Mul = 0.66 if self.eidolon >= 5 else 0.6
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Mul, 0], [10, 0], 25, self.scaling, 1, "TingyunBasic"))
        tl.append(Turn(self.name, self.beneTarget, self.getTargetID(enemyID), Targeting.SPECIAL, [AtkType.SPECIAL], [self.element], [e5Mul, 0], [0, 0], 0, Scaling.ATK, 0, "TYAllyBonus"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.SKL], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "TingyunSkill"))
        bl.append(Buff("Benediction", Pwr.ATK_PERCENT, 0.55, self.beneTarget, [AtkType.ALL], 3, 1, self.beneTarget, TickDown.END))
        bl.append(Buff("TingyunSkillSPD", Pwr.SPD_PERCENT, 0.2, self.role, [AtkType.ALL], 2, 1, Role.SELF, TickDown.END))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        errGain = 60 if self.eidolon == 6 else 50
        e3Dmg = 0.56 if self.eidolon >= 3 else 0.50
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.NA, [AtkType.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "TingyunUlt"))
        bl.append(Buff("TingyunUltEnergy", Pwr.ERR_F, errGain, self.beneTarget, [AtkType.ALL], 1, 1, self.beneTarget, TickDown.PERM))
        bl.append(Buff("TingyunUltDMG", Pwr.DMG_PERCENT, e3Dmg, self.beneTarget, [AtkType.ALL], 2, 1, self.beneTarget, TickDown.END))
        if self.eidolon >= 1:
            bl.append(Buff("TingyunE1UltSPD", Pwr.SPD_PERCENT, 0.2, self.beneTarget, turns=1, tickDown=self.beneTarget, tdType=TickDown.END))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        e4BeneBonus = 0.2 if self.eidolon >= 4 else 0
        e5BeneBonus = 0.44 if self.eidolon >= 5 else 0.4
        if (turn.charRole == self.beneTarget) and (turn.moveName not in bonusDMG) and result.enemiesHit:
            tl.append(Turn(self.name, self.beneTarget, result.enemiesHit[0], Targeting.SPECIAL, [AtkType.SPECIAL], [self.element], [e5BeneBonus + e4BeneBonus  , 0], [0, 0], 0, Scaling.ATK, 0, "TYBeneBonus"))
        return bl, dbl, al, dl, tl
    
    