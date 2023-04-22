import sys

# model = {}
uchFlag = False
symbolSet = set()
clauseSet = set()
symbolList = []
clauseList = []
totalCalls = 0

def printCommand():
    print('command: python', end=' ')
    for i in range(len(sys.argv)):
        print(sys.argv[i], end=' ')
    print(' ')

def processCNF():
    global symbolList
    global clauseList
    global uchFlag
    filename = sys.argv[1]
    file = open(filename, 'r')
    for line in file:
        if (line[0] != '#'):
            clauseList.append(line.strip())
            symbols = line.split()
            for sym in symbols:
                if sym[0] == '-':
                    sym = sym[1:]
                if sym not in symbolList:
                    # model[sym] = 0
                    symbolList.append(sym)

    if sys.argv[-1] == '+UCH':
        uchFlag = True

    for i in range(2, len(sys.argv)):
        sym = sys.argv[i]
        if sym == '+UCH':
            continue
        clauseList.append(sym)
        if sym[0] == '-':
            sym = sym[1:]
        if sym not in symbolList:
            # model[sym] = 0
            symbolList.append(sym)
    '''symbolList = list(symbolSet)
    clauseList = list(clauseSet)'''
    #print('Set of symbols:', clauseList)

def unitClauseHeuristic(clauses, model):
    # print('UCH Clauses:')
    for clause in clauses:
        falseLiteralCount = 0
        unknownLiteralList = []
        isClauseTrue = False
        symbols = clause.split()
        # print(symbols)
        for sym in symbols:
            if sym[0] == '-':
                if sym[1:] in model and model[sym[1:]] == False:
                    isClauseTrue = True
                    break
                elif sym[1:] in model and model[sym[1:]] == True:
                    falseLiteralCount += 1
                else:
                    unknownLiteralList.append(sym)
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
            if unknownLiteralList[0][0] == '-':
                return (unknownLiteralList[0][1:], False)
            else:
                return (unknownLiteralList[0], True)
    return ()


def checkClauses(clauses, model):
    trueClauseCount = 0
    falseClauseCount = 0

    # print('checkClauses Clauses:')
    for clause in clauses:
        falseLiteralCount = 0
        symbols = clause.split()
        # print(symbols)
        for sym in symbols:
            if sym[0] == '-':
                if sym[1:] in model and model[sym[1:]] == False:
                    trueClauseCount += 1
                    # print('True')
                    break
                elif sym[1:] in model and model[sym[1:]] == True:
                    falseLiteralCount += 1
            else:
                if sym in model and model[sym] == True:
                    trueClauseCount += 1
                    # print('True')
                    break
                elif sym in model and model[sym] == False:
                    falseLiteralCount += 1
        if falseLiteralCount == len(symbols):
            falseClauseCount += 1   # Probably don't need this line
            # print('False')
            return 0
        
    if trueClauseCount == len(clauses):
        return 1
    
    return -1

def printFinalModel(model):
    finalModel = {}
    for symbol in symbolList:
        if symbol not in model:
            finalModel[symbol] = 0
        elif model[symbol] == True:
            finalModel[symbol] = 1
        elif model[symbol] == False:
            finalModel[symbol] = -1
    print('FINAL MODEL:', finalModel)


def DPPL(clauses, symbols, model, action):
    if (action != 'Root node'):
        print(action)

    global totalCalls
    totalCalls += 1
    # print(model)
    checkClausesRes = checkClauses(list(clauses), dict(model))

    if checkClausesRes == 1:
        print('')
        printFinalModel(model)
        print('Just the satisfied propositions:')
        propStr = ''
        for key in model:
            if model[key] == True:
                propStr += key
                propStr += ' '
        print(propStr)
        return True
    if checkClausesRes == 0:
        print('Backtracking occured')
        return False
    
    if uchFlag == True:
        uchTuple = unitClauseHeuristic(list(clauses), dict(model))
        if uchTuple:
            symbols.remove(uchTuple[0])
            actionStr = 'UCH: Forced assignment of ' + str(uchTuple[0]) + ' : ' + str(uchTuple[1]) + ' to model'
            return DPPL(list(clauses), list(symbols), dict(model) | {uchTuple[0]:uchTuple[1]}, actionStr)
    
    sym = symbols.pop(0)
    
    actionStrTrue = 'Trying ' + str(sym) + ' : True to model'
    actionStrFalse = 'Trying ' + str(sym) + ' : False to model'
    return DPPL(list(clauses), list(symbols), dict(model) | {sym:True}, actionStrTrue) or DPPL(list(clauses), list(symbols), dict(model) | {sym:False}, actionStrFalse)

def DPPLSat():
    # filename = sys.argv[1]
    result = DPPL(list(clauseList), list(symbolList), {}, 'Root node')
    if result == False:
        print('Unsatisifiable')
    print('Total DPLL calls:', totalCalls)
    print('UCH =', str(uchFlag))

printCommand()
processCNF()
# print('Symbol List:', symbolList)
# print('Clause List:', clauseList)
# print('UCHFlag:', uchFlag)
DPPLSat()
'''print('Number of arguments: {}'.format(len(sys.argv)))
print('Argument(s) passed: {}'.format(str(sys.argv)))'''