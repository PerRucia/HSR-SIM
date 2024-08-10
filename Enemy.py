class Enemy:
    level = 95
    
    def __init__(self, spd, toughness, actionOrder):
        self.spd = spd
        self.toughness = toughness
        self.actionOrder = actionOrder