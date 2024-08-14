from Buff import *
from Turn import Turn
from Result import Result
from Enemy import Enemy
from Delay import Delay

wbMultiplier = 3767.5533

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

def parseDebuffs(lst: list[Debuff], enemyTeam: list[Enemy]) -> list:
    debuffList = []
    for d in lst:
        if d.target == "ALL": # AoE debuff, need to add 1 instace per enemy
            for i in range(len(enemyTeam)):
                debuffList.append(Debuff(d.name, d.debuffType, d.val, i, d.atkType, d.turns, d.stackLimit))
        else: # Just add debuff normally
            debuffList.append(debuffList)
    return debuffList

def parseAdvance(lst: list, playerTeam: list) -> list:
    advList = []
    for a in lst:
        if a[0] == "ALL": # Teamwide advance
            for char in playerTeam:
                advList.append([char.role, a[1]])
        else: # Single advance
            advList.append(a)
    return advList

def parseDelay(lst: list[Delay], enemyTeam: list[Enemy]):
    delayList = []
    for delay in lst:
        if delay.target == "ALL":
            for enemy in enemyTeam:
                delayList.append(Delay(delay.name, delay.delayPercent, enemy.enemyID, delay.reqBroken, delay.stackable))
        else:
            delayList.append(delay)
    return delayList

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

def initCharAV(char, buffList: list[Buff]):
    charSPD = getCharSPD(char, buffList)
    char.currAV = 10000 / charSPD
    char.currSPD = charSPD
    
def spdAdjustment(teamList: list, buffList: list[Buff]):
    for char in teamList:
        newSPD = getCharSPD(char, buffList)
        if newSPD != char.currSPD:
            char.currAV = char.currAV * char.currSPD / newSPD
        char.currSPD = newSPD
    return

def avAdjustment(teamList: list, avList: list[list]):
    for av in avList:
        role = av[0]
        advPercent = av[1]
        for char in teamList:
            if char.role == role:
                avRed = (10000 / char.currSPD)  * advPercent
                char.reduceAV(avRed)
                char.priority = char.priority + 10
    return
                
def sortUnits(allUnits: list) -> list:
    return sorted(allUnits, key=lambda x: (x.currAV, -x.priority))

def setPriority(allUnits: list) -> list:
    for i in range(len(allUnits)):
        allUnits[i].priority = len(allUnits) - i
        
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
    newLst = []
    for debuff in debuffList:
        if debuff.enemyID != enemyID:
            newLst.append(debuff)
        else:
            if debuff.turns == 1:
                continue
            debuff.reduceTurns()
            newLst.append(debuff)
    return newLst

def tickBuffs(charRole: str, buffList: list) -> list:
    newLst = []
    for buff in buffList:
        if buff.target != charRole:
            newLst.append(buff)
        else:
            if buff.turns == 1:
                continue
            buff.reduceTurns()
            newLst.append(buff)
    return newLst

def findChar(playerTeam: list, charRole: str):
    for char in playerTeam:
        if char.role == charRole:
            return char
        
def handleTurn(turn: Turn, enemyTeam: list[Enemy], playerTeam: list, buffList: list[Buff], debuffList: list[Debuff]) -> Result:
    char = findChar(playerTeam, turn.charRole)
    scalingVal = getScalingValues(char, buffList, turn.atkType)
    dmgMul = getDmgMul(char, buffList, turn.atkType)
    wbe = getWBE(char, buffList, turn.atkType)
    cd = getCritMul(char, buffList, turn.atkType)
    cr = getCritChance(char, buffList, turn.atkType)
    err = getERR(char, buffList, turn.atkType)
    char.addEnergy(turn.errGain * err)
    be = 1 + getBE(char, buffList, turn.atkType)
    
    dmgDealt = 0
    wbDmgDealt = 0
    anyBroken = False
    
    def processEnemy(enemy: Enemy, brk: float, dmg: float):
        nonlocal dmgDealt, wbDmgDealt, anyBroken
        
        enemyBroken = enemy.redToughness(brk * wbe)
        penMul = getPenMul(char, enemy, buffList, turn.atkType, turn.element[0])
        enemyMul = getEnemyMul(enemy.enemyID, enemyTeam, debuffList, turn.atkType)
        dmgDealt += expectedDMG(dmg * scalingVal * dmgMul * penMul * enemyMul, cr, cd)
        
        if enemyBroken:
            anyBroken = True
            wbDmgDealt += getWBDmg(turn.element[0], wbMultiplier, enemy.maxToughnessMul) * be * penMul * enemyMul
            
    if turn.moveType == "AOE": # AOE attack, don't need to select enemy
        for enemy in enemyTeam:
            processEnemy(enemy, turn.brkSplit[0], turn.dmgSplit[0])
    else: # ST and Blast attacks
        if turn.targetID == -1: # automatically determine best enemy to attack
            enemy, _ = findBestEnemy(enemyTeam, debuffList, turn.atkType)
        else:
            enemy = enemyTeam[turn.targetID]
        
        # Main Targets
        processEnemy(enemy, turn.brkSplit[0], turn.dmgSplit[0])    
            
        # Adjacent Targets
        if enemy.hasAdj and turn.dmgSplit[1] > 0:
            for enemyID in enemy.adjacent:
                adj_enemy = enemyTeam[enemyID]
                processEnemy(adj_enemy, turn.brkSplit[1], turn.dmgSplit[1])
                
    return Result(turn.charName, turn.charRole, turn.atkType, turn.element, anyBroken, dmgDealt, wbDmgDealt)

def getWBDmg(element: str, wbMultiplier: float, maxToughnessMul: float) -> float:
    match element:
        case "PHY":
            breakMul = 2 * wbMultiplier * maxToughnessMul
            debuffMul = 4 * wbMultiplier * maxToughnessMul
        case "FIR":
            breakMul = 2 * wbMultiplier * maxToughnessMul
            debuffMul = 2 * wbMultiplier
        case "WIN":
            breakMul = 1.5 * wbMultiplier * maxToughnessMul
            debuffMul = 6 * wbMultiplier
        case "ICE":
            breakMul = 1 * wbMultiplier * maxToughnessMul
            debuffMul = 1 * wbMultiplier
        case "LNG":
            breakMul = 1 * wbMultiplier * maxToughnessMul
            debuffMul = 4 * wbMultiplier
        case "QUA":
            breakMul = 0.5 * wbMultiplier * maxToughnessMul
            debuffMul = 2.4 * wbMultiplier * maxToughnessMul
        case "IMG":
            breakMul = 0.5 * wbMultiplier * maxToughnessMul
            debuffMul = 0
    return breakMul + debuffMul

def findBestEnemy(enemyTeam: list[Enemy], debuffList: list[Debuff], atkType: list[str]) -> tuple[Enemy, float]:
    bestMul = 0
    bestEnemy = None
    for enemy in enemyTeam:
        currMul = getEnemyMul(enemy.enemyID, enemyTeam, debuffList, atkType)
        if currMul > bestMul:
            bestMul = currMul
            bestEnemy = enemy
    return bestEnemy, bestMul

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
    enemy = enemyTeam[enemyID]
    return getShredMul(enemy, debuffList, atkType) * getVulnMul(enemy, debuffList, atkType) * getUniMul(enemy, debuffList, atkType)

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
    return be

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