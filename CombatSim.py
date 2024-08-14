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

# Print Char Info
logging.critical("\nPlayer Team:")
for char in playerTeam:
    logging.critical(char)
    logging.critical("")

# Setup equipment and char traces
teamBuffs, enemyDebuffs, advList, delayList = [], [], [], [Delay("TestDelay", 0.2, 0, False, False)]
for char in playerTeam:
    tempBuffs, tempDebuffs, tempAdv, tempDelay = char.equip()
    teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
# Setup initial AV
for char in playerTeam:
    initCharAV(char, teamBuffs) # apply any pre-existing speed buffs

logging.info("\nInitial AV Adjustments")
avAdjustment(playerTeam, advList) # apply any "on battle start" advances
advList = [] # clear advList after applying

logging.info("\nInitial Enemy Delays")
delayList = delayAdjustment(eTeam, delayList, enemyDebuffs) # apply any "on battle start" delays

allUnits = sortUnits(playerTeam + eTeam)
setPriority(allUnits)
    
# Simulator Loop
logging.critical("\n==========COMBAT SIMULATION STARTED==========")
simAV = 0

def processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList):
    while turnList:
        turn = turnList[0]
        logging.warning(turn)
        logging.debug("\n----------Team Buffs----------")
        [logging.debug(buff) for buff in teamBuffs]
        logging.debug("----------End of Buff List----------")
        logging.debug("\n----------Enemy Debuffs----------")
        [logging.debug(debuff) for debuff in enemyDebuffs]
        logging.debug("----------End of Debuff List----------")

        res, newDebuffs, newDelays = handleTurn(turn, playerTeam, eTeam, teamBuffs, enemyDebuffs)
        logging.warning(res)
        teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, [], newDebuffs, [], newDelays)
        for char in playerTeam:
            if char.role == turn.charRole:
                tempB, tempDB, tempA, tempD, newTurns = char.ownTurn(res)
            else:
                tempB, tempDB, tempA, tempD, newTurns = char.allyTurn(turn, res)
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempB, tempDB, tempA, tempD)
            turnList.extend(newTurns)

        turnList = turnList[1:]
    
    return teamBuffs, enemyDebuffs, advList, delayList

while simAV < avLimit:
    logging.critical("\n==========NEW TURN==========")
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
    teamBuffs, enemyDebuffs, advList, delayList = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    turnList = []
        
    # Check if any unit can ult
    for char in playerTeam:
        if char.canUseUlt():
            tempBuffs, tempDebuffs, tempAdvs, tempDelays, tempTurns = char.useUlt()
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
            turnList.extend(tempTurns)

    # Handle any new attacks from unit ults  
    teamBuffs, enemyDebuffs, advList, delayList = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
        
    # Apply any speed adjustments
    spdAdjustment(playerTeam, teamBuffs)
    enemySPDAdjustment(eTeam, enemyDebuffs)
    
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
    
logging.critical("\n==========COMBAT SIMULATION ENDED==========")

logging.critical("\n==========CHARACTER STATS==========")
totalDMG = 0
for char in playerTeam:
    logging.critical(char.name)
    res, dmg = char.gettotalDMG()
    logging.critical(res)
    totalDMG += dmg

logging.critical(f"DPAV: {totalDMG / avLimit:.3f}")