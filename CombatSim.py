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
teamBuffs, enemyDebuffs, enemyDelay = [], [], []

for char in playerTeam:
    tempBuffList, tempDebuffList, tempAdvList, tempDelayList = char.equip()
    buffList = parseBuffs(tempBuffList, playerTeam)
    debuffList = parseDebuffs(tempDebuffList, enemyTeam)
    advList = parseAdvance(tempAdvList, playerTeam)
    delayList = parseDebuffs(tempDelayList, enemyTeam)
    addBuffs(teamBuffs, buffList)
    addBuffs(enemyDebuffs, debuffList)

# Setup initial AV
for char in playerTeam:
    initCharAV(char, teamBuffs) # apply any pre-existing speed buffs

avAdjustment(playerTeam, advList) # apply any "on battle start" advances
advList = [] # clear advList after applying

allUnits = sortUnits(playerTeam + enemyTeam)
setPriority(allUnits)

for u in allUnits:
    print(u.name, u.priority, u.currAV)
# Simulator Loop
simAV = 0
while simAV < avLimit:
    # Find next turn
    unit = allUnits[0]
    break
    # Handle the turn
        # Check whether its character or enemy turn
        
        # Enemy Turn
        
        # Character Turn
        
    # Apply any speed adjustments
    
        # After speed adjustments applied
        
    # Apply any AV adjustments
        # Add 10 to priority if any char is forwarded
