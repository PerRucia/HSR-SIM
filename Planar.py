from equipment import Equipment
from Misc import *

class Planar(Equipment):
    name = "Planar"
    
    def __init__(self, wearerRole: Role):
        super().__init__(wearerRole)
        
    def __str__(self) -> str:
        return f"{self.name}"
    
