'''
Returns 4 lists:
- list of buffs added
- list of debuffs added
- list of adv% adjustments
- list of enemy debuffs to be applied
'''
from Turn import *
from Result import *
from Misc import *

class Equipment:
    def __init__(self, wearerRole: Scaling):
        self.wearerRole = wearerRole
    
    def equip(self, enemyID=-1): # init function to add base buffs to wearer
        return [], [], [], []
    
    def useSkl(self, enemyID=-1):
        return [], [], [], []
    
    def useBsc(self, enemyID=-1):
        return [], [], [], []
    
    def useUlt(self, enemyID=-1):
        return [], [], [], []
    
    def useFua(self, enemyID=-1):
        return [], [], [], []
    
    def useHit(self, enemyID=-1):
        return [], [], [], []
    
    def allyTurn(self, turn: Turn, result: Result):
        return [], [], [], []
    
    def ownTurn(self, result: Result):
        return [], [], [], []
    
    def specialStart(self, special: Special):
        return [], [], [], []
    
    def specialEnd(self, special: Special):
        return [], [], [], []