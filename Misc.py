from enum import Enum, auto

bonusDMG = ["AvenFUAExtras", "TYAllyBonus", "TYBeneBonus", "YunliCullBounce", "FeixiaoUlt", "RobinConcertoDMG", "H7UltEnhancedBSCExtras", "H7EnhancedBSCExtras", "MozeBonusDMG", "RuanMeiBreakBonus", "LingshaFuaExtra"]
wbMultiplier = 3767.5533
eleDct = {"PHY": 2.0, "FIR": 2.0, "WIN": 1.5, "ICE": 1.0, "LNG": 1.0, "QUA": 0.5, "IMG": 0.5}

atkRatio = [0.55, 0.2, 0.25] # Single Target, Blast Attack, AOE Attack splits for enemy behaviour

class BuffType(Enum):
    SPD = auto()
    HP = auto()
    ATK = auto()
    DEF = auto()
    HP_PERCENT = auto()
    ATK_PERCENT = auto()
    DEF_PERCENT = auto()
    CR_PERCENT = auto()
    CD_PERCENT = auto()
    BE_PERCENT = auto()
    OGH_PERCENT = auto()
    ERR_PERCENT = auto()
    EHR_PERCENT = auto()
    ERS_PERCENT = auto()
    DMG_PERCENT = auto()
    SHRED = auto()
    VULN = auto()
    PEN = auto()
    ERR_T = auto()
    ERR_F = auto()
    
class Element(Enum):
    WIND = "WIN"
    FIRE = "FIR"
    LIGHTNING = "LNG"
    IMAGINARY = "IMG"
    QUANTUM = "QUA"
    ICE = "ICE"
    PHYSICAL = "PHY"
    
class Path(Enum):
    HUNT = 3
    ERUDTION = 3
    HARMONY = 4
    NIHILITY = 4
    ABUNDANCE = 4
    DESTRUCTION = 5
    PRESERVATION = 6
    
class Role(Enum):
    DPS = auto()
    SUBDPS1 = auto()
    SUBDPS2 = auto()
    SUP1 = auto()
    SUP2 = auto()
    SUS = auto()
    
class Scaling(Enum):
    ATK = auto()
    HP = auto()
    DEF = auto()