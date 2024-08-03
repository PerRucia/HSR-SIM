class Equipment:
    def __init__(self):
        pass
    
    def equip(self): # init function to add base buffs to wearer
        return ["DefaultBuff"], ["DefaultDebuff"]
    
    def useSkl(self):
        return ["DefaultBuff"], ["DefaultDebuff"], "DefaultMove"
    
    def useBsc(self):
        return ["DefaultBuff"], ["DefaultDebuff"], "DefaultMove"
    
    def useUlt(self):
        return ["DefaultBuff"], ["DefaultDebuff"], "DefaultMove"
    
    def useFua(self):
        return ["DefaultBuff"], ["DefaultDebuff"], "DefaultMove"
    
    def useHit(self):
        return ["DefaultBuff"], ["DefaultDebuff"], "DefaultMove"
    
    def allyTurn(self, turn):
        return ["DefaultBuff"], ["DefaultDebuff"], "DefaultMove"