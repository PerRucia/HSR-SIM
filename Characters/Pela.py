from Character import Character
from Lightcones.Resolution import ResolutionPela
from Relics.Messenger import Messenger
from Relics.Longevous import Longevous
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Result import *
from Turn import Turn
from Misc import *
from Delay import *
import logging

logger = logging.getLogger(__name__)

class Pela(Character):
    # Standard Character Settings
    name = "Pela"
    path = Path.NIHILITY
    element = Element.ICE
    scaling = Scaling.ATK
    baseHP = 987.8
    baseATK = 546.84
    baseDEF = 463.05
    baseSPD = 105
    maxEnergy = 110
    currEnergy = 55
    ultCost = 110
    currAV = 0
    rotation = ["E"] # Adjust accordingly
    dmgDct = {Move.BSC: 0, Move.SKL: 0, Move.ULT: 0, Move.BRK: 0} # Adjust accordingly
    
    # Unique Character Properties
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else ResolutionPela(role, 5)
        self.relic1 = r1 if r1 else Longevous(role, 2)
        self.relic2 = r2 if r2 else Messenger(role, 2, False)
        self.planar =  pl if pl else Keel(role)
        self.relicStats = subs if subs else RelicStats(11, 2, 2, 2, 2, 2, 2, 2, 13, 10, 0, 0, Pwr.HP_PERCENT, Pwr.SPD, Pwr.DEF_PERCENT, Pwr.ERR_PERCENT)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("PelaTraceEHR", Pwr.ERR_PERCENT, 0.1, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("PelaTraceDMG", Pwr.DMG_PERCENT, 0.224, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("PelaTraceATK", Pwr.ATK_PERCENT, 0.18, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("PelaTeamEHR", Pwr.ERR_PERCENT, 0.1, Role.ALL, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("PelaDebuffBonusDMG", Pwr.DMG_PERCENT, 0.2, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.BSC], [self.element], [1.1 + 0.4, 0], [10, 0], 20, self.scaling, 1, "PelaBasic")) # bonus 0.4 from e6
        if self.lightcone.name == "Resolution Shines as Pearls of Sweat":
            tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.ALL], [self.element], [0, 0], [0, 0], 11, self.scaling, 0, "PelaTalentERR"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.SKL], [self.element], [2.31 + 0.4, 0], [20, 0], 41, self.scaling, -1, "PelaSkill")) # bonus 0.4 from e6
        dbl.append(Debuff("PelaIceRes", self.role, Pwr.ICEPEN, 0.12, self.getTargetID(enemyID), [Move.ALL], 1, 1, False, [0, 0], False)) # e4
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.AOE, [Move.ULT], [self.element], [1.08 + 0.4, 0], [10, 0], 16, self.scaling, 0, "PelaUlt")) # bonus 0.4 from e6
        dbl.append(Debuff("PelaUltShred", self.role, Pwr.SHRED, 0.42, Role.ALL, [Move.ALL], 2, 1, False, [0, 0], False))
        return bl, dbl, al, dl, tl
    
    
    