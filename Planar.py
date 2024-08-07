from equipment import Equipment

class Planar(Equipment):
    name = "Planar"
    
    def __init__(self, wearerRole: str):
        super().__init__(wearerRole)
        
    def __str__(self) -> str:
        return f"{self.name}"
    
