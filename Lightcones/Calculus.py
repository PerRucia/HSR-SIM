from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Result import Result
from Turn import Turn


class Calculus(Lightcone):
    name = "Eternal Calculus"
    path = Path.ERUDITION
    baseHP = 1058.4
    baseATK = 529.20
    baseDEF = 396.90

    def __init__(self, wearerRole, level: int = 5):
        super().__init__(wearerRole, level)
    
    def equip(self):
        bl, dbl, al, dl = super().equip()
        bl.append(Buff("CalculusATK", Pwr.ATK_PERCENT, self.level * 0.01 + 0.07, self.wearerRole))
        return bl, dbl, al, dl

class CalculusRappa(Calculus):
    def __init__(self, wearerRole, level: int = 5):
        super().__init__(wearerRole, level)

    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().ownTurn(turn, result)
        if result.charRole == self.wearerRole and result.turnName in {"RappaBasic", "RappaEBAP2", "RappaSkill"}:
            bl.append(Buff("CalculusHitATK", Pwr.ATK_PERCENT, (self.level * 0.01 + 0.03) * len(result.enemiesHit), self.wearerRole))
            if len(result.enemiesHit) > 2:
                bl.append(Buff("CalculusSPD", Pwr.SPD_PERCENT, self.level * 0.02 + 0.6, self.wearerRole, turns=2, tdType=TickDown.END))
        return bl, dbl, al, dl
    

    