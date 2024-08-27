from Relic import Relic
from Buff import Buff
from Delay import *
from Misc import *
from Result import Special

class NoSet(Relic):
    name = "No Relic Set Bonuses"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)

