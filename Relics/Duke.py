from Relic import Relic
from Buff import Buff
from Misc import *

class DukeTopaz(Relic):
    name = "The Ashblazing Grand Duke"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("DukeDMG", "DMG%", 0.20, self.wearerRole, ["FUA"], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            bl.append(Buff("DukeBasicATK", "ATK%", 0.06, self.wearerRole, ["BSC"], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("DukeFuaATK", "ATK%", 0.24, self.wearerRole, ["TOPAZFUA"], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("DukeUltATK", "ATK%", 0.312, self.wearerRole, ["TOPAZULT"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList
    
class DukeFeixiao(Relic):
    name = "The Ashblazing Grand Duke"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("DukeDMG", "DMG%", 0.20, self.wearerRole, ["FUA"], 1, 1, Role.SELF, TickDown.PERM))
        if self.setType == 4:
            bl.append(Buff("DukeBasicATK", "ATK%", 0.144, self.wearerRole, ["BSC"], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("DukeSklATK", "ATK%", 0.12, self.wearerRole, ["SKL"], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("DukeFuaATK", "ATK%", 0.06, self.wearerRole, ["DUKEFUA"], 1, 1, Role.SELF, TickDown.PERM))
            bl.append(Buff("DukeUltATK", "ATK%", 0.3543, self.wearerRole, ["DUKEULT"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList

class DukeMoze(Relic):
    name = "The Ashblazing Grand Duke"
    
    def __init__(self, wearerRole, setType):
        super().__init__(wearerRole, setType)
        
    def equip(self):
        bl, debuffList, advList, delayList = super().equip()
        bl.append(Buff("DukeDMG", "DMG%", 0.20, self.wearerRole, ["FUA"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("DukeFuaATK", "ATK%", 0.288, self.wearerRole, ["DUKEFUA"], 1, 1, Role.SELF, TickDown.PERM))
        bl.append(Buff("DukeUltATK", "ATK%", 0.06, self.wearerRole, ["DUKEULT"], 1, 1, Role.SELF, TickDown.PERM))
        return bl, debuffList, advList, delayList