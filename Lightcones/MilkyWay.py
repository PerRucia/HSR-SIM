from Delay import Advance
from Lightcone import Lightcone
from Buff import Buff
from Misc import *
from Result import Result, Special
from Turn import Turn


class MilkyWay(Lightcone):
    name = "Night on the Milky Way"
    path = Path.ERUDITION
    baseHP = 1164.2
    baseATK = 582.12
    baseDEF = 396.90

    def __init__(self, wearerRole, level: int = 1):
        super().__init__(wearerRole, level)
    
    def ownTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().ownTurn(turn, result)
        if result.brokenEnemy:
            bl.append(Buff("MilkyWayDMG", Pwr.DMG_PERCENT, self.level * 0.05 + 0.25, self.wearerRole, tdType=TickDown.END))
        return bl, dbl, al, dl

    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().allyTurn(turn, result)
        if result.brokenEnemy:
            bl.append(Buff("MilkyWayDMG", Pwr.DMG_PERCENT, self.level * 0.05 + 0.25, self.wearerRole, tdType=TickDown.END))
        return bl, dbl, al, dl

class MilkyWayRappa(MilkyWay):
    numEnemies = 0

    def specialStart(self, special: Special):
        bl, dbl, al, dl = super().specialStart(special)
        if special.specialName == "Rappa":
            self.numEnemies = len(special.attr3)
            bl.append(Buff("MilkyWayATK", Pwr.ATK_PERCENT, self.numEnemies * (self.level * 0.015 + 0.075), self.wearerRole))
        return bl, dbl, al, dl



    