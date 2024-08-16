from Character import Character
from Lightcones.MemoriesOfThePast import MOTP
from Relics.Musketeer import Musketeer
from Planars.Vonwacq import Vonwacq
from RelicStats import RelicStats
from Buff import Buff
from Result import Result
from Turn import Turn

class Tingyun(Character):
    # Standard Character Settings
    name = "Tingyun"
    path = "HAR"
    element = "LNG"
    scaling = "ATK"
    baseHP = 846.70
    baseATK = 529.20
    baseDEF = 396.90
    baseSPD = 112
    maxEnergy = 130
    ultCost = 130
    currEnergy = 130
    currAV = 0
    rotation = ["E", "A", "A"]
    dmgDct = {"BSC": 0, "BREAK": 0}
    
    # Unique Character Properties
    beneTarget = "DPS"
    
    # Relic Settings
    relicStats = RelicStats(9, 2, 2, 5, 2, 4, 6, 6, 3, 6, 3, 0, "ATK%", "SPD", "ATK%", "ERR%")
    
    def __init__(self, pos: int, role: str) -> None:
        super().__init__(pos, role)
        self.lightcone = MOTP(role, 5)
        self.relic1 = Musketeer(role, 4)
        self.relic2 = None
        self.planar = Vonwacq(role)
        
    def equip(self):
        buffList, debuffList, advList, delayList = super().equip()
        buffList.extend([Buff("TingyunBasicDMG", "DMG%", 0.4, self.role, ["BSC"], 1, 1, "SELF", "PERM"),
                         Buff("TingyunTraceATK", "ATK%", 0.28, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("TingyunTraceDEF", "DEF%", 0.225, self.role, ["ALL"], 1, 1, "SELF", "PERM"),
                         Buff("TingyunTraceDMG", "DMG%", 0.08, self.role, ["ALL"], 1, 1, "SELF", "PERM")
                         ])
        return buffList, debuffList, advList, delayList
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "ST", ["BSC"], [self.element], [1.1, 0], [10, 0], 25, self.scaling, 1, "TingyunBasic"))
        tl.append(Turn(self.name, self.beneTarget, -1, "ST", ["BSC"], [self.element], [0.66, 0], [0, 0], 0, "ATK", 0, "TYAllyBonus"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "NA", ["SKL"], [self.element], [0, 0], [0, 0], 35, self.scaling, -1, "TingyunSkill"))
        bl.append(Buff("Benediction", "ATK%", 0.55, self.beneTarget, ["ALL"], 3, 1, self.beneTarget, "END"))
        bl.append(Buff("TingyunSkillSPD", "SPD%", 0.2, self.role, ["ALL"], 1, 1, "SELF", "END"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        self.currEnergy = self.currEnergy - self.ultCost
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        tl.append(Turn(self.name, self.role, enemyID, "NA", ["ULT"], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "TingyunUlt"))
        bl.append(Buff("TingyunUltEnergy", "ERR_F", 60, self.beneTarget, ["ALL"], 1, 1, self.beneTarget, "PERM"))
        bl.append(Buff("TingyunUltDMG", "DMG%", 0.56, self.beneTarget, ["ALL"], 2, 1, self.beneTarget, "END"))
        return bl, dbl, al, dl, tl
    
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl, tl = super().allyTurn(turn, result)
        beneFilter = ["TYAllyBonus", "TYBeneBonus", "YunliCullBounce"]
        if (turn.charRole == self.beneTarget) and (turn.moveName not in beneFilter) and (turn.moveType != "NA"):
            tl.append(Turn(self.name, self.beneTarget, -1, "ST", ["BSC"], [self.element], [0.64, 0], [0, 0], 0, "ATK", 0, "TYBeneBonus"))
        return bl, dbl, al, dl, tl
    
    