import logging
from Enemy import Enemy
from Summons import *
from HelperFuncs import *
from Misc import *
from Characters.Feixiao import Feixiao
# BiS Team
from Characters.Robin import Robin
from Characters.Topaz import Topaz
from Characters.Aventurine import Aventurine
# F2P Team
from Characters.Hunt7th import Hunt7th
from Characters.Pela import Pela
from Characters.Gallagher import Gallagher
# Extra Characters
from Characters.Jiaoqiu import Jiaoqiu
from Characters.Yunli import Yunli

# Enemy Settings
enemyLevel = 95
enemySPD = [158.4, 145.2] # make sure that the number of entries in this list is the same as "numEnemies"
attackTypeRatio = atkRatio # from Misc.py
toughness = 100
numEnemies = 2
weaknesses = [Element.WIND, Element.FIRE, Element.IMAGINARY, Element.LIGHTNING]
actionOrder = [1,1,2] # determines how many attacks enemies will have per turn

# Character Settings
slot1 = Feixiao(0, Role.DPS, 0, eidolon=0, sig=True)
slot2 = Robin(1, Role.SUP1, 0)
slot3 = Aventurine(2, Role.SUS, 0)
slot4 = Topaz(3, Role.SUBDPS, 0)

# Simulation Settings
cycleLimit = 50
avLimit = 150 + 100 * (cycleLimit - 1)
startingSP = 3
spGain = 0
spUsed = 0
totalEnemyAttacks = 0
logLevel = logging.CRITICAL
# CRITICAL: Only prints the main action taken during each turn + ultimates
# WARNING: Prints the above plus details on all actions recorded during the turn (FuA/Bonus attacks etc.), and all AV adjustments
# INFO: Prints the above plus buff and debuff expiry, speed adjustments, av of all chars at the start of each turn
# DEBUG: Prints the above plus all associated buffs and debuffs present during each turn
# =============== END OF SETTINGS ===============

# Logging Config
playerTeam = [slot1, slot2, slot3, slot4]
log_folder = "Output"
teamInfo = "".join([char.name for char in playerTeam])
enemyInfo = f"_{numEnemies}Enemies_{cycleLimit}Cycles"
logging.basicConfig(filename=f"{log_folder}/{teamInfo}{enemyInfo}.log", 
                    level=logLevel,
                    format="%(message)s",
                    filemode="w")


# Summons
summons = []
for char in playerTeam:
    if char.hasSummon:
        if char.name == "Topaz":
            summons.append(Numby(char.role, char.numbyRole))
        elif char.name == "Lingsha":
            summons.append(Fuyuan(char.role, char.fuyuanRole))
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
        logging.warning(f"    TURN   - {turn}")
        logging.debug("\n        ----------Char Buffs----------")
        [logging.debug(f"        {buff}") for buff in teamBuffs if (buff.target == turn.charRole and checkValidList(turn.atkType, buff.atkType))]
        logging.debug("        ----------End of Buff List----------")
        logging.debug("\n        ----------Enemy Debuffs----------")
        [logging.debug(f"        {debuff}") for debuff in enemyDebuffs if debuff.target == turn.targetID]
        logging.debug("        ----------End of Debuff List----------")

        res, newDebuffs, newDelays = handleTurn(turn, playerTeam, eTeam, teamBuffs, enemyDebuffs)
        if res.errGain > 0:
            char = findCharRole(playerTeam, res.charRole)
            logging.warning(f"    RESULT - {res} | {char.name}Energy: {min(char.maxEnergy, char.currEnergy + res.errGain):.3f}")
        else:
            logging.warning(f"    RESULT - {res}")
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

    unit = allUnits[0] # Find next turn
    av = unit.currAV
    simAV += av
    if simAV > avLimit: # don't parse turn once over avLimit
        break
    logging.critical("\n<<< NEW TURN >>>")
    turnList = []
    # Reduce AV of all chars
    for u in allUnits:
        u.standardAVred(av)
        logging.info(f"{u.name} AV: {u.currAV:.3f}")
    logging.info("")
        
    # Apply any special effects
    for char in playerTeam:
        if char.hasSpecial:
            spec = char.special()
            specRes = handleSpec(spec, unit, playerTeam, eTeam, teamBuffs, enemyDebuffs, "START")
            bl, dbl, al, dl, tl = char.handleSpecialStart(specRes)
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)    
            
    # Handle any attacks from special attacks  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    turnList = []        
    
    # Add Energy if any was provided from special effects
    teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
    # Check if any unit can ult
    for char in playerTeam:
        if char.canUseUlt():
            logging.critical(f"ULT    > {char.name} used their ultimate")
            bl, dbl, al, dl, tl = char.useUlt()
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)

    # Handle any new attacks from unit ults  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    turnList = []
    
    # Handle any errGain from unit ults
    teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
    
    # Handle unit Turns
    if not unit.isChar(): # Enemy turn
        numAttacks = unit.takeTurn()
        totalEnemyAttacks += numAttacks
        logging.critical(f"ENEMY  > TotalAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {numAttacks} attacks")
        for i in range(numAttacks):
            for char in playerTeam:
                bl, dbl, al, dl, tl = char.useHit(unit.enemyID)
                teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
                turnList.extend(tl)
        energyList = addEnergy(playerTeam, eTeam, numAttacks, attackTypeRatio, teamBuffs)
        logging.warning(f"    CharEnergy - {playerTeam[0].name}: {playerTeam[0].currEnergy:.3f} | {playerTeam[1].name}: {playerTeam[1].currEnergy:.3f} | {playerTeam[2].name}: {playerTeam[2].currEnergy:.3f} | {playerTeam[3].name}: {playerTeam[3].currEnergy:.3f}")
        takeDebuffDMG(unit, playerTeam, teamBuffs, enemyDebuffs)
    elif unit.isChar() and not unit.isSummon(): # Character Turn
        moveType = unit.takeTurn()
        logging.critical(f"ACTION > TotalAV: {simAV:.3f} | TurnAV: {av:.3f} | {unit.name} | {moveType}-move")
        teamBuffs = tickBuffs(unit.role, teamBuffs, "START")
        if moveType == "E":
            bl, dbl, al, dl, tl = unit.useSkl()
        elif moveType == "A":
            bl, dbl, al, dl, tl = unit.useBsc()
        teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
        turnList.extend(tl)
    elif unit.isChar() and unit.isSummon():
        logging.critical(f"SUMMON > TotalAV: {simAV:.3f} | TurnAV: {av:.3f}") # Summon logic
        bl, dbl, al, dl, tl = unit.takeTurn()
        teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
        turnList.extend(tl)
        
    # Handle any pending attacks:
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    turnList = []
    spGain += spPlus
    spUsed += spMinus
    
    # Handle any errGain from unit turns
    teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
    
    # Apply any special effects
    for char in playerTeam:
        if char.hasSpecial:
            spec = char.special()
            specRes = handleSpec(spec, unit, playerTeam, eTeam, teamBuffs, enemyDebuffs, "MIDDLE")
            bl, dbl, al, dl, tl = char.handleSpecialMiddle(specRes)
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)
    
    # Handle any attacks from special attacks  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    turnList = []        
    
    # Add Energy if any was provided from special effects
    teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
    
    # Check if any unit can ult
    for char in playerTeam:
        if char.canUseUlt():
            logging.critical(f"ULT    > {char.name} used their ultimate")
            bl, dbl, al, dl, tl = char.useUlt()
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)

    # Handle any new attacks from unit ults  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    turnList = []
    
    # Handle any errGain from unit ults
    teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
    
    if unit.isChar() and not unit.isSummon(): 
        teamBuffs = tickBuffs(unit.role, teamBuffs, "END") # THIS MARKS THE END OF THE PLAYER TURN
    elif not unit.isChar():
        enemyDebuffs = tickDebuffs(unit, enemyDebuffs) # THIS MARKS THE END OF THE ENEMY TURN
        
    # Apply any special effects
    for char in playerTeam:
        if char.hasSpecial:
            spec = char.special()
            specRes = handleSpec(spec, unit, playerTeam, eTeam, teamBuffs, enemyDebuffs, "END")
            bl, dbl, al, dl, tl = char.handleSpecialEnd(specRes)
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)
            
    # Handle any attacks from special attacks  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    turnList = []        
    
    # Add Energy if any was provided from special effects
    teamBuffs = handleEnergyFromBuffs(teamBuffs, enemyDebuffs, playerTeam, eTeam)
    
    # Check if any unit can ult
    for char in playerTeam:
        if char.canUseUlt():
            logging.critical(f"ULT    > {char.name} used their ultimate")
            bl, dbl, al, dl, tl = char.useUlt()
            teamBuffs, enemyDebuffs, advList, delayList = handleAdditions(playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList, bl, dbl, al, dl)
            turnList.extend(tl)

    # Handle any new attacks from unit ults  
    teamBuffs, enemyDebuffs, advList, delayList, spPlus, spMinus = processTurnList(turnList, playerTeam, eTeam, teamBuffs, enemyDebuffs, advList, delayList)
    spGain += spPlus
    spUsed += spMinus
    
    # Apply any speed adjustments
    spdAdjustment(playerTeam, teamBuffs)
    enemySPDAdjustment(eTeam, enemyDebuffs)
    
    # Reset the AV of the current unit by checking its current speed
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
        
    allUnits = sortUnits(allUnits)
    
logging.critical("\n==========COMBAT SIMULATION ENDED==========")

# Extra calculations
for char in playerTeam:
    if char.name == "Yunli":
        char.hitMultiplier = char.ults / totalEnemyAttacks

logging.critical("\n==========SIMULATION RESULTS==========")
debuffDMG = 0
charDMG = 0
dmgList = []
for enemy in eTeam:
    debuffDMG += enemy.debuffDMG
for char in playerTeam:
    res, dmg = char.gettotalDMG()
    dmgList.append(dmg)
    charDMG += dmg
totalDMG = debuffDMG + charDMG
dpavList = [i / avLimit for i in dmgList]
percentList = [i / totalDMG * 100 for i in dmgList]

logging.critical(f"TOTAL TEAM DMG: {totalDMG:.3f} | AV: {avLimit}")
logging.critical(f"TEAM DPAV: {totalDMG / avLimit:.3f}")
logging.critical(f"DEBUFF DMG: {debuffDMG:.3f} | CHAR DMG: {charDMG:.3f}")
logging.critical(f"SP GAINED: {spGain} | SP USED: {spUsed} | Enemy Attacks: {totalEnemyAttacks}")
res = ""
i = 0
for char in playerTeam:
    res += f"{char.name} DPAV: {dpavList[i]:.3f}, {percentList[i]:.3f}% | "
    i += 1
    
logging.critical(res)

for char in playerTeam:
    res, dmg = char.gettotalDMG()
    logging.critical(f"\n{char.name} > Total DMG: {dmg:.3f} | Basics: {char.basics} | Skills: {char.skills} | Ults: {char.ults} | FuAs: {char.fuas} | Leftover AV: {char.currAV if char.currAV < 500 else char.charge:.3f} | Excess Energy: {char.currEnergy:.3f}")
    logging.critical(res)

