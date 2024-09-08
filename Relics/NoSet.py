from Relic import Relic


class NoSet(Relic):
    name = "No Relic Set Bonuses"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)

