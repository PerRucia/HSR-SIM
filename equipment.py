'''
Returns 4 lists:
- list of buffs added
- list of debuffs added
- list of adv% adjustments
- lsit of spd adjustments
'''


class Equipment:
    def __init__(self, wearerRole: str):
        self.wearerRole = wearerRole
    
    def equip(self): # init function to add base buffs to wearer
        return [], [], [], []
    
    def useSkl(self):
        return [], [], [], []
    
    def useBsc(self):
        return [], [], [], []
    
    def useUlt(self):
        return [], [], [], []
    
    def useFua(self):
        return [], [], [], []
    
    def useHit(self):
        return [], [], [], []
    
    def allyTurn(self, turn, result):
        return [], [], [], []