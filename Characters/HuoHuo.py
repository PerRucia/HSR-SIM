from Character import Character
from Lightcones.PostOpConversation import PostOp
from Relics.Longevous import Longevous
from Relics.Messenger import Messenger
from Planars.Keel import Keel
from RelicStats import RelicStats
from Buff import *
from Misc import *
from Result import *
from Turn import Turn

class HuoHuo(Character):
    # Standard Character Settings
    name = "HuoHuo"
    path = Path.ABUNDANCE
    element = Element.WIND
    scaling = Scaling.HP
    baseHP = 1358.3
    baseATK = 601.52
    baseDEF = 509.36
    baseSPD = 98
    maxEnergy = 140
    currEnergy = 70
    ultCost = 140
    currAV = 0
    rotation = ["E", "A", "A"] # Adjust accordingly
    dmgDct = {Move.BSC: 0, Move.BRK: 0} # Adjust accordingly
    hasSpecial = True
    
    # Unique Character Properties
    ally1Energy = 0
    ally2Energy = 0
    ally3Energy = 0
    ally1Role = 0
    ally2Role = 0
    ally3Role = 0
    
    # Relic Settings
    # First 12 entries are sub rolls: SPD, HP, ATK, DEF, HP%, ATK%, DEF%, BE%, EHR%, RES%, CR%, CD%
    # Last 4 entries are main stats: Body, Boots, Sphere, Rope
    
    def __init__(self, pos: int, role: str, defaultTarget: int = -1, lc = None, r1 = None, r2 = None, pl = None, subs = None) -> None:
        super().__init__(pos, role, defaultTarget)
        self.lightcone = lc if lc else PostOp(self.role, 5)
        self.relic1 = r1 if r1 else Messenger(self.role, 2, True)
        self.relic2 = r2 if r2 else Longevous(self.role, 2)
        self.planar = pl if pl else Keel(self.role)
        self.relicStats = subs if subs else RelicStats(8, 2, 3, 4, 7, 6, 4, 0, 0, 9, 5, 0, Pwr.OGH_PERCENT, Pwr.SPD, Pwr.HP_PERCENT, Pwr.ERR_PERCENT)
        
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("HHTraceHP", Pwr.HP_PERCENT, 0.28, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("HHTraceERS", Pwr.ERS_PERCENT, 0.18, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("HHTraceSPD", Pwr.SPD, 5, self.role, [Move.ALL], 1, 1, Role.SELF, TickDown.PERM))
        return bl, dbl, al, dl
    
    def useBsc(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useBsc(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.SINGLE, [Move.BSC], [self.element], [0.5, 0], [10, 0], 20, self.scaling, 1, "HuoHuoBasic"))
        return bl, dbl, al, dl, tl
    
    def useSkl(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useSkl(enemyID)
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.SKL], [self.element], [0, 0], [0,0], 36, self.scaling, -1, "HuoHuoSkill"))
        return bl, dbl, al, dl, tl
    
    def useUlt(self, enemyID=-1):
        bl, dbl, al, dl, tl = super().useUlt(enemyID)
        self.currEnergy = self.currEnergy - self.ultCost
        bl.append(Buff("HuoHuoUltATK", Pwr.ATK_PERCENT, 0.4, Role.ALL, [Move.ALL], 2, 1, Role.SELF, TickDown.END))
        bl.append(Buff("HuoHuoERR", Pwr.ERR_F, self.ally1Energy, self.ally1Role, [Move.ALL], 1, 1, self.ally1Role, TickDown.PERM))
        bl.append(Buff("HuoHuoERR", Pwr.ERR_F, self.ally2Energy, self.ally2Role, [Move.ALL], 1, 1, self.ally2Role, TickDown.PERM))
        bl.append(Buff("HuoHuoERR", Pwr.ERR_F, self.ally3Energy, self.ally3Role, [Move.ALL], 1, 1, self.ally3Role, TickDown.PERM))
        tl.append(Turn(self.name, self.role, self.getTargetID(enemyID), AtkTarget.NA, [Move.ULT], [self.element], [0, 0], [0, 0], 5, self.scaling, 0, "HuoHuoULT"))
        return bl, dbl, al, dl, tl
    
    def special(self):
        self.hasSpecial = False
        return "HuoHuoUlt"
    
    def handleSpecialStart(self, specialRes: Special):
        self.ally1Energy = specialRes.attr1[0]
        self.ally1Role = specialRes.attr1[1]
        self.ally2Energy = specialRes.attr2[0]
        self.ally2Role = specialRes.attr2[1]
        self.ally3Energy = specialRes.attr3[0]
        self.ally3Role = specialRes.attr3[1]
        return super().handleSpecialStart(specialRes)
    
    