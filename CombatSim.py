import logging
from Enemy import Enemy
from Characters.Yunli import Yunli
from HelperFuncs import *

# Enemy Settings
enemyTeam = []
enemyLevel = 95
enemySPD = [158.4, 145.2]
attackTypeRatio = [0.55, 0.20, 0.25] # ST/BLAST/AOE splits for enemy attacks
toughness = 100
numEnemies = 2
weaknesses = ["PHY"]
actionOrder = [1,1,2]
for i in range(numEnemies):
    adjList = []
    if (i - 1) >= 0:
        adjList.append(i - 1)
    if (i + 1) < numEnemies:
        adjList.append(i + 1)

    enemyTeam.append(Enemy(i, enemyLevel, enemySPD[i], toughness, actionOrder, weaknesses, adjList))

# Character Settings
playerTeam = [Yunli(0, "DPS")]
teamBuffs, enemyDebuffs = [], []

# Simulation Settings
cycleLimit = 5
avLimit = 150 + 100 * (cycleLimit - 1)
startingSP = 3
spGain = 0
spSpent = 0

# =============== END OF SETTINGS ===============
logging.basicConfig(filename="Output/output.log", 
                    level=logging.DEBUG,
                    format="%(message)s",
                    filemode="w")

# Print Enemy Info
logging.critical("Enemy Team:")
for enemy in enemyTeam:
    logging.critical(enemy)
logging.critical("")

# Print Char Info
logging.critical("Player Team:")
for char in playerTeam:
    logging.critical(char)
    logging.critical("")

# Setup equipment and char traces
for char in playerTeam:
    tempBuffList, tempDebuffList, tempAdvList = char.equip()
    buffList = parseBuffs(tempBuffList, playerTeam)
    debuffList = parseDebuffs(tempDebuffList, enemyTeam)
    advList = parseAdvance(tempAdvList, playerTeam)
    addBuffs(teamBuffs, buffList)
    addBuffs(enemyDebuffs, debuffList)

# Setup initial AV
for char in playerTeam:
    resetCharAV(char, teamBuffs) # Apply any pre-existing speed buffs

for adv in advList:
    advanceChar(adv[0], adv[1], playerTeam, buffList) # Apply any "on battle start" action advance
advList = [] # clear advList after applying

allUnits = enemyTeam + playerTeam
# Simulator Loop
simAV = 0
while simAV < avLimit:
    # Check whether its enemy/char turn
    turnType, av, unit = findNextTurn(enemyTeam + playerTeam)
    turnList = []
    simAV += av
    logging.warning(f"CumAV: {simAV:.3f} | AV: {av:.3f} | {unit.name}")
    
    # Enemy Turn logic
    if not turnType:
        numAttacks = unit.takeTurn()
        addEnergy(playerTeam, numAttacks, attackTypeRatio, teamBuffs)
        tempBuffList, tempDebuffList, advList = [], [], []
        for char in playerTeam:
            bl, dbl, al, turnList = char.useHit(unit.enemyID)
            for i in range(numAttacks):
                turnList.extend(turnList)
                tempBuffList.extend(parseBuffs(bl, playerTeam))
                tempDebuffList.extend(parseDebuffs(dbl, enemyTeam))
                advList.extend(parseAdvance(al, playerTeam))
                    
        # Parse any character turns collected so far
        while turnList:
            turn = turnList[0]
            turnList.remove(turn)
            result = handleTurn(turnList[0], enemyTeam, playerTeam, buffList, debuffList)
            for char in playerTeam:
                bl, dbl, al, turn = char.allyTurn(turn, result)
        enemyDebuffs = tickDebuffs(unit.enemyID, enemyDebuffs) # end of enemy turn, tick down debuffs
        addBuffs(enemyDebuffs, tempDebuffList) # add new buffs to team buffs
        addBuffs(teamBuffs, tempBuffList) # add new debuffs to enemy
        
    # Char Turn Logic
    elif turnType:
        teamBuffs = tickBuffs(unit.role, teamBuffs) # start of char turn, tick down buffs
        atkType = unit.takeTurn()
        resetCharAV(unit, teamBuffs)
        if atkType == "E":
            bl, dbl, al, turn = unit.useSkl()
        elif atkType == "A":
            bl, dbl, al, turn = unit.useBsc()

    # Reduce AV of all units
    for u in allUnits:
        if u == unit:
            continue
        u.reduceAV(av)
        
    # Check if any ults can be used

    # Apply any speed adjustments
    
    # Apply any AV adjustments

