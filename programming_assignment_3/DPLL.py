import sys

# model = {}
uchFlag = False
symbolSet = set()
clauseSet = set()
totalCalls = 0

def printCommand():
    print('command: python', end=' ')
    for i in range(len(sys.argv)):
        print(sys.argv[i], end=' ')
    print(' ')

def processCNF():
    filename = sys.argv[1]
    file = open(filename, 'r')
    for line in file:
        if (line[0] != '#'):
            clauseSet.add(line)
            symbols = line.split()
            for sym in symbols:
                if sym[0] == '-':
                    sym = sym[1:]
                if sym not in symbolSet:
                    # model[sym] = 0
                    symbolSet.add(sym)

    if sys.argv[-1] == '+UCH':
        uchFlag = True

    for i in range(2, len(sys.argv)):
        sym = sys.argv[i]
        if sym == '+UCH':
            continue
        if sym[0] == '-':
            sym = sym[1:]
        if sym not in symbolSet:
            # model[sym] = 0
            symbolSet.add(sym)
    print('Set of symbols:', symbolSet)

def unitClauseHeuristic(clauses, model):
    for clause in clauses:
        falseLiteralCount = 0
        unknownLiteralList = []
        isClauseTrue = False
        symbols = clause.split()
        for sym in symbols:
            if sym[0] == '-':
                if sym[1:] in model and model[sym[1:]] == False:
                    isClauseTrue = True
                    break
                elif sym[1:] in model and model[sym[1:]] == True:
                    falseLiteralCount += 1
                else:
                    unknownLiteralList.append(sym[1:])
            else:
                if sym in model and model[sym] == True:
                    isClauseTrue = True
                    break
                elif sym in model and model[sym] == False:
                    falseLiteralCount += 1
                else:
                    unknownLiteralList.append(sym)
        if isClauseTrue == False and falseLiteralCount == len(symbols) - 1:
            #model.update({unknownLiteralList[0]:True})
            if sym[0] == '-':
                return (unknownLiteralList[0][1:], False)
            else:
                return (unknownLiteralList[0], True)
    return ()


def checkClauses(clauses, model):
    trueClauseCount = 0
    falseClauseCount = 0

    for clause in clauses:
        falseLiteralCount = 0
        symbols = clause.split()
        for sym in symbols:
            if sym[0] == '-':
                if sym[1:] in model and model[sym[1:]] == False:
                    trueClauseCount += 1
                    break
                elif sym[1:] in model and model[sym[1:]] == True:
                    falseLiteralCount += 1
            else:
                if sym in model and model[sym] == True:
                    trueClauseCount += 1
                    break
                elif sym in model and model[sym] == False:
                    falseLiteralCount += 1
        if falseLiteralCount == len(symbols):
            falseClauseCount += 1   # Probably don't need this line
            return 0
        
    if trueClauseCount == len(clauses):
        return 1
    
    return -1

def DPPL(clauses, symbols, model):
    # print(model, len(model) == len(symbolSet))
    '''
    if (4th paramter != "root node"):
        print(4th parameter)
    '''
    global totalCalls
    totalCalls += 1
    checkClausesRes = checkClauses(clauses, model)

    if checkClausesRes == 1:
        print('Model:', model)
        return True
    if checkClausesRes == 0:
        return False
    
    if uchFlag == True:
        uchTuple = unitClauseHeuristic(clauses, model)
        if not uchTuple:
            symbols.remove(uchTuple[0])
            return DPPL(clauses, set(symbols), dict(model) | {uchTuple[0]:uchTuple[1]})
    
    sym = symbols.pop()
    
    return DPPL(clauses, set(symbols), dict(model) | {sym:True}) or DPPL(clauses, set(symbols), dict(model) | {sym:False})

def DPPLSat():
    # filename = sys.argv[1]
    result = DPPL(clauseSet, symbolSet, {})
    if result == False:
        print('Unsatisifiable')
    print(totalCalls)

printCommand()
processCNF()
DPPLSat()
'''print('Number of arguments: {}'.format(len(sys.argv)))
print('Argument(s) passed: {}'.format(str(sys.argv)))'''