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
spUsed = 0

# =============== END OF SETTINGS ===============
log_folder = "Output"
teamInfo = "".join([char.name for char in playerTeam])
enemyInfo = f"_{numEnemies}-Enemies"
logging.basicConfig(filename=f"{log_folder}/{teamInfo}{enemyInfo}.log", 
                    level=logging.CRITICAL,
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

def processTurnList(turnList: list[Turn], playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList):
    spGain = 0
    spUsed = 0
    while turnList:
        turn = turnList[0]
        if turn.spChange < 0:
            spUsed = spUsed - turn.spChange
        elif turn.spChange > 0:
            spGain = spUsed + turn.spChange
        logging.warning(turn)
        logging.debug("\n----------Char Buffs----------")
        [logging.debug(buff) for buff in teamBuffs if buff.target == turn.charRole]
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
    
    return teamBuffs, enemyDebuffs, advList, delayList, spGain, spUsed

while simAV < avLimit:
    if simAV > avLimit: # don't parse turn once over avLimit
        break
    logging.critical("\n==========NEW TURN==========")
    unit = allUnits[0] # Find next turn
    av = unit.currAV
    simAV += av

    turnList = []
    
    # Reduce AV of all chars
    for u in allUnits:
        if u != unit:
            u.reduceAV(av)
        
    # Handle unit Turns
    if not unit.isChar(): # Enemy turn
        numAttacks = unit.takeTurn()
        logging.critical(f"CumAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {numAttacks} attacks")
        for i in range(numAttacks):
            for char in playerTeam:
                tempB, tempDB, tempA, tempD, tempT = char.useHit(unit.enemyID)
                teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
                turnList.extend(tempT)
        addEnergy(playerTeam, numAttacks, attackTypeRatio, teamBuffs)
        takeDot(unit, eTeam, playerTeam, teamBuffs, enemyDebuffs)
        enemyDebuffs = tickDebuffs(enemy, enemyDebuffs)
    else: # Character Turn
        moveType = unit.takeTurn()
        logging.critical(f"CumAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {moveType}-move")
        teamBuffs = tickBuffs(unit.role, teamBuffs, "START")
        if moveType == "E":
            tempB, tempDB, tempA, tempD, tempT = char.useSkl()
        elif moveType == "A":
            tempB, tempDB, tempA, tempD, tempT = char.useBsc()
        teamBuffs = tickBuffs(unit.role, teamBuffs, "END")
        teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
        turnList.extend(tempT)
        
    # Handle any pending attacks:
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    turnList = []
    spGain += spPlus
    spUsed += spMinus
    
    # Check if any unit can ult
    for char in playerTeam:
        if char.canUseUlt():
            tempBuffs, tempDebuffs, tempAdvs, tempDelays, tempTurns = char.useUlt()
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, tempBuffs, tempDebuffs, tempAdv, tempDelay)
            turnList.extend(tempTurns)

    # Handle any new attacks from unit ults  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    
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

logging.critical("\n==========SIMULATION RESULTS==========")
dotDMG = 0
charDMG = 0
for enemy in eTeam:
    dotDMG += enemy.dotDMG
for char in playerTeam:
    res, dmg = char.gettotalDMG()
    charDMG += dmg
totalDMG = dotDMG + charDMG

logging.critical(f"TOTAL TEAM DMG: {totalDMG:.3f} | AV: {avLimit}")
logging.critical(f"TEAM DPAV: {totalDMG / avLimit:.3f}")
logging.critical(f"DOT DMG: {dotDMG:.3f} | CHAR DMG: {charDMG:.3f}")
logging.critical(f"SP GAINED: {spGain} | SP USED: {spUsed}")

for char in playerTeam:
    res, dmg = char.gettotalDMG()
    logging.critical(f"\n{char.name} | Total DMG: {dmg:.3f} | Team%: {dmg / totalDMG * 100:.3f} | Basics: {char.basics} | Skills: {char.skills} | Ults: {char.ults} | FuAs: {char.fuas}")
    logging.critical(f"Leftover AV: {char.currAV:.3f} | Excess Energy: {char.currEnergy:.3f}")
    logging.critical(res)

