from equipment import Equipment

class Lightcone(Equipment):
    name = "Lightcone"
    path = "None"
    baseHP = 0
    baseATK = 0
    baseDEf = 0
    
    def __init__(self, level: int):
        self.level = level
        
    def __str__(self):
        return f"{self.name} S{self.level}"
    
a = Lightcone(5)