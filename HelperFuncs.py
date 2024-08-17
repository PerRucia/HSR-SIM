from Buff import *
from Turn import Turn
from Result import *
from Enemy import Enemy
from Delay import *
from Character import *
import logging
from Misc import *

logger = logging.getLogger(__name__)

def parseBuffs(lst: list[Buff], playerTeam: list[Character]) -> list:
    buffList = []
    for buff in lst:
        if buff.target == "ALL": #teamwide buff, need to add 4 instances
            for char in playerTeam:
                target = char.role if (buff.tickDown == "SELF") else buff.tickDown
                buffList.append(Buff(buff.name, buff.buffType, buff.val, char.role, buff.atkType, buff.turns, buff.stackLimit, target, buff.tdType))
        else: #single target buff, only add one instance
            target = buff.target if (buff.tickDown == "SELF") else buff.tickDown
            buffList.append(Buff(buff.name, buff.buffType, buff.val, buff.target, buff.atkType, buff.turns, buff.stackLimit, target, buff.tdType))
    return buffList

def parseDebuffs(lst: list[Debuff], enemyTeam: list[Enemy]) -> list[Debuff]:
    debuffList = []
    for d in lst:
        if d.target == "ALL": # AoE debuff, need to add 1 instace per enemy
            for i in range(len(enemyTeam)):
                debuffList.append(Debuff(d.name, d.charRole, d.debuffType, d.val, i, d.atkType, d.turns, d.stackLimit, d.isDot, d.isBlast))
        elif d.isBlast: # Blast-type debuff, need to add to up to three enemies
            if d.target == -1:
                if len(enemyTeam) == 3 or len(enemyTeam) == 4:
                    enemy = enemyTeam[1]
                elif len(enemyTeam) == 5:
                    enemy = enemyTeam[2]
                else:
                    enemy = enemyTeam[0]
            else:
                enemy = enemyTeam[d.target]
            debuffList.append(Debuff(d.name, d.charRole, d.debuffType, d.val, enemy.enemyID, d.atkType, d.turns, d.stackLimit, d.isDot, d.isBlast))
            if enemy.hasAdj:
                for adjID in enemy.adjacent:
                    debuffList.append(Debuff(d.name, d.charRole, d.debuffType, d.val, adjID, d.atkType, d.turns, d.stackLimit, d.isDot, d.isBlast))
        else: # Just add debuff normally
            debuffList.append(d)
    return debuffList

def parseAdvance(lst: list[Advance], playerTeam: list[Character]) -> list[Advance]:
    advList = []
    for adv in lst:
        if adv.targetRole == "ALL": # Teamwide advance
            for char in playerTeam:
                advList.append(Advance(adv.name, char.role, adv.advPercent))
        else: # Single advance
            advList.append(adv)
    return advList

def parseDelay(lst: list[Delay], enemyTeam: list[Enemy]) -> list[Delay]:
    delayList = []
    for delay in lst:
        if delay.target == "ALL":
            for enemy in enemyTeam:
                delayList.append(Delay(delay.name, delay.delayPercent, enemy.enemyID, delay.reqBroken, delay.stackable))
        else:
            delayList.append(delay)
    return delayList

def parseTurns(lst: list[Turn], playerTeam: list[Character]) -> list[Turn]:
    turnList = []
    for turn in lst:
        if turn.charRole == "ALL":
            for char in playerTeam:
                turnList.append(Turn(turn.charName, char.role, turn.targetID, turn.moveType, turn.atkType, turn.element, turn.dmgSplit, turn.brkSplit, turn.errGain, turn.scaling, turn.spChange, turn.moveName))
        elif turn.charRole == "TEAM":
            for char in playerTeam:
                if char.name == turn.charName:
                    continue
                turnList.append(Turn(turn.charName, char.role, turn.targetID, turn.moveType, turn.atkType, turn.element, turn.dmgSplit, turn.brkSplit, turn.errGain, turn.scaling, turn.spChange, turn.moveName))
        else:
            turnList.append(turn)
    return turnList
def addDelay(currList: list[Delay], newList: list[Delay]) -> list[Delay]:
    def checkValidAdd(delay: Delay, currList: list[Delay]) -> bool:
        return all(delay.name != existingDelay.name or delay.stackable for existingDelay in currList)

    for delay in newList:
        if checkValidAdd(delay, currList):
            currList.append(delay)
    
    return currList

def addAdvance(currList: list[Advance], newList: list[Advance]) -> list[Advance]:
    currList.extend(newList)
    return currList

def addBuffs(currList: list[Buff], newList: list[Buff]) -> tuple[bool, int, float]:
    def checkValidAdd(buff: Buff, currList: list[Buff]) -> tuple[bool, int]:
        for i in range(len(currList)):
            checkAgainst = currList[i]
            if buff.name == checkAgainst.name:
                if buff.target == checkAgainst.target:
                    checkAgainst.val = buff.val
                    return False, i
        return True, -1
    
    # Only add a new entry if unique name or repeated name but different target
    for buff in newList:
        check, buffID = checkValidAdd(buff, currList)
        if check:
            currList.append(buff)
        else:
            if not currList[buffID].atMaxStacks():
                currList[buffID].incStack()
            currList[buffID].refreshTurns()
    return currList

def findBuffs(charRole: str, buffType: str, buffList: list[Buff]) -> list:
    return [x for x in buffList if (x.buffType == buffType and x.target == charRole)]

def sumBuffs(buffList: list[Buff]):
    return sum([x.getBuffVal() for x in buffList])

def getCharSPD(char: Character, buffList: list[Buff]) -> float:
    baseSPD = char.baseSPD
    spdPercent = sumBuffs(findBuffs(char.role, "SPD%", buffList))
    spdFlat = sumBuffs(findBuffs(char.role, "SPD", buffList)) + char.getSPD()
    return baseSPD * (1 + spdPercent) + spdFlat

def getEnemySPD(enemy: Enemy, debuffList: list[Debuff]) -> float:
    baseSPD = enemy.spd
    debuffSum = 0
    for debuff in debuffList:
        if (debuff.debuffType == "SPD%") and (debuff.target == enemy.enemyID):
            debuffSum += debuff.getDebuffVal()
    return baseSPD * (1 - debuffSum)

def initCharAV(char: Character, buffList: list[Buff]):
    charSPD = getCharSPD(char, buffList)
    char.reduceAV(char.currAV - (10000 / charSPD))
    char.currSPD = charSPD
    
def resetUnitAV(unit, buffList: list[Buff], debuffList: list[Debuff]):
    # check if unit is a char or enemy
    if unit.isChar(): # Character, check buffList for spd buffs
        initCharAV(unit, buffList)
    else: # Enemy, check debuffList for spd debuffs
        eSPD = getEnemySPD(unit, debuffList)
        unit.currAV = 10000 / eSPD
        unit.currSPD = eSPD
        
def spdAdjustment(teamList: list[Character], buffList: list[Buff]):
    for char in teamList:
        newSPD = getCharSPD(char, buffList)
        if newSPD != char.currSPD:
            char.reduceAV(char.currAV - (char.currAV * char.currSPD / newSPD))
    return

def enemySPDAdjustment(enemyTeam: list[Enemy], debuffList: list[Debuff]):
    for enemy in enemyTeam:
        newSPD = getEnemySPD(enemy, debuffList)
        if newSPD != enemy.currSPD:
            enemy.currAV = enemy.currAV * enemy.currSPD / newSPD
        enemy.currSPD = newSPD
    return

def avAdjustment(teamList: list[Character], advList: list[Advance]):
    for adv in advList:
        logger.info(adv)
        char = findCharRole(teamList, adv.targetRole)
        avRed = (10000 / char.currSPD)  * adv.advPercent
        char.reduceAV(avRed)
        char.priority = char.priority + 10
    return
                
def sortUnits(allUnits: list) -> list:
    return sorted(allUnits, key=lambda x: (x.currAV, -x.priority))

def setPriority(allUnits: list):
    for i in range(len(allUnits)):
        allUnits[i].priority = len(allUnits) - i
        
def delayAdjustment(enemyTeam: list[Enemy], delayList: list[Delay], debuffList: list[Debuff]) -> list[Delay]:
    def findEnemy(enemyID: int) -> Enemy:
        return next((enemy for enemy in enemyTeam if enemy.enemyID == enemyID), None)
    
    res = []
    for delay in delayList:
        logger.info(delay)
        enemy = findEnemy(delay.target)
        enemyAV = 10000 / getEnemySPD(enemy, debuffList)
        if not delay.reqBroken or (delay.reqBroken and enemy.broken):
            enemy.reduceAV(enemyAV * delay.delayPercent * -1)
        else:
            res.append(delay) # keep the delay in delayList until it can be applied
    return res

def addEnergy(playerTeam: list[Character], enemyTeam: list[Enemy], numAttacks: int, attackTypeRatio: list[float], buffList: list[Buff]):
    aggroLst = []
    for char in playerTeam:
        aggro = aggroDct[char.path]
        if char.path == "DES":
            if char.lightcone.name == "Dance at Sunset":
                aggro += aggroDct["DES"] * 5
            if checkInTeam("Lynx", playerTeam) and char.role == "DPS":
                aggro += aggroDct["DES"] * 5
            if checkInTeam("March7th", playerTeam) and char.role == "DPS":
                aggro += aggroDct["DES"] * 5
        elif char.path == "PRE":
            if char.name == "Gepard":
                aggro += aggroDct["PRE"] * 3
            if char.lightcone.name == "Landau's Choice" or char.lightcone.name == "Moment of Victory":
                aggro += aggroDct["PRE"] * 3
        elif char.path == "HUN":
            if char.name == "Dan Heng" or char.name == "Seele" or char.name == "Sushang":
                aggro -= aggroDct["HUN"] * 0.5
            if char.name == "Yanqing":
                aggro -= aggroDct["HUN"] * 0.6
        aggroLst.append(aggro)
    aggroSum = sum(aggroLst)
    chanceST = [a * numAttacks * 10 * attackTypeRatio[0] / aggroSum for a in aggroLst]
    chanceBlast = [aggroLst[i] + (aggroLst[i - 1] if i - 1 >= 0 else 0) + (aggroLst[i + 1] if i + 1 < len(aggroLst) else 0) for i in range(len(aggroLst))]
    chanceBlast = [a * numAttacks * 10 * attackTypeRatio[1] / aggroSum for a in chanceBlast]
    chanceAOE = [10 * numAttacks * attackTypeRatio[2] for _ in aggroLst]
    finalEnergy = [sum(values) for values in zip(chanceAOE, chanceBlast, chanceST)]
    for i in range(len(playerTeam)):
        char = playerTeam[i]
        placeHolderTurn = Turn(char.name, char.role, -1, "NA", ["ALL"], [char.element], [0, 0], [0, 0], 0, char.scaling, 0, "HitEnergyPlaceholder")
        errMul = getMulERR(char, enemyTeam[0], buffList, [], placeHolderTurn) if not char.specialEnergy else 0
        char.addEnergy(finalEnergy[i]* errMul) 
    return [i / (numAttacks * 10) for i in finalEnergy]

def checkInTeam(name: str, team: list[Character]) -> bool:
    for char in team:
        if char.name == name:
            return True
    return False

def tickDebuffs(enemy: Enemy, debuffList: list[Debuff]) -> list[Debuff]:
    newList = []
    for debuff in debuffList:
        if debuff.target == enemy.enemyID:
            if debuff.turns > 1:
                debuff.reduceTurns()
                newList.append(debuff)
            else:
                logging.info(f"{debuff.name} expired")
        else:
            newList.append(debuff)
    return newList

def tickBuffs(charRole: str, buffList: list[Buff], tdType: str) -> list[Buff]:
    newList = []
    for buff in buffList:
        if buff.tdType == tdType: # must match tdType to tickdown
            if buff.tickDown == charRole: # must match charRole to tickdown
                if buff.turns <= 1:
                    logging.info(f"{buff.name} expired")
                    continue
                buff.reduceTurns()
        newList.append(buff)
    return newList

def takeDot(enemy: Enemy, playerTeam: list[Character], buffList: list[Buff], debuffList: list[Debuff]):
    dmg = 0
    dotList = [debuff for debuff in debuffList if (debuff.isDot and debuff.target == enemy.enemyID)]

    for dot in dotList:
        char = findCharRole(playerTeam, dot.charRole)
        placeholderTurn = Turn(char.name, char.role, enemy.enemyID, "NA", ["DOT"], [char.element], [0, 0], [0, 0], 0, char.scaling, 0, "DOTPlaceholder")
        dmg += dot.getDebuffVal() * getMulENEMY(char, enemy, buffList, debuffList, placeholderTurn)
        logging.warning(f"{enemy.name} took {dmg:.3f} DOT-dmg from {dot.name}")
    enemy.dotDMG = enemy.dotDMG + dmg

def findCharRole(playerTeam: list[Character], charRole: str) -> Character:
    for char in playerTeam:
        if char.role == charRole:
            return char
        
def findCharName(playerTeam: list[Character], charName: str) -> Character:
    for char in playerTeam:
        if char.name == charName:
            return char
        
def handleAdditions(playerTeam: list, enemyTeam: list[Enemy], buffList: list[Buff], debuffList: list[Debuff], advList: list[Advance], delayList: list[Delay], 
                    buffToAdd: list[Buff], DebuffToAdd: list[Debuff], advToAdd: list[Advance], delayToAdd: list[Delay]) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay]]:
    buffs, debuffs, advs, delays = parseBuffs(buffToAdd, playerTeam), parseDebuffs(DebuffToAdd, enemyTeam), parseAdvance(advToAdd, playerTeam), parseDelay(delayToAdd, enemyTeam)
    buffList = addBuffs(buffList, buffs)
    debuffList = addBuffs(debuffList, debuffs)
    advList = addAdvance(advList, advs)
    delayList = addDelay(delayList, delays)
    
    return buffList, debuffList, advList, delayList

def handleTurn(turn: Turn, playerTeam: list[Character], enemyTeam: list[Enemy], buffList: list[Buff], debuffList: list[Debuff]) -> tuple[Result, list[Debuff], list[Delay]]:
    char = findCharRole(playerTeam, turn.charRole)
    charERR = getMulERR(char, enemyTeam[0], buffList, debuffList, turn)
    baseValue = getBaseValue(char, buffList, turn)
    
    anyBroken = False
    turnDmg = 0
    wbDmg = 0
    newDebuff, newDelay = [], []
    
    def processEnemy(enemy: Enemy, breakUnits: float, percentMultiplier: float, charCR=0, charCD=0) -> tuple[list[Debuff], list[Delay]]:
        nonlocal turnDmg, wbDmg, anyBroken
        
        charBE = getMulBE(char, enemy, buffList, debuffList, turn)
        charWBE = getMulWBE(char, enemy, buffList, debuffList, turn)
        charDMG = getMulDMG(char, enemy, buffList, debuffList, turn)
        if charCR == 0:
            charCR = getMulCR(char, enemy, buffList, debuffList, turn)
        if charCD == 0:
            charCD = getMulCD(char, enemy, buffList, debuffList, turn)
        enemyMul = getMulENEMY(char, enemy, buffList, debuffList, turn)
        
        enemyBroken = False
        newDebuffs, newDelays = [], []
        if checkValidList(turn.element, enemy.weakness):
            enemyBroken = enemy.redToughness(breakUnits * charWBE)
        turnDmg += expectedDMG(baseValue * charDMG * percentMultiplier * enemyMul, charCR, charCD)
        
        if enemyBroken:
            anyBroken = True
            for ele in turn.element:
                wbDmg += eleDct[ele] * wbMultiplier * enemy.maxToughnessMul * charBE * enemyMul
                newDelays.extend(wbDelay(ele, charBE, enemy))
                newDebuff.append(wbDebuff(ele, char.role, charBE, enemy))
        return newDebuffs, newDelays
    
    if turn.moveType == "AOE":
        # AOE Attack
        for enemy in enemyTeam:
            a, b = processEnemy(enemy, turn.brkSplit[0], turn.dmgSplit[0])
            newDebuff.extend(a)
            newDelay.extend(b)
    elif turn.moveType == "NA":
        if turn.moveName == "RobinConcertoDMG":
            char = findCharName(playerTeam, "Robin")
            enemy = findBestEnemy(char, enemyTeam, buffList, debuffList, turn)
            _, _ = processEnemy(enemy, turn.brkSplit[0], turn.dmgSplit[0], 1.0, 2.5)
    else :
        if turn.targetID == -1:
            enemy = findBestEnemy(char, enemyTeam, buffList, debuffList, turn)
        else:
            enemy = enemyTeam[turn.targetID]  
        a, b = processEnemy(enemy, turn.brkSplit[0], turn.dmgSplit[0])
        newDebuff.extend(a)
        newDelay.extend(b)
        if enemy.hasAdj and (turn.brkSplit[1] > 0 or (turn.dmgSplit[1] > 0)):
            for enemyID in enemy.adjacent:
                adj_enemy = enemyTeam[enemyID]
                a, b = processEnemy(adj_enemy, turn.brkSplit[1], turn.dmgSplit[1])
                newDebuff.extend(a)
                newDelay.extend(b)
                
    return Result(turn.charName, turn.charRole, turn.atkType, turn.element, anyBroken, turnDmg, wbDmg, turn.errGain * charERR, turn.moveName), newDebuff, newDelay

def handleEnergyFromBuffs(buffList: list[Buff], debuffList: list[Debuff], playerTeam: list[Character], enemyTeam: list[Enemy]) -> list[Buff]:
    errBuffs, newList = [], []
    for buff in buffList:
        if buff.buffType == "ERR_T" or buff.buffType == "ERR_F":
            errBuffs.append(buff)
        else:
            newList.append(buff)
    for eb in errBuffs:
        char = findCharRole(playerTeam, eb.target)
        placeholderTurn = Turn(char.name, char.role, 0, "NA", ["ALL"], ["ALL"], [0, 0], [0, 0], 0, char.scaling, 0, "PlaceHolderTurn: ERR")
        charERR = getMulERR(char, enemyTeam[0], buffList, debuffList, placeholderTurn)
        if not char.specialEnergy:
            if eb.buffType == "ERR_T":
                char.addEnergy(eb.getBuffVal() * charERR)
            elif eb.buffType == "ERR_F":
                char.addEnergy(eb.getBuffVal())
    return newList

def handleSpec(specStr: str, playerTeam: list[Character], enemyTeam: list[Enemy], buffList: list[Buff], debuffList: list[Debuff]) -> Special:
    if specStr == "":
        return Special()
    elif specStr == "updateRobinATK":
        for p in playerTeam:
            if p.name == "Robin":
                role = p.role
                break
        char = findCharRole(playerTeam, role)
        res = getBaseValue(char, buffList, Turn(char.name, char.role, -1, "NA", ["ULT"], [char.element], [0, 0], [0, 0], 0, char.scaling, 0, "updateRobinATK"))
        return Special(attr1=res)
    elif specStr == "HuoHuoUlt":
        lst = []
        for char in playerTeam:
            if char.name != "HuoHuo":
                charMaxEnergy = 0 if char.specialEnergy else char.maxEnergy
                lst.append([charMaxEnergy * 0.2, char.role])
        return Special(attr1=lst[0], attr2=lst[1], attr3=lst[2])
    elif specStr == "getYunliAggro":
        yunliSlot = findCharName(playerTeam, "Yunli").pos
        lst = addEnergy(playerTeam, enemyTeam, 1, [0.55, 0.2, 0.25], buffList)
        return Special(attr1=lst[yunliSlot])
    elif specStr == "FeixiaoStartFUA":
        return Special()
    
def wbDelay(ele: str, charBE: float, enemy: Enemy) -> list[Delay]:
    res = [Delay("STDBreakDelay", 0.25, enemy.enemyID, True, False)]
    breakName = f"{ele}-break"
    if ele in ["WIN", "PHY", "FIR", "LNG"]: # standard break delay
        pass # no additional effects (for now)
    elif ele == "ICE":
        res.append(Delay(breakName, 0.50, enemy.enemyID, True, False))
    elif ele == "QUA":
        res.append(Delay(breakName, 0.2 * charBE, enemy.enemyID, True, False))
    elif ele == "IMG":
        res.append(Delay(breakName, 0.3 * charBE, enemy.enemyID, True, False))
    return res

def wbDebuff(ele: str, charRole: str, charBE: float, enemy: Enemy) -> Debuff:
    debuffName = f"{enemy.name} {ele}-break"
    if ele == "PHY":
        return Debuff(debuffName, charRole, "BLEED", 2 * wbMultiplier * enemy.maxToughnessMul * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "FIR":
        return Debuff(debuffName, charRole, "BURN", 1 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "ICE":
        return Debuff(debuffName, charRole, "FREEZE", 1 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 1, 1, False, False)
    elif ele == "WIN":
        return Debuff(debuffName, charRole, "WINDSHEAR", 3 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "LNG":
        return Debuff(debuffName, charRole, "SHOCK", 2 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "QUA":
        return Debuff(debuffName, charRole, "ENTANGLE", 1.8 * wbMultiplier * enemy.maxToughnessMul * charBE, enemy.enemyID, ["ALL"], 1, 1, False, False)
    elif ele == "IMG":
        return Debuff(debuffName, charRole, "SPD%", -0.1, enemy.enemyID, ["ALL"], 1, 1, False, False)
    
def findBestEnemy(char: Character, enemyTeam: list[Enemy], buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> Enemy:
    bestEnemy = None
    bestMul = 0
    for enemy in enemyTeam:
        currMul = getMulENEMY(char, enemy, buffList, debuffList, turn)
        if currMul > bestMul:
            bestMul = currMul
            bestEnemy = enemy
    return bestEnemy

def expectedDMG(baseDMG: float, cr: float, cd: float) -> float:
    return (baseDMG * (1 - cr)) + (baseDMG * cr * cd)

# Functions to get various multipliers
def checkValidList(list1: list, list2: list) -> bool:
    if ("ALL" in list2) or ("ALL" in list1):
        return True
    set2 = set(list2)
    return any(l1 in set2 for l1 in list1)

def getBaseValue(char, buffList: list[Buff], turn: Turn) -> float: 
    if turn.scaling == "ATK" or turn.scaling == "DEF" or turn.scaling == "HP": # normal scaling attacks
        return getScalingValues(char, buffList, turn.atkType)
    else:
        return 0
    
def getScalingValues(char, buffList: list[Buff], atkType: list[str]) -> float:
    base, mul, flat = char.getBaseStat()
    mulChecker = f"{char.scaling}%"
    flatChecker = char.scaling
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == mulChecker:
            mul += buff.getBuffVal()
        elif buff.buffType == flatChecker:
            flat += buff.getBuffVal()
    return base * (1 + mul) + flat

# Use this function to get the stat of the character, without any associated base multipliers:
# e.g. 1 + dmg%, 1 + err% etc.
def getCharStat(query: str, char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    res = 0
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(turn.atkType, buff.atkType):
            continue
        if buff.buffType == query:
            res += buff.getBuffVal()
    
    for debuff in debuffList:
        if debuff.target != enemy.enemyID:
            continue
        if not checkValidList(turn.atkType, debuff.atkType):
            continue
        if debuff.debuffType == query:
            res += debuff.getDebuffVal()
            
    match query:
        case "BE%":
            return res + char.relicStats.getBE() # base multiplier of 1 not added
        case "WBE%":
            return res # base multiplier of 1 not added
        case "EHR%":
            return res + char.relicStats.getEHR()
        case "ERS%":
            return res + char.relicStats.getERS()
        case "CR%":
            return res + char.relicStats.getCR() # base value of 0.05 added
        case "CD%":
            return res + char.relicStats.getCD() # base value of 0.5 added, base multi of 1 not added
        case "DMG%":
            return res + char.relicStats.getDMG() # base value of 1 not added
        case "ERR%":
            return res + char.relicStats.getERR() # base value of 1 not added
        case "OGH%":
            return res + char.relicStats.getOGH() # base multiplier of 1 not added
        case "SHRED":
            return res
        case "PEN":
            return res
        case "VULN":
            return res

# Use these functions to directly get the multiplier against the specified enemy for the specified char
def getMulBE(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("BE%", char, enemy, buffList, debuffList, turn) + 1

def getMulWBE(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("WBE%", char, enemy, buffList, debuffList, turn) + 1

def getMulEHR(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("EHR%", char, enemy, buffList, debuffList, turn)

def getMulERS(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("ERS%", char, enemy, buffList, debuffList, turn)

def getMulCR(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("CR%", char, enemy, buffList, debuffList, turn)

def getMulCD(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("CD%", char, enemy, buffList, debuffList, turn) + 1

def getMulDMG(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("DMG%", char, enemy, buffList, debuffList, turn) + 1

def getMulERR(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("ERR%", char, enemy, buffList, debuffList, turn) + 1

def getMulOGH(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    return getCharStat("OGH%", char, enemy, buffList, debuffList, turn) + 1

def getMulSHRED(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    shred = getCharStat("SHRED", char, enemy, buffList, debuffList, turn)
    return min(1.0, 100 / ((enemy.level + 20) * (1 - shred) + 100))

def getMulVULN(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    vuln = getCharStat("VULN", char, enemy, buffList, debuffList, turn) 
    return min(3.5, 1 + vuln)

def getMulPEN(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    pen = getCharStat("PEN", char, enemy, buffList, debuffList, turn)
    pen = pen - enemy.getRes(turn.element[0])
    return min(3.0, 1 - pen)

def getMulUNI(enemy: Enemy) -> float:
    return enemy.getUniMul()

def getMulENEMY(char: Character, enemy: Enemy, buffList: list[Buff], debuffList: list[Debuff], turn: Turn) -> float:
    shredMul = getMulSHRED(char, enemy, buffList, debuffList, turn)
    vulnMul = getMulVULN(char, enemy, buffList, debuffList, turn)
    penMul = getMulPEN(char, enemy, buffList, debuffList, turn)
    uniMul = getMulUNI(enemy)
    return shredMul * vulnMul * penMul * uniMul