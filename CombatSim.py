import logging
from Enemy import Enemy
from Summons import *
from HelperFuncs import *
from Misc import *
from Trackers import *

from Characters.Feixiao import Feixiao
from Characters.Robin import Robin
from Characters.Jiaoqiu import Jiaoqiu
from Characters.Aventurine import Aventurine
from Characters.Moze import Moze
from Characters.Sparkle import Sparkle
from Characters.Hunt7th import Hunt7th
from Characters.RuanMei import RuanMei

cycleLimit = 5 # comment out this line if running the simulator from an external script
log = True

def startSimulator(cycleLimit = 5, s1: Character = None, s2: Character = None, s3: Character = None, s4: Character = None, outputLog: bool = False, weak = None) -> str:
    
    # =============== SETTINGS ===============
    # Enemy Settings
    enemyLevel = 95
    numEnemies = 2
    enemySPD = [158.4, 145.2] # make sure that the number of entries in this list is the same as "numEnemies"
    toughness = [100, 100] # make sure that the number of entries in this list is the same as "numEnemies"
    attackTypeRatio = atkRatio # from Misc.py
    weaknesses = weak if weak else [Element.WIND, Element.FIRE, Element.IMAGINARY, Element.LIGHTNING]
    actionOrder = [1, 1, 2] # determines how many attacks enemies will have per turn

    # Character Settings
    if all([a is None for a in [s1, s2, s3, s4]]):
        slot1 = Feixiao(0, Role.DPS, 0, eidolon=0, rotation=["E"])
        slot2 = Aventurine(1, Role.SUS, 0, eidolon=0)
        slot3 = RuanMei(2, Role.SUP1, 0, eidolon=1)
        slot4 = Moze(3, Role.SUBDPS, 0, eidolon=6)
        
    # Simulation Settings   
    totalEnemyAttacks = 0
    logLevel = logging.CRITICAL
    # CRITICAL: Only prints the main action taken during each turn + ultimates
    # WARNING: Prints the above plus details on all actions recorded during the turn (FuA/Bonus attacks etc.), and all AV adjustments
    # INFO: Prints the above plus buff and debuff expiry, speed adjustments, av of all chars at the start of each turn
    # DEBUG: Prints the above plus all associated buffs and debuffs present during each turn
    # =============== END OF SETTINGS ===============
    
    # Logging Config
    if not s1:
        playerTeam = [slot1, slot2, slot3, slot4]
    else:
        playerTeam = [s1, s2, s3, s4]
        
    if outputLog:
        log_folder = "Output"
        teamInfo = "".join([char.name for char in playerTeam])
        enemyInfo = f"_{numEnemies}Enemies_{cycleLimit}Cycles"
        logging.basicConfig(
            filename=f"{log_folder}/{teamInfo}{enemyInfo}.log", 
            level=logLevel,
            format="%(message)s",
            filemode="w"
        )   
    else:
        logging.disable(logging.CRITICAL)  # Disable all logging messages

    avLimit = cycleLimit * 100 + 50
    simAV = 0
    
    # Damage Module
    dmg = DmgTracker()
    
    # Skill Point Module
    startingSP = 3 + [p.relic1.name for p in playerTeam if p.relic1.setType == 4].count("Passerby of Wandering Cloud")
    maxSP = (8 if findCharName(playerTeam, "Sparkle").eidolon >= 4 else 7) if inTeam(playerTeam, "Sparkle") else 5
    spTracker = SpTracker(startingSP, maxSP)
    
    # Summons
    summons = addSummons([p for p in playerTeam if p.hasSummon])

    # Print Enemy Info
    eTeam = []
    for i in range(numEnemies):
        adjList = []
        if (i - 1) >= 0:
            adjList.append(i - 1)
        if (i + 1) < numEnemies:
            adjList.append(i + 1)

        eTeam.append(Enemy(i, enemyLevel, enemySPD[i], toughness[i], actionOrder, weaknesses, adjList))
        
    logging.critical("Enemy Team:")
    for enemy in eTeam:
        logging.critical(enemy)
        
    # Print Char Info
    logging.critical("\nPlayer Team:")
    for char in playerTeam:
        logging.critical(f"{char}\n")

    # Setup equipment and char traces
    teamBuffs, enemyDebuffs, advList, delayList = [], [], [], []
    for char in playerTeam:
        initBuffs, initDebuffs, initAdv, initDelay = char.equip()
        teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, initBuffs, initDebuffs, initAdv, initDelay)

    # Setup initial AV
    for char in playerTeam:
        initCharAV(char, teamBuffs) # apply any pre-existing speed buffs

    logging.warning("\nInitial AV Adjustments")
    avAdjustment(playerTeam, advList) # apply any "on battle start" advances
    advList = [] # clear advList after applying

    logging.warning("\nInitial Enemy Delays")
    delayList = delayAdjustment(eTeam, delayList, enemyDebuffs) # apply any "on battle start" delays

    allUnits = sortUnits(playerTeam + eTeam + summons)
    setPriority(allUnits)

    # Simulator Loop
    logging.critical("\n==========COMBAT SIMULATION STARTED==========")

    while simAV < avLimit:

        unit = allUnits[0] # Find next turn
        av = unit.currAV
        simAV += av
        turnList = []
        if simAV > avLimit: # don't parse turn once over avLimit
            break
        logging.critical("\n<<< NEW TURN >>>")
        # Reduce AV of all chars
        for u in allUnits:
            u.standardAVred(av)
            logging.info(f"-    {u.name} AV: {u.currAV:.3f}")
        logging.info("")
            
        # Apply any special effects
        teamBuffs, enemyDebuffs, advList, delayList = handleSpecialEffects(unit, playerTeam, summons, eTeam, teamBuffs, enemyDebuffs, advList, delayList, "START", spTracker, dmg)
        
        # Check if any unit can ult
        teamBuffs, enemyDebuffs, advList, delayList = handleUlts(playerTeam, summons, eTeam, teamBuffs, enemyDebuffs, advList, delayList, spTracker, dmg)
        
        # Handle unit Turns
        if not unit.isChar(): # Enemy turn
            numAttacks = unit.takeTurn()
            totalEnemyAttacks += numAttacks
            logging.critical(f"ACTION > [ENEMY] TotalAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {numAttacks} attacks")
            for i in range(numAttacks):
                for char in playerTeam:
                    bl, dbl, al, dl, tl = char.useHit(unit.enemyID)
                    teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
                    turnList.extend(tl)
            energyList = addEnergy(playerTeam, eTeam, numAttacks, attackTypeRatio, teamBuffs) # might be useful someday lol
            logging.warning(f"    CharEnergy - {playerTeam[0].name}: {playerTeam[0].currEnergy:.3f} | {playerTeam[1].name}: {playerTeam[1].currEnergy:.3f} | {playerTeam[2].name}: {playerTeam[2].currEnergy:.3f} | {playerTeam[3].name}: {playerTeam[3].currEnergy:.3f}")
            dmg.addDebuffDMG(takeDebuffDMG(unit, playerTeam, teamBuffs, enemyDebuffs))
        elif unit.isChar() and not unit.isSummon(): # Character Turn
            moveType = unit.takeTurn()
            logging.critical(f"ACTION > [CHAR] TotalAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {moveType}-move")
            teamBuffs = tickBuffs(unit, teamBuffs, "START")
            if moveType == "E":
                bl, dbl, al, dl, tl = unit.useSkl()
            elif moveType == "A":
                bl, dbl, al, dl, tl = unit.useBsc()
            else:
                print("Invalid move type!")
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)
        elif unit.isChar() and unit.isSummon():
            logging.critical(f"ACTION > [SUMMON] TotalAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name}") # Summon logic
            bl, dbl, al, dl, tl = unit.takeTurn()
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)
            
        # Handle any pending attacks:
        teamBuffs, enemyDebuffs, advList, delayList, turnList = processTurnList(turnList, playerTeam, summons, eTeam, teamBuffs, enemyDebuffs, advList, delayList, spTracker, dmg)
        
        # Handle any errGain from unit turns
        teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
        
        # Check if any unit can ult
        teamBuffs, enemyDebuffs, advList, delayList = handleUlts(playerTeam, summons, eTeam, teamBuffs, enemyDebuffs, advList, delayList, spTracker, dmg)
        
        if unit.isChar() and not unit.isSummon(): 
            teamBuffs = tickBuffs(unit, teamBuffs, "END") # THIS MARKS THE END OF THE PLAYER TURN
        elif not unit.isChar():
            enemyDebuffs = tickDebuffs(unit, enemyDebuffs) # THIS MARKS THE END OF THE ENEMY TURN
        
        # Apply any special effects
        teamBuffs, enemyDebuffs, advList, delayList = handleSpecialEffects(unit, playerTeam, summons, eTeam, teamBuffs, enemyDebuffs, advList, delayList, "END", spTracker, dmg)
        
        # Check if any unit can ult
        teamBuffs, enemyDebuffs, advList, delayList = handleUlts(playerTeam, summons, eTeam, teamBuffs, enemyDebuffs, advList, delayList, spTracker, dmg)
        
        # Apply any speed adjustments
        spdAdjustment(playerTeam, teamBuffs)
        enemySPDAdjustment(eTeam, enemyDebuffs)
        
        # Reset the AV of the current unit by checking its current speed
        if not unit.isChar() or not unit.isSummon():
            resetUnitAV(unit, teamBuffs, enemyDebuffs)
            logging.warning(f"AV     > {unit.name} AV reset to {unit.currAV:.3f} | {unit.currSPD:.3f} SPD")
        
        allUnits = sortUnits(allUnits)
        # Reset priorities
        setPriority(allUnits)
        
        # Apply any enemy delays
        delayList = delayAdjustment(eTeam, delayList, enemyDebuffs)
        
        # Apply any character/summon AV adjustments
        avAdjustment(playerTeam + summons, advList)
        advList = []
        
        if unit.isChar() and unit.isSummon():
            resetUnitAV(unit, [], []) # summons cannot be advanced during their own turn
            logging.warning(f"AV     > {unit.name} AV reset to {unit.currAV:.3f} | {unit.currSPD:.3f} SPD")
            
        allUnits = sortUnits(allUnits)
        
    logging.critical("\n==========COMBAT SIMULATION ENDED==========")

    # Extra calculations
    for char in playerTeam:
        if char.name == "Yunli":
            char.hitMultiplier = char.ults / totalEnemyAttacks

    logging.critical("\n==========SIMULATION RESULTS==========")
    
    # Print damage info
    charDMG = 0
    dmgList = []
    for char in playerTeam:
        res, currCharDMG = char.gettotalDMG()
        dmgList.append(currCharDMG)
        charDMG += currCharDMG
    dpavList = [i / avLimit for i in dmgList]
    percentList = [i / dmg.getTotalDMG() * 100 for i in dmgList]

    logging.critical(f"TOTAL TEAM DMG: {dmg.getTotalDMG():.3f} | AV: {avLimit}")
    logging.critical(f"TEAM DPAV: {dmg.getTotalDMG() / avLimit:.3f}")
    logging.critical(f"DEBUFF DMG: {dmg.getDebuffDMG():.3f} | CHAR DMG: {dmg.getActionDMG():.3f} | WB DMG: {dmg.getWeaknessBreakDMG():.3f}")
    logging.critical(f"SP GAINED: {spTracker.getSPGain()} | SP USED: {spTracker.getSPUsed()} | Enemy Attacks: {totalEnemyAttacks}")
    res = ""
    i = 0
    for char in playerTeam:
        res += f"\n{char.name} DPAV: {dpavList[i]:.3f}, {percentList[i]:.3f}%"
        i += 1
        
    logging.critical(f"{res}\n")

    for char in playerTeam:
        res, charDMG = char.gettotalDMG()
        logging.critical(f"{char.name} > Total DMG: {charDMG:.3f} | Basics: {char.basics} | Skills: {char.skills} | Ults: {char.ults} | FuAs: {char.fuas} | Leftover AV: {char.currAV if char.currAV < 500 else char.charge:.3f} | Excess Energy: {char.currEnergy:.3f}")
        logging.critical(res)
    
    return f"DPAV: {dmg.getTotalDMG() / avLimit:.3f} | SP Used: {spTracker.getSPUsed()}, SP Gain: {spTracker.getSPGain()}"

if __name__ == "__main__":
    # Start the simulator with logging output to a file
    print(startSimulator(cycleLimit=cycleLimit, outputLog=log))