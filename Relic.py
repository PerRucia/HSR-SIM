from equipment import Equipment

class Relic(Equipment):
    name = "Relic"
    
    def __init__(self, setType: int):
        self.setType = setType
        
    def __str__(self) -> str:
        return f"{self.name} ({self.setType}-pc)"