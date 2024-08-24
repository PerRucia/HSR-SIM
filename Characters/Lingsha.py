from Character import Character
from Lightcones.PostOpConversation import PostOp
from Relics.Messenger import Messenger
from Relics.Thief import Thief
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
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
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {"BSC": 0, "FUA": 0, "SKL": 0, "ULT": 0, "BREAK": 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSummon = True
    fuyuanRole = Role.FUYUAN
    count = 2
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    relicStats = RelicStats(10, 2, 2, 2, 2, 2, 2, 15, 3, 8, 0, 0, Pwr.OGH_PERCENT, Pwr.SPD, Pwr.ATK_PERCENT, Pwr.BE_PERCENT)
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = PostOp(role, 5)
        self.relic1 = Messenger(role, 2, False)
        self.relic2 = Thief(role, 2)
        self.planar = Keel(role)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("LingshaTraceBE", Pwr.BE_PERCENT, 0.373, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LingshaTraceATK", Pwr.ATK_PERCENT, 0.1, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LingshaTraceHP", Pwr.HP_PERCENT, 0.18, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("LingshaBEtoATK", Pwr.ATK_PERCENT, 0.5, self.role, ["ALL"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["BSC"], [self.element], [1.0, 0], [10, 0], 30, self.scaling, 1, "LingshaBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.AOE, ["SKL"], [self.element], [0.8, 0], [10, 0], 30, self.scaling, -1, "LingshaSkill"))
        al.append(Advance("LingshaADV", self.fuyuanRole, 0.2))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.AOE, ["ULT"], [self.element], [1.5, 0], [20, 0], 5, self.scaling, 0, "LingshaUlt"))
        al.append(Advance("LingshaADV", self.fuyuanRole, 1.0))
        dbl.append(Debuff("LingshaBefog", self.role, Pwr.VULN, 0.25, Role.ALL, ["BREAK"], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl, tl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl, tl = super().ownTurn(result)
        if self.count == 0 and result.turnName != "FuyuanGoGo" and result.turnName != "LingshaAutoheal":
            self.count = 3
            self.fuas = self.fuas + 1
            tl.append(Turn(self.name, self.role, self.getTargetID(-1), AtkTarget.AOE, ["FUA"], [self.element], [0.9, 0], [10, 0], 0, self.scaling, 0, "LingshaAutoheal"))
        elif result.turnName == "FuyuanGoGo":
            return self.useFua(-1)
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        if turn.moveName == "FuyuanGoGo":
            return self.useFua(-1)
        return super().allyTurn(turn, result)
         
    def useFua(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useFua(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.AOE, ["FUA"], [self.element], [0.75, 0], [10, 0], 0, self.scaling, 0, "LingshaFua"))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, ["FUA"], [self.element], [0.75, 0], [10, 0], 0, self.scaling, 0, "LingshaFuaExtra"))
        return bl, dbl, al, dl, tl
    
    def takeTurn(self) -> str:
        self.count = self.count - 1
        return super().takeTurn()
    
    
    