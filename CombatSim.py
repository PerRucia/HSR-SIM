from Enemy import Enemy
from Characters.Yunli import Yunli
from HelperFuncs import *

# Enemy Settings
enemyTeam = []
enemyLevel = 95
enemySPD = [158.4, 145.2]
attackTypeRatio = [0.55, 0.20, 0.25] # ST/BLAST/AOE
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

# Simulator Loop
simAV = 0
while simAV < avLimit:
    # Check whether its enemy/char turn
    turnType, av, unit = findNextTurn(enemyTeam + playerTeam)
    turnList = []
    simAV += av
    # Enemy Turn logic
    if not turnType:
        numAttacks = unit.takeTurn()
        addEnergy(playerTeam, numAttacks, attackTypeRatio)
        tempBuffList, tempDebuffList, advList = [], [], []
        for char in playerTeam:
            bl, dbl, al, turn = char.useHit(unit.enemyID)
            if turn.moveType != "NA":
                turnList.append(turn)
                tempBuffList.extend(parseBuffs(bl))
                tempDebuffList.extend(parseDebuffs(dbl))
                advList.extend(parseAdvance(al))
                
        enemyDebuffs = tickDebuffs(unit.enemyID, enemyDebuffs) # end of enemy turn, tick down debuffs
        addBuffs(enemyDebuffs, tempDebuffList) # add new buffs to team buffs
        addBuffs(teamBuffs, tempBuffList) # add new debuffs to enemy
        
    # Char Turn Logic
    elif turnType:
        teamBuffs = tickBuffs(unit.role, teamBuffs)
        atkType = unit.takeTurn()
        if atkType == "E":
            bl, dbl, al, turn = unit.useSkl()
        elif atkType == "A":
            bl, dbl, al, turn = unit.useBsc()
    # Check if any ults can be used

    # Apply any speed adjustments
    
    # Apply any AV adjustments

