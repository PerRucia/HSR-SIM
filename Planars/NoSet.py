from Buff import Buff
from Planar import Planar
from Result import Result
from Turn import Turn
from Misc import *

class NoSet(Planar):
    name = "No Planar Set Bonuses"
    
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        