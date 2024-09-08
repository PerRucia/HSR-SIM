from Misc import *
from Planar import Planar


class NoSet(Planar):
    name = "No Planar Set Bonuses"
    
    def __init__(self, wearerRole: Role):
        super().__init__(wearerRole)
        