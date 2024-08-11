from Buff import *

def matchBuff(char, buff) -> bool:
    return True if (char.role == buff.target) else False

def parseBuffs(lst: list, playerTeam: list) -> list:
    buffList = []
    for buff in lst:
        if buff.target == "ALL": #teamwide buff, need to add 4 instances
            for char in playerTeam:
                target = char.role if (buff.tickDown == "SELF") else buff.tickDown
                buffList.append(Buff(buff.name, buff.buffType, buff.val, char.role, buff.atkType, buff.turns, buff.stackLimit, target))
        else: #single target buff, only add one instance
            target = buff.target if (buff.tickDown == "SELF") else buff.tickDown
            buffList.append(Buff(buff.name, buff.buffType, buff.val, buff.target, buff.atkType, buff.turns, buff.stackLimit, target))
    return buffList

def parseDebuffs(lst: list, enemyTeam: list) -> list:
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

def getCharSPD(char, buffList) -> float:
    baseSPD = char.baseSPD
    spdPercent = sumBuffs(findBuffs(char.role, "SPD%", buffList))
    spdFlat = sumBuffs(findBuffs(char.role, "SPD", buffList)) + char.getSPD()
    return baseSPD * (1 + spdPercent) + spdFlat

def resetCharAV(char, buffList) -> float:
    char.currAV = 10000 / getCharSPD(char, buffList)
    
def advanceChar(target: str, advPercent: float, playerTeam: list, buffList: list):
    for char in playerTeam:
        if char.role == target:
            char.advanceAV(advPercent, getCharSPD(char, buffList))
    
def findBuffs(charRole: str, buffType: str, buffList: list) -> list:
    return [x for x in buffList if (x.buffType == buffType and x.target == charRole)]

def sumBuffs(buffList):
    return sum([x.val for x in buffList])