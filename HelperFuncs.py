from Buff import *
from Turn import Turn
from Result import Result
from Enemy import Enemy
from Delay import *
import logging

logger = logging.getLogger(__name__)
wbMultiplier = 3767.5533
eleDct = {"PHY": 2.0, "FIR": 2.0, "WIN": 1.5, "ICE": 1.0, "LNG": 1.0, "QUA": 0.5, "IMG": 0.5}

def matchBuff(char, buff) -> bool:
    return True if (char.role == buff.target) else False

def parseBuffs(lst: list, playerTeam: list) -> list:
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
                debuffList.append(Debuff(d.name, d.debuffType, d.val, i, d.atkType, d.turns, d.stackLimit, d.isDot, d.isBlast))
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
            debuffList.append(Debuff(d.name, d.debuffType, d.val, enemy.enemyID, d.atkType, d.turns, d.stackLimit, d.isDot, d.isBlast))
            if enemy.hasAdj:
                for adjID in enemy.adjacent:
                    debuffList.append(Debuff(d.name, d.debuffType, d.val, adjID, d.atkType, d.turns, d.stackLimit, d.isDot, d.isBlast))
        else: # Just add debuff normally
            debuffList.append(d)
    return debuffList

def parseAdvance(lst: list[Advance], playerTeam: list) -> list[Advance]:
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

def parseTurns(lst: list[Turn], playerTeam: list) -> list[Turn]:
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

def addBuffs(currList: list, newList: list) -> list:
    def checkValidAdd(buff: Buff, currList: list) -> tuple[bool, int]:
        for i in range(len(currList)):
            checkAgainst = currList[i]
            if buff.name == checkAgainst.name:
                if buff.target == checkAgainst.target:
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

def findBuffs(charRole: str, buffType: str, buffList: list) -> list:
    return [x for x in buffList if (x.buffType == buffType and x.target == charRole)]

def sumBuffs(buffList: list[Buff]):
    return sum([x.getBuffVal() for x in buffList])

def getCharSPD(char, buffList: list[Buff]) -> float:
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

def initCharAV(char, buffList: list[Buff]):
    charSPD = getCharSPD(char, buffList)
    char.currAV = 10000 / charSPD
    char.currSPD = charSPD
    
def resetUnitAV(unit, buffList: list[Buff], debuffList: list[Debuff]):
    # check if unit is a char or enemy
    if unit.isChar(): # Character, check buffList for spd buffs
        initCharAV(unit, buffList)
    else: # Enemy, check debuffList for spd debuffs
        eSPD = getEnemySPD(unit, debuffList)
        unit.currAV = 10000 / eSPD
        unit.currSPD = eSPD
        
def spdAdjustment(teamList: list, buffList: list[Buff]):
    for char in teamList:
        newSPD = getCharSPD(char, buffList)
        if newSPD != char.currSPD:
            char.currAV = char.currAV * char.currSPD / newSPD
        char.currSPD = newSPD
    return

def enemySPDAdjustment(enemyTeam: list[Enemy], debuffList: list[Debuff]):
    for enemy in enemyTeam:
        newSPD = getEnemySPD(enemy, debuffList)
        if newSPD != enemy.currSPD:
            enemy.currAV = enemy.currAV * enemy.currSPD / newSPD
        enemy.currSPD = newSPD
    return

def avAdjustment(teamList: list, advList: list[Advance]):
    for adv in advList:
        logger.info(adv)
        char = findChar(teamList, adv.targetRole)
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

def addEnergy(playerTeam: list, numAttacks: int, attackTypeRatio: list[float], buffList: list[Buff]):
    dct = {"HUN": 3, "ERU": 3, "NIH": 4, "HAR": 4, "ABU": 4, "DES": 5, "PRE": 6}
    aggroLst = []
    for char in playerTeam:
        aggro = dct[char.path]
        if char.path == "DES":
            if char.lightcone.name == "Dance at Sunset":
                aggro += dct["DES"] * 5
            if checkInTeam("Lynx", playerTeam) and char.role == "DPS":
                aggro += dct["DES"] * 5
            if checkInTeam("March7th", playerTeam) and char.role == "DPS":
                aggro += dct["DES"] * 5
        elif char.path == "PRE":
            if char.name == "Gepard":
                aggro += dct["PRE"] * 3
            if char.lightcone.name == "Landau's Choice" or char.lightcone.name == "Moment of Victory":
                aggro += dct["PRE"] * 3
        elif char.path == "HUN":
            if char.name == "Dan Heng" or char.name == "Seele" or char.name == "Sushang":
                aggro -= dct["HUN"] * 0.5
            if char.name == "Yanqing":
                aggro -= dct["HUN"] * 0.6
        aggroLst.append(aggro)
    aggroSum = sum(aggroLst)
    chanceST = [a * numAttacks * 10 * attackTypeRatio[0] / aggroSum for a in aggroLst]
    chanceBlast = [aggroLst[i] + (aggroLst[i - 1] if i - 1 >= 0 else 0) + (aggroLst[i + 1] if i + 1 < len(aggroLst) else 0) for i in range(len(aggroLst))]
    chanceBlast = [a * numAttacks * 10 * attackTypeRatio[1] / aggroSum for a in chanceBlast]
    chanceAOE = [10 * numAttacks * attackTypeRatio[2] for _ in aggroLst]
    finalEnergy = [sum(values) for values in zip(chanceAOE, chanceBlast, chanceST)]
    for i in range(len(playerTeam)):
        char = playerTeam[i]
        errMul = getERR(char, buffList, ["ALL"])
        char.addEnergy(finalEnergy[i]* errMul) 
    return

def checkInTeam(name, team) -> bool:
    for char in team:
        if char.name == name:
            return True
    return False

def tickDebuffs(enemyID: int, debuffList: list) -> list:
    pass

def tickBuffs(charRole: str, buffList: list, tdType: str) -> list:
    pass

def findChar(playerTeam: list, charRole: str):
    for char in playerTeam:
        if char.role == charRole:
            return char
        
def handleAdditions(playerTeam: list, enemyTeam: list[Enemy], buffList: list[Buff], debuffList: list[Debuff], advList: list[Advance], delayList: list[Delay], 
                    buffToAdd: list[Buff], DebuffToAdd: list[Debuff], advToAdd: list[Advance], delayToAdd: list[Delay]) -> tuple[list[Buff], list[Debuff], list[Advance], list[Delay]]:
    buffs, debuffs, advs, delays = parseBuffs(buffToAdd, playerTeam), parseDebuffs(DebuffToAdd, enemyTeam), parseAdvance(advToAdd, playerTeam), parseDelay(delayToAdd, enemyTeam)
    buffList = addBuffs(buffList, buffs)
    debuffList = addBuffs(debuffList, debuffs)
    advList = addAdvance(advList, advs)
    delayList = addDelay(delayList, delays)
    
    return buffList, debuffList, advList, delayList

def handleTurn(turn: Turn, playerTeam: list, enemyTeam: list[Enemy], buffList: list[Buff], debuffList: list[Debuff]) -> tuple[Result, list[Debuff], list[Delay]]:
    char = findChar(playerTeam, turn.charRole)
    baseValue = getBaseValue(char, buffList, turn)
    charERR = getERR(char, buffList, turn.atkType)
    charDMG = getDmgMul(char, buffList, turn.atkType)
    charCR = getCritChance(char, buffList, turn.atkType)
    charCD = getCritMul(char, buffList, turn.atkType)
    charBE = getBE(char, buffList, turn.atkType)
    
    errGain = charERR * turn.errGain # actual energy gained from this move
    wbe = getWBE(char, buffList, turn.atkType)
    
    anyBroken = False
    turnDmg = 0
    wbDmg = 0
    newDebuff, newDelay = [], []
    
    def processEnemy(enemy: Enemy, breakUnits: float, dmgMul) -> tuple[list[Debuff], list[Delay]]:
        nonlocal turnDmg, wbDmg, anyBroken
        
        enemyBroken = False
        newDebuffs, newDelays = [], []
        if checkValidList(turn.element, enemy.weakness):
            enemyBroken = enemy.redToughness(breakUnits * wbe)
        penMul = getPenMul(char, enemy, buffList, turn.atkType, turn.element[0])
        enemyMul = getEnemyMul(enemy.enemyID, enemyTeam, debuffList, turn.atkType)
        turnDmg += expectedDMG(dmgMul * baseValue * charDMG * penMul * enemyMul, charCR, charCD)
        
        if enemyBroken:
            anyBroken = True
            for ele in turn.element:
                wbDmg += eleDct[ele] * wbMultiplier * enemy.maxToughnessMul * charBE * enemyMul
                newDelays.extend(wbDelay(ele, charBE, enemy))
                newDebuff.append(wbDebuff(ele, charBE, enemy))
        return newDebuffs, newDelays
    
    if turn.moveType == "AOE":
        # AOE Attack
        for enemy in enemyTeam:
            a, b = processEnemy(enemy, turn.brkSplit[0], turn.dmgSplit[0])
            newDebuff.extend(a)
            newDelay.extend(b)
    elif turn.moveType == "NA":
        pass # Do nothing (for now)
    else :
        if turn.targetID == -1:
            enemy = findBestEnemy(enemyTeam, debuffList, turn.atkType)
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
                
    return Result(turn.charName, turn.charRole, turn.atkType, turn.element, anyBroken, turnDmg, wbDmg, errGain), newDebuff, newDelay

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

def wbDebuff(ele: str, charBE: float, enemy: Enemy) -> Debuff:
    debuffName = f"{enemy.name} {ele}-break"
    if ele == "PHY":
        return Debuff(debuffName, "BLEED", 2 * wbMultiplier * enemy.maxToughnessMul * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "FIR":
        return Debuff(debuffName, "BURN", 1 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "ICE":
        return Debuff(debuffName, "FREEZE", 1 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 1, 1, False, False)
    elif ele == "WIN":
        return Debuff(debuffName, "WINDSHEAR", 3 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "LNG":
        return Debuff(debuffName, "SHOCK", 2 * wbMultiplier * charBE, enemy.enemyID, ["ALL"], 2, 1, True, False)
    elif ele == "QUA":
        return Debuff(debuffName, "ENTANGLE", 1.8 * wbMultiplier * enemy.maxToughnessMul * charBE, enemy.enemyID, ["ALL"], 1, 1, False, False)
    elif ele == "IMG":
        return Debuff(debuffName, "SPD%", -0.1, enemy.enemyID, ["ALL"], 1, 1, False, False)
    
def findBestEnemy(enemyTeam: list[Enemy], debuffList: list[Debuff], atkType: list[str]) -> Enemy:
    bestEnemy = None
    bestMul = 0
    for enemy in enemyTeam:
        currMul = getEnemyMul(enemy.enemyID, enemyTeam, debuffList, atkType)
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

def getShredMul(enemy: Enemy, debuffList: list[Debuff], atkType: list[str]) -> float:
    defShred = 0
    for debuff in debuffList:
        if debuff.target != enemy.enemyID:
            continue
        if debuff.debuffType != "SHRED":
            continue
        if not checkValidList(atkType, debuff.atkType):
            continue
        defShred += debuff.getDebuffVal()
    return min(1.0, 100 / ((enemy.level + 20) * (1 - defShred) + 100))

def getVulnMul(enemy: Enemy, debuffList: list[Debuff], atkType: list[str]) -> float:
    vuln = 0
    for debuff in debuffList:
        if debuff.target != enemy.enemyID:
            continue
        if debuff.debuffType != "VULN":
            continue
        if not checkValidList(atkType, debuff.atkType):
            continue
        vuln += debuff.getDebuffVal()
    return min(3.5, 1 + vuln)

def getUniMul(enemy: Enemy, debuffList: list[Debuff], atkType: list[str]) -> float:
    return enemy.getUniMul()

def getEnemyMul(enemyID: int, enemyTeam: list, debuffList: list[Debuff], atkType: list[str]) -> float:
    # Returns total multiplier for Vuln, Shred, and Uni Res for the specified enemy
    enemy = enemyTeam[enemyID]
    return getShredMul(enemy, debuffList, atkType) * getVulnMul(enemy, debuffList, atkType) * getUniMul(enemy, debuffList, atkType)

def getBaseValue(char, buffList: list[Buff], turn: Turn): 
    if turn.scaling == "ATK" or turn.scaling == "DEF" or turn.scaling == "HP": # normal scaling attacks
        return getScalingValues(char, buffList, turn.atkType)
    # reserved for weird stuff like firefly
    else:
        return 
    
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

def getDmgMul(char, buffList: list[Buff], atkType: list[str]) -> float:
    dmg = 1 + char.relicStats.getDMG()
    for buff in buffList:
        if buff.target != char.role:
             continue
        if not checkValidList(atkType, buff.atkType):
             continue
        if buff.buffType == "DMG%":
            dmg += buff.getBuffVal()
    return dmg

def getPenMul(char, enemy: Enemy, buffList: list[Buff], atkType: list[str], element: str) -> float:
    enemyRes = enemy.getRes(element)
    resPen = 0
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "PEN":
            resPen += buff.getBuffVal()
    return min(2.0, (1 - (enemyRes - resPen)))

def getCritMul(char, buffList: list[Buff], atkType: list[str]) -> float:
    cd = 1 + char.relicStats.getCD()
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "CD%":
            cd += buff.getBuffVal()
    return cd

def getCritChance(char, buffList: list[Buff], atkType: list[str]) -> float:
    cr = char.relicStats.getCR()
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "CR%":
            cr += buff.getBuffVal()
    return min(1.0, cr)

def getBE(char, buffList: list[Buff], atkType: list[str]) -> float:
    be = char.relicStats.getBE()
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "BE%":
            be += buff.getBuffVal()
    return 1 + be

def getEHR(char, buffList: list[Buff], atkType: list[str]) -> float:
    ehr = char.relicStats.getEHR()
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "EHR%":
            ehr += buff.getBuffVal()
    return ehr

def getERS(char, buffList: list[Buff], atkType: list[str]) -> float:
    ers = char.relicStats.getERS()
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "ERS%":
            ers += buff.getBuffVal()
    return ers

def getERR(char, buffList: list[Buff], atkType: list[str]) -> float:
    err = char.relicStats.getERR()
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "ERR%":
            err += buff.getBuffVal()
    return err

def getWBE(char, buffList: list[Buff], atkType: list[str]) -> float:
    wbe = 1
    for buff in buffList:
        if buff.target != char.role:
            continue
        if not checkValidList(atkType, buff.atkType):
            continue
        if buff.buffType == "WBE%":
            wbe += buff.getBuffVal()
    return wbe