from Character import Character
from Lightcones.PostOpConversation import PostOp
from Lightcones.Scent import ScentLingsha
from Relics.Thief import Thief
from Planars.Keel import Keel
from Planars.Kalpagni import KalpagniLingsha
from RelicStats import RelicStats
from Buff import *
from Result import *
from Result import Special
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Lingsha(Character):
    # Standard Character Settings
    name = "Lingsha"
    path = Path.ABUNDANCE
    element = Element.FIRE
    scaling = Scaling.ATK   
    baseHP = 1358.3
    baseATK = 679.14
    baseDEF = 436.59
    baseSPD = 98
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.FUA: 0, AtkType.SKL: 0, AtkType.ULT: 0, AtkType.BRK: 0, AtkType.SBK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    canUlt = False
    hasSummon = True
    beStat = 0
    count = 2
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 0, breakTeam = False, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else ScentLingsha(role)
        self.relic1 = r1 if r1 else Thief(role, 4)
        self.relic2 = r2 if r2 else None
        self.planar = pl if pl else KalpagniLingsha(role)
        rope = Pwr.BE_PERCENT if self.lightcone.name == "Post-Op Conversation" else Pwr.ERR_PERCENT
        self.relicStats = subs if subs else RelicStats(12, 4, 0, 4, 4, 0, 4, 12, 4, 4, 0, 0, Pwr.OGH_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, rope)
        self.breakTeam = breakTeam
        self.rotation = rotation if rotation else ["E", "A", "A"]
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("LingshaTraceBE", Pwr.BE_PERCENT, 0.373, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LingshaTraceATK", Pwr.ATK_PERCENT, 0.1, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LingshaTraceHP", Pwr.HP_PERCENT, 0.18, self.role, [AtkType.ALL], 1, 1, Role.SELF, TickDown.PERM))
        if self.eidolon >= 1:
            bl.append(Buff("LingshaE1WBE", Pwr.WB_EFF, 0.5, self.role))
            bl.append(Buff("LingshaE1Shred", Pwr.SHRED, 0.20, Role.ALL, reqBroken=True))
        if self.eidolon == 6:
            bl.append(Buff("LingshaE6Pen", Pwr.PEN, 0.20, Role.ALL))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e5Mul = 1.1 if self.eidolon >= 5 else 1.0
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e5Mul, 0], [10, 0], 30, self.scaling, 1, "LingshaBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        e5Mul = 0.88 if self.eidolon >= 5 else 0.8
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.SKL], [self.element], [e5Mul, 0], [10, 0], 30, self.scaling, -1, "LingshaSkill"))
        al.append(Advance("LingshaADV", Role.FUYUAN, 0.2))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        e3Mul = 1.62 if self.eidolon >= 3 else 1.5
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.ULT], [self.element], [e3Mul, 0], [20, 0], 5, self.scaling, 0, "LingshaUlt"))
        al.append(Advance("LingshaADV", Role.FUYUAN, 1.0))
        befog = 0.27 if self.eidolon >= 3 else 0.25
        dbl.append(Debuff("LingshaBefog", self.role, Pwr.VULN, befog, Role.ALL, [AtkType.BRK], 2, 1, False, [0, 0], False))
        if self.eidolon >= 2:
            bl.append(Buff("LingshaE2BE", Pwr.BE_PERCENT, 0.40, Role.ALL, turns=3, tdType=TickDown.END))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(turn, result)
        if self.count == 0 and result.turnName != "FuyuanGoGo" and result.turnName != "LingshaAutoheal":
            self.count = 3
            self.fuas = self.fuas + 1
            e3Bonus = 0.825 if self.eidolon >= 3 else 0.75
            tl.append(Turn(self.name, self.role, self.getTargetID(-1), Targeting.AOE, [AtkType.FUA], [self.element], [e3Bonus, 0], [10, 0], 0, self.scaling, 0, "LingshaAutoheal"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.SINGLE, [AtkType.FUA], [self.element], [e3Bonus, 0], [10, 0], 0, self.scaling, 0, "LingshaAutohealExtra"))
            if self.eidolon == 6:
                for _ in range(4):
                    tl.append(Turn(self.name, self.role, self.bestEnemy(-1), Targeting.SINGLE, [AtkType.FUA], [self.element], [0.5, 0], [5, 0], 0, self.scaling, 0, "LingshaE6Extras"))
        elif result.turnName == "FuyuanGoGo":
            return self.useFua(-1)
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        if turn.moveName == "FuyuanGoGo":
            return self.useFua(-1)
        return super().allyTurn(turn, result)
         
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        e3Bonus = 0.825 if self.eidolon >= 3 else 0.75
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.FUA], [self.element], [e3Bonus, 0], [10, 0], 0, self.scaling, 0, "LingshaFua"))
        tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [e3Bonus, 0], [10, 0], 0, self.scaling, 0, "LingshaFuaExtra"))
        if self.eidolon == 6:
            for _ in range(4):
                tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.FUA], [self.element], [0.5, 0], [5, 0], 0, self.scaling, 0, "LingshaE6Extras"))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.count = self.count - 1
        return super().takeTurn()
    
    def special(self):
        return "Lingsha"
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.canUlt = specialRes.attr1
        self.enemyStatus = specialRes.attr2
        self.beStat = specialRes.attr3
        atkBuff = min(0.5, self.beStat * 0.25)
        bl.append(Buff("LingshaBEtoATK", Pwr.ATK_PERCENT, atkBuff, self.role))
        return bl, dbl, al, dl, tl
        
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False
    
    def bestEnemy(self, enemyID) -> int:
        if all(x == self.enemyStatus[0] for x in self.enemyStatus) or not self.breakTeam: # all enemies have the same toughness, choose default target
            return self.defaultTarget if enemyID == -1 else enemyID
        return self.enemyStatus.index(max(self.enemyStatus)) if enemyID == -1 else enemyID
    
    
    