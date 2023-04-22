import sys

number = int(sys.argv[1])

# at most one queen in each column
for c in range(1, number + 1):
    print('# at most one queen in column', c)
    columnQueens = []
    for r in range(1, number + 1):
        queen = '-Q' + str(c) + str(r)
        columnQueens.append(queen)
    for r in range(1, number + 1):
        cnfStringTemplate = '-Q' + str(c) + str(r)
        for otherR in range(1, number + 1):
            cnfString = cnfStringTemplate
            if otherR != r:
                cnfString = cnfString + ' -Q' + str(c) + str(otherR)
                print(cnfString)

# at most one queen in each row
for r in range(1, number + 1):
    print('# at most one queen in row', r)
    rowQueens = []
    for c in range(1, number + 1):
        queen = '-Q' + str(c) + str(r)
        rowQueens.append(queen)
    for c in range(1, number + 1):
        cnfStringTemplate = '-Q' + str(c) + str(r)
        for otherC in range(1, number + 1):
            cnfString = cnfStringTemplate
            if otherC != c:
                cnfString = cnfString + ' -Q' + str(otherC) + str(r)
                print(cnfString)

# right to left diagonal
iterations = number
for r in range(1, number):
    print('# at most one queen in diagonalSet1')
    col = 1
    row = r
    diagonalQueens = []

    for i in range(iterations):
        queen = '-Q' + str(col) + str(row)
        diagonalQueens.append(queen)
        col += 1
        row += 1

    iterations -= 1

    for j in range(len(diagonalQueens)):
        for k in range(len(diagonalQueens)):
            if j != k:
                cnfString = diagonalQueens[j] + ' ' + diagonalQueens[k]
                print(cnfString)

iterations = number - 1
for c in range(2, number):
    print('# at most one queen in diagonalSet1')
    col = c
    row = 1
    diagonalQueens = []

    for i in range(iterations):
        queen = '-Q' + str(col) + str(row)
        diagonalQueens.append(queen)
        col += 1
        row += 1
    
    iterations -= 1

    for j in range(len(diagonalQueens)):
        for k in range(len(diagonalQueens)):
            if j != k:
                cnfString = diagonalQueens[j] + ' ' + diagonalQueens[k]
                print(cnfString)

# left to right diagonal
iterations = number
for r in range(1, number + 1):
    print('# at most one queen in diagonalSet2')
    col = number
    row = r
    diagonalQueens = []

    for i in range(iterations):
        queen = '-Q' + str(col) + str(row)
        diagonalQueens.append(queen)
        col -= 1
        row += 1
    
    iterations -= 1

    for j in range(len(diagonalQueens)):
        for k in range(len(diagonalQueens)):
            if j != k:
                cnfString = diagonalQueens[j] + ' ' + diagonalQueens[k]
                print(cnfString)

iterations = number - 1
for c in range(number - 1, 1, -1):
    print('# at most one queen in diagonalSet2')
    col = c
    row = 1
    diagonalQueens = []

    for i in range(iterations):
        queen = '-Q' + str(col) + str(row)
        diagonalQueens.append(queen)
        col -= 1
        row += 1

    iterations -= 1

    for j in range(len(diagonalQueens)):
        for k in range(len(diagonalQueens)):
            if j != k:
                cnfString = diagonalQueens[j] + ' ' + diagonalQueens[k]
                print(cnfString)

# at least one queen in each row
for r in range(1, number + 1):
    print('# at least one queen in row', r)
    cnfString = ''
    for c in range(1, number + 1):
        queen = 'Q' + str(c) + str(r)
        cnfString += queen
        if c != number:
            cnfString += ' '
    print(cnfString)

# at least one queen in each column
for c in range(1, number + 1):
    print('# at least one queen in column', c)
    cnfString = ''
    for r in range(1, number + 1):
        queen = 'Q' + str(c) + str(r)
        cnfString += queen
        if r != number:
            cnfString += ' '
    print(cnfString)



