import logging

from Buff import *
from Character import Character
from Delay import *
from Lightcones.Multi import Multi
from Planars.Kalpagni import KalpagniGallagher
from RelicStats import RelicStats
from Relics.Messenger import Messenger
from Relics.Thief import Thief
from Result import Special
from Turn import Turn

logger = logging.getLogger(__name__)

class Gallagher(Character):
    # Standard Character Settings
    name = "Gallagher"
    path = Path.ABUNDANCE
    element = Element.FIRE
    scaling = Scaling.ATK
    baseHP = 1305.4
    baseATK = 529.20
    baseDEF = 441.00
    baseSPD = 98
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    dmgDct = {AtkType.BSC: 0, AtkType.ULT: 0, AtkType.BRK: 0, AtkType.SBK: 0} # Adjust accordingly
    
    # Unique Character Properties
    hasSpecial = True
    beStat = 0
    canUlt = False
    nectarBlitz = False

    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: Role, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None, eidolon = 6, breakTeam = False, rotation = None) -> None:
        super().__init__(pos, role, defaultTarget, eidolon)
        self.lightcone = lc if lc else Multi(role)
        self.relic1 = r1 if r1 else Thief(role, 2)
        self.relic2 = None if self.relic1.setType == 4 else (r2 if r2 else Messenger(role, 2))
        self.planar = pl if pl else KalpagniGallagher(role)
        self.relicStats = subs if subs else RelicStats(11, 4, 0, 4, 4, 0, 4, 13, 4, 4, 0, 0, Pwr.OGH_PERCENT, Pwr.SPD, Pwr.HP_PERCENT, Pwr.ERR_PERCENT)
        self.breakTeam = breakTeam
        self.rotation = rotation if rotation else ["A"]
        self.enemyStatus = []
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("GallagherTraceERS", Pwr.ERS_PERCENT, 0.28, self.role))
        bl.append(Buff("GallagherTraceBE", Pwr.BE_PERCENT, 0.133, self.role))
        bl.append(Buff("GallagherTraceHP", Pwr.HP_PERCENT, 0.18, self.role))
        if self.eidolon >= 1:
            bl.append(Buff("GallagherE1ERS", Pwr.ERS_PERCENT, 0.5, self.role))
            bl.append(Buff("GallagherE1ERR", Pwr.ERR_T, 20, self.role))
        if self.eidolon == 6:
            bl.append(Buff("GallagherE6BE", Pwr.BE_PERCENT, 0.2, self.role))
            bl.append(Buff("GallagherE6WBE", Pwr.WB_EFF, 0.2, self.role))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        e3Normal = 1.1 if self.eidolon >= 3 else 1.0
        e3Enhanced = 2.75 if self.eidolon >= 3 else 2.5
        e3Debuff = 0.16 if self.eidolon >= 3 else 0.15
        if self.nectarBlitz:
            self.nectarBlitz = False
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Enhanced * 0.25, 0], [30 * 0.25, 0], 0, self.scaling, 0, "GallagherEBSCExtras"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Enhanced * 0.15, 0], [30 * 0.15, 0], 0, self.scaling, 0, "GallagherEBSCExtras"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Enhanced * 0.60, 0], [30 * 0.6, 0], 20, self.scaling, 1, "GallagherEBSC"))
            dbl.append(Debuff("GalNectarBlitz", self.role, Pwr.GENERIC, e3Debuff, self.getTargetID(enemyID), [AtkType.ALL], 2))
        else:
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Normal * 0.5, 0], [5, 0], 0, self.scaling, 0, "GallagherBasicP1"))
            tl.append(Turn(self.name, self.role, self.bestEnemy(enemyID), Targeting.SINGLE, [AtkType.BSC], [self.element], [e3Normal * 0.5, 0], [5, 0], 20, self.scaling, 1, "GallagherBasicP2"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        self.nectarBlitz = True
        besottedTurns = 3 if self.eidolon >= 4 else 2
        e5Vuln = 0.132 if self.eidolon >= 5 else 0.12
        e5ult = 0.165 if self.eidolon >= 5 else 0.15
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), Targeting.AOE, [AtkType.ULT], [self.element], [e5ult, 0], [20, 0], 5, self.scaling, 0, "GallagherUlt"))
        dbl.append(Debuff("GalBesotted", self.role, Pwr.VULN, e5Vuln, Role.ALL, [AtkType.BRK], besottedTurns, 1, False, [0, 0], False))
        al.append(Advance("GallagherUltAdv", self.role, 1.0))
        return bl, dbl, al, dl, tl
    
    def special(self):
        return "Gallagher"
    
    def canUseUlt(self) -> bool:
        return super().canUseUlt() if self.canUlt else False
    
    def handleSpecialStart(self, specialRes: Special):
        bl, dbl, al, dl, tl = super().handleSpecialStart(specialRes)
        self.beStat = specialRes.attr1
        oghBuff = min(0.75, self.beStat * 0.5)
        bl.append(Buff("GallagherBEtoOGH", Pwr.OGH_PERCENT, oghBuff, self.role, [AtkType.ALL]))
        self.canUlt = specialRes.attr2
        self.enemyStatus = specialRes.attr3
        return bl, dbl, al, dl, tl
    
    def bestEnemy(self, enemyID) -> int:
        if all(x == self.enemyStatus[0] for x in self.enemyStatus) or not self.breakTeam: # all enemies have the same toughness, choose default target
            return self.defaultTarget if enemyID == -1 else enemyID
        return self.enemyStatus.index(max(self.enemyStatus)) if enemyID == -1 else enemyID
        
    
    
    