# src: Who is taking the turn DPS/SDPS/SUP/SUS
# targetID: Enemy ID to be attacked, middle enemy if it is a blast attack
# moveType: ST, BLAST, AOE, NA | NA refers to a non-attacking move
# atkType: BSC, SKL, ULT, FUA, NA
# element: WIN, FIR, ICE, LNG, PHY, IMG, QUA
# dmgSplit: Base multiplier split [main, adjacent], set adjacent to 0 for ST and AOE attacks
# brkSplit: Toughness reduction split [main, adjacent], set adjacent to 0 for ST and AOE attacks

class Turn:
    def __init__(self, src: str, targetID: int, moveType: str, atkType: list, element: list, dmgSplit: list, brkSplit: list, errGain: float, scaling: str):
        self.src = src
        self.targetID = targetID
        self.moveType = moveType
        self.atkType = atkType
        self.element = element
        self.dmgSplit = dmgSplit
        self.brkSplit = brkSplit
        self.errGain = errGain
        self.scaling = scaling
        
    def __str__(self) -> str:
        res = f"{self.moveType} attack | {self.element} | {self.atkType}\n"
        res += f"Scaling: {self.scaling} | Enermy Target: {self.targetID}\n"
        res += f"DMG/BREAK Splits: {self.dmgSplit}/{self.brkSplit}\n"
        res += f"Energy Gained: {self.errGain}\n"
        return res
    