from enum import Enum, auto

bonusDMG = {"AvenFUAExtras", "TYAllyBonus", "TYBeneBonus", "YunliCullBounce", "FeixiaoUlt", "RobinConcertoDMG", "H7UltEnhancedBSCExtras", "H7EnhancedBSCExtras", "MozeBonusDMG", "RuanMeiBreakBonus", "LingshaFuaExtra",
            "RatioE2Bonus", "JadeBonusDMG"}
wbMultiplier = 3767.5533
eleDct = {"PHY": 2.0, "FIR": 2.0, "WIN": 1.5, "ICE": 1.0, "LNG": 1.0, "QUA": 0.5, "IMG": 0.5}
atkRatio = [0.55, 0.2, 0.25] # Single Target, Blast Attack, AOE Attack splits for enemy behaviour

class Pwr(Enum):
    SPD = "SPD"
    HP = "HP"
    ATK = "ATK"
    DEF = "DEF"
    SPD_PERCENT = "SPD%"
    HP_PERCENT = "HP%"
    ATK_PERCENT = "ATK%"
    DEF_PERCENT = "DEF%"
    CR_PERCENT = "CR%"
    CD_PERCENT = "CD%"
    BE_PERCENT = "BE%"
    WB_EFF = "WBE%"
    OGH_PERCENT = "OGH%"
    ERR_PERCENT = "ERR%"
    EHR_PERCENT = "EHR%"
    ERS_PERCENT = "ERS%"
    DMG_PERCENT = "DMG%"
    SHRED = "SHRED"
    VULN = "VULN"
    PEN = "PEN"
    ERR_T = "ERR_T"
    ERR_F = "ERR_F"
    ICEPEN = "ICEPEN"
    FIRPEN = "FIRPEN"
    LNGPEN = "LNGPEN"
    WINPEN = "WINPEN"
    PHYPEN = "PHYPEN"
    QUAPEN = "QUAPEN"
    IMGPEN = "IMGPEN"
    ENTANGLE = "ENTANGLE"
    SHOCK = "SHOCK"
    WINDSHEAR = "WINDSHEAR"
    FREEZE = "FREEZE"
    BURN = "BURN"
    BLEED = "BLEED"
    
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
    SUBDPS = auto()
    SUP1 = auto()
    SUP2 = auto()
    SUS = auto()
    ALL = auto()
    SELF = auto()
    TEAM = auto()
    ENEMY = auto()
    NUMBY = auto()
    FUYUAN = auto()
    
class Scaling(Enum):
    ATK = "ATK%"
    HP = "HP%"
    DEF = "DEF%"
    
class TickDown(Enum):
    END = auto()
    START = auto()
    PERM = auto()
    
class AtkTarget(Enum):
    SINGLE = "ST"
    BLAST = "BLAST"
    AOE = "AOE"
    NA = "NA"
    SPECIAL = "SPECIAL"
    STBREAK = "STBREAK"
    BLASTBREAK = "BLASTBREAK"
    AOEBREAK = "AOEBREAK"
    STSB = "STSBREAK"
    BLASTSB = "BLASTSBREAK"
    AOESB = "AOESBREAK"
    DOT = "DOT"
    DEBUFF = "DEBUFF"
    
class Move(Enum):
    BSC = auto()
    SKL = auto()
    ULT = auto()
    FUA = auto()
    BRK = auto()
    SBK = auto()
    DOT = auto()
    ALL = auto()
    TECH = auto()
    SPECIAL = auto() # special attacks, only takes effect from "ALL"-type buffs
    # Special Buffs/Moves
    DUKEFUA = auto()
    DUKEULT = auto()
    TOPAZULT = auto()
    TOPAZFUA = auto()
    UEBSC = auto()
    EBSC = auto()

penDct = {Element.PHYSICAL: Pwr.PHYPEN, Element.FIRE: Pwr.FIRPEN, Element.WIND: Pwr.WINPEN, Element.ICE: Pwr.ICEPEN, Element.QUANTUM: Pwr.QUAPEN, Element.LIGHTNING: Pwr.LNGPEN, Element.IMAGINARY: Pwr.IMGPEN}