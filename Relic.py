from equipment import Equipment

class Relic(Equipment):
    name = "Relic"
    
    def __init__(self, wearerRole: str, setType: int):
        super().__init__(wearerRole)
        self.setType = setType
        
    def __str__(self) -> str:
        return f"{self.name} ({self.setType}-pc)"