import logging
from Enemy import Enemy
from Characters.Yunli import Yunli
from HelperFuncs import *

# Enemy Settings
enemyLevel = 95
enemySPD = [158.4, 145.2]
attackTypeRatio = [0.55, 0.20, 0.25] # ST/BLAST/AOE splits for enemy attacks
toughness = 100
numEnemies = 2
weaknesses = ["PHY"]
actionOrder = [1,1,2]

# Character Settings
playerTeam = [Yunli(0, "DPS")]

# Simulation Settings
cycleLimit = 5
avLimit = 150 + 100 * (cycleLimit - 1)
startingSP = 3
spGain = 0
spSpent = 0

# =============== END OF SETTINGS ===============
log_folder = "Output"
teamInfo = "".join([char.name for char in playerTeam])
enemyInfo = f"_{numEnemies}-Enemies"
logging.basicConfig(filename=f"{log_folder}/{teamInfo}{enemyInfo}.log", 
                    level=logging.WARNING,
                    format="%(message)s",
                    filemode="w")

# Print Enemy Info
eTeam = []
for i in range(numEnemies):
    adjList = []
    if (i - 1) >= 0:
        adjList.append(i - 1)
    if (i + 1) < numEnemies:
        adjList.append(i + 1)

    eTeam.append(Enemy(i, enemyLevel, enemySPD[i], toughness, actionOrder, weaknesses, adjList))
    
logging.critical("Enemy Team:")
for enemy in eTeam:
    logging.critical(enemy)
logging.critical("")

# Print Char Info
logging.critical("Player Team:")
for char in playerTeam:
    logging.critical(char)
    logging.critical("")

# Setup equipment and char traces
teamBuffs, enemyDebuffs, advList, delayList = [], [], [], []
for char in playerTeam:
    tempBuffs, tempDebuffs, tempAdv, tempDelay = char.equip()
    teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
# Setup initial AV
for char in playerTeam:
    initCharAV(char, teamBuffs) # apply any pre-existing speed buffs

avAdjustment(playerTeam, advList) # apply any "on battle start" advances
advList = [] # clear advList after applying

delayList = delayAdjustment(eTeam, delayList, enemyDebuffs) # apply any "on battle start" delays

allUnits = sortUnits(playerTeam + eTeam)
setPriority(allUnits)
    
# Simulator Loop
simAV = 0
while simAV < avLimit:
    logging.critical("")
    # Find next turn
    unit = allUnits[0]
    av = unit.currAV
    simAV += av
    if simAV > avLimit: # don't parse turn once over avLimit
        break
    turnList = []
    
    # Reduce AV of all chars
    for u in allUnits:
        if u != unit:
            u.reduceAV(av)
        
    # Handle unit Turns
    if not unit.isChar(): # Enemy turn
        numAttacks = unit.takeTurn()
        for i in range(numAttacks):
            for char in playerTeam:
                tempB, tempDB, tempA, tempD, tempT = char.useHit(unit.enemyID)
                teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
                turnList.extend(tempT)
        addEnergy(playerTeam, numAttacks, attackTypeRatio, teamBuffs)
        logging.critical(f"CumAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {numAttacks} attacks")
    else: # Character Turn
        moveType = unit.takeTurn()
        if moveType == "E":
            tempB, tempDB, tempA, tempD, tempT = char.useSkl()
        elif moveType == "A":
            tempB, tempDB, tempA, tempD, tempT = char.useBsc()
        teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
        turnList.extend(tempT)
        logging.critical(f"CumAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {moveType}-move")
    # Handle any pending attacks:
    while turnList:
        turn = turnList[0]
        logging.warning(turn)
        turnList = turnList[1:]
        
    # Check if any unit can ult
    for char in playerTeam:
        if char.canUseUlt():
            tempBuffs, tempDebuffs, tempAdvs, tempDelays, tempTurns = char.useUlt()
    
    # Apply any speed adjustments
    spdAdjustment(playerTeam, teamBuffs)
    
    # Reset the AV of the current unit by checking its current speed
    resetUnitAV(unit, teamBuffs, enemyDebuffs)
    
    # Reset priorities
    setPriority(allUnits)
    
    # Apply any enemy delays
    delayList = delayAdjustment(eTeam, delayList, enemyDebuffs)
    
    # Apply any character AV adjustments
    avAdjustment(playerTeam, advList)
    advList = []
    
    allUnits = sortUnits(allUnits)
    
