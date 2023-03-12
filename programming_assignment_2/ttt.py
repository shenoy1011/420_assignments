board = [['','',''], ['','',''], ['','','']]

def show():
    for i in range(3):
        for j in range(3):
            if (board[i][j] == ''):
                print('. ', end = '')
            elif (board[i][j] == 'X'):
                print('X ', end = '')
            elif (board[i][j] == 'O'):
                print('O ', end = '')
            
            if (j == 2):
                print('')

def boardEval(board):
    if (board[0][0] != '' and board[0][0] == board[0][1] and board[0][1] == board[0][2]):
        # Check first row
        # print(' ')
        return board[0][0] + ' Wins'
    elif (board[1][0] != '' and board[1][0] == board[1][1] and board[1][1] == board[1][2]): 
        # Check second row
        # print(' ')
        return board[1][0] + ' Wins'
    elif (board[2][0] != '' and board[2][0] == board[2][1] and board[2][1] == board[2][2]): 
        # Check third row
        # print(' ')
        return board[2][0] + ' Wins'
    elif (board[0][0] != '' and board[0][0] == board[1][0] and board[1][0] == board[2][0]): 
        # Check first column
        # print(' ')
        return board[0][0] + ' Wins'
    elif (board[0][1] != '' and board[0][1] == board[1][1] and board[1][1] == board[2][1]): 
        # Check second column
        # print(' ')
        return board[0][1] + ' Wins'
    elif (board[0][2] != '' and board[0][2] == board[1][2] and board[1][2] == board[2][2]): 
        # Check third column
        # print(' ')
        return board[0][2] + ' Wins'
    elif (board[0][0] != '' and board[0][0] == board[1][1] and board[1][1] == board[2][2]): 
        # Check left to right diagonal
        # print(' ')
        return board[0][0] + ' Wins'
    elif (board[0][2] != '' and board[0][2] == board[1][1] and board[1][1] == board[2][0]): 
        # Check right to left diagonal
        # print(' ')
        return board[0][2] + ' Wins'
    
    for i in range(3):
        for j in range(3):
            if (board[i][j] == ''):
                return 'Game In Progress'
    
    # print(' ')
    return 'Game Ends In Draw'


def move(piece, rowLetter, colNum):
    rowIndex = -1
    colIndex = -1

    if (rowLetter == 'A'):
        rowIndex = 0
    elif (rowLetter == 'B'):
        rowIndex = 1
    elif (rowLetter == 'C'):
        rowIndex = 2
    else:
        print('Invalid input')
        return

    if (colNum == '1'):
        colIndex = 0
    elif (colNum == '2'):
        colIndex = 1
    elif (colNum == '3'):
        colIndex = 2
    else:
        print('Invalid input')
        return
    
    if (board[rowIndex][colIndex] != ''):
        print('Invalid input')
        return
    
    board[rowIndex][colIndex] = piece
    show()

def getRowLetter(rowIndex):
    rowLetter = ''

    if (rowIndex == 0):
        rowLetter = 'A'
    elif (rowIndex == 1):
        rowLetter = 'B'
    elif (rowIndex == 2):
        rowLetter = 'C'

    return rowLetter

def getColNum(colIndex):
    colNum = ''

    if (colIndex == 0):
        colNum = '1'
    elif (colIndex == 1):
        colNum = '2'
    elif (colIndex == 2):
        colNum = '3'

    return colNum
        
def maxscore(piece, boardInput, depth):
    status = boardEval(boardInput)
    if (piece == 'X' and status == 'X Wins'):
        util = 1.0 - (0.1 * depth)
        return util, 'null', 1
    elif (piece == 'X' and status == 'O Wins'):
        util = -1.0 + (0.1 * depth)
        return util, 'null', 1
    elif (piece == 'O' and status == 'O Wins'):
        util = 1.0 - (0.1 * depth)
        return util, 'null', 1
    elif (piece == 'O' and status == 'X Wins'):
        util = -1.0 + (0.1 * depth)
        return util, 'null', 1
    elif (status == 'Game Ends In Draw'):
        return 0.0, 'null', 1
    
    utility = -100
    move = ''
    childrenNodes = 0

    # print('Maxscore ' + piece + ' with depth: ' + str(depth))
    for i in range(3):
        for j in range(3):
            if (boardInput[i][j] == ''):
                boardCopy = [row[:] for row in boardInput]
                boardCopy[i][j] = piece
                result = ()
                if (piece == 'X'):
                    result = minscore('O', boardCopy, 1 + depth)
                else:
                    result = minscore('X', boardCopy, 1 + depth)
                
                childrenNodes += result[2]
                # print('Considered ' + str(result[0]) + ' ' + result[1])
                """print(result)
                print(result[0])
                print(type(result[0]))"""
                if (result[0] > utility):
                    utility = result[0]
                    rowLetter = getRowLetter(i)
                    colNum = getColNum(j)
                    move = piece + ' ' + rowLetter + ' ' + colNum
                if (depth == 1):
                    rowLetter = getRowLetter(i)
                    colNum = getColNum(j)
                    print('move (' + rowLetter + ',' + colNum + '), Utility score: ' + str(result[0]))

    childrenNodes += 1
    if (depth == 1):
        print('Number of nodes searched: ' + str(childrenNodes))

    return utility, move, childrenNodes

def minscore(piece, boardInput, depth):
    status = boardEval(boardInput) 
    if (piece == 'X' and status == 'X Wins'):
        util = -1.0 + (0.1 * depth)
        return util, 'null', 1
    elif (piece == 'X' and status == 'O Wins'):
        util = 1.0 - (0.1 * depth)
        return util, 'null', 1
    elif (piece == 'O' and status == 'O Wins'):
        util = -1.0 + (0.1 * depth)
        return util, 'null', 1
    elif (piece == 'O' and status == 'X Wins'):
        util = 1.0 - (0.1 * depth)
        return util, 'null', 1
    elif (status == 'Game Ends In Draw'):
        return 0.0, 'null', 1
    
    utility = 100
    move = ''
    childrenNodes = 0

    # print('Minscore ' + piece + ' with depth: ' + str(depth))
    for i in range(3):
        for j in range(3):
            if (boardInput[i][j] == ''):
                boardCopy = [row[:] for row in boardInput]
                boardCopy[i][j] = piece
                result = ()
                if (piece == 'X'):
                    result = maxscore('O', boardCopy, 1 + depth)
                else:
                    result = maxscore('X', boardCopy, 1 + depth)

                childrenNodes += result[2]
                # print('Considered ' + str(result[0]) + ' ' + result[1])
                """print(result)
                print(result[0])
                print(type(result[0]))"""
                if (result[0] < utility):
                    utility = result[0]
                    rowLetter = getRowLetter(i)
                    colNum = getColNum(j)
                    move = piece + ' ' + rowLetter + ' ' + colNum
    
    childrenNodes += 1

    return utility, move, childrenNodes

def choose(piece):  
    result = maxscore(piece, board, 1)
    move(result[1][0], result[1][2], result[1][4])


while True:
    command = input('>> ')
    if (command == 'ttt'):
        print('Welcome to tic tac toe')
        show()
    elif (command[:4] == "move"):
        pieceInput = command[5]
        rowInput = command[7]
        colInput = command[9]
        move(pieceInput, rowInput, colInput)

        result = boardEval(board)
        if (result != 'Game In Progress'):
            print('')
            print(result)
            break
    elif (command[:6] == 'choose'):
        choose(command[7])

        result = boardEval(board)
        if (result != 'Game In Progress'):
            print('')
            print(result)
            break
    elif (command == 'show'):
        show()
    elif (command == 'quit'):
        break