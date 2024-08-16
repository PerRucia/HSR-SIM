from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class Duran(Planar):
    name = "Duran, Dynasty of Running Wolves"
    procs = 0
    appliedCDBuff = False
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def allyTurn(self, turn: Turn, result: Result):
        bl, dbl, al, dl = super().allyTurn(turn, result)
        filterFUA = []
        if "FUA" in turn.atkType and turn.moveName not in filterFUA:
            self.procs = self.procs + 1
            bl.append(Buff("DuranATK", "ATK%", 0.05, self.wearerRole, ["FUA"], 1, 5, "SELF", "PERM"))
            if self.procs == 5 and not self.appliedCDBuff:
                self.appliedCDBuff = True
                bl.append(Buff("DuranCD", "CD%", 0.25, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl
    
    def ownTurn(self, result: Result):
        bl, dbl, al, dl = super().ownTurn(result)
        if "FUA" in result.atkType and result.turnName not in bonusDMG:
            self.procs = self.procs + 1
            bl.append(Buff("DuranATK", "ATK%", 0.05, self.wearerRole, ["FUA"], 1, 5, "SELF", "PERM"))
            if self.procs == 5 and not self.appliedCDBuff:
                self.appliedCDBuff = True
                bl.append(Buff("DuranCD", "CD%", 0.25, self.wearerRole, ["ALL"], 1, 1, "SELF", "PERM"))
        return bl, dbl, al, dl