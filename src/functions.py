#Import Modules
from ezgraphics import GraphicsImage, GraphicsWindow, ImageWindow, GraphicsMenu
from random import randint
from pygame import mixer

#Import Classes
from classes import *

def playMusic(musicFile):
    '''playMusic [Plays a music file]
    
    Args:
        musicFile ([string]): [The name of the music file with the extension]
    '''
    mixer.init()
    mixer.music.load(musicFile)
    mixer.music.play()

def helpButton(helpBox, click, helpMenu, canvas, helpImage, buttonsImage):
    '''helpButton [Tells user information in game]
    
    Args:
        helpBox ([object]): [The object of the help button]
        click ([string]): [string containing the x y cordinates]
        helpMenu ([bool]): [Indication of menu is shown]
        canvas ([ezGraphics method]): [The window]
        helpImage ([string]): [Image of the help menu]
        buttonsImage ([string]): [The image of the buttons]
    
    Returns:
        [bool]: [Indication if menu is shown]
    '''
    if helpBox.checkBox(click):
        if not helpMenu:
            helpMenu = True
            canvas.drawImage(0,0,helpImage)
        else:
            helpMenu = False
            canvas.drawImage(0,0,buttonsImage)

    return helpMenu

def insertNum(click, imageCord, sudokuBoard, canvas, tileImage, win, history, sounds):
    '''insertNum [Inserts the number the user input to the board]
    
    Args:
        click ([string]): [string containing the x y cordinates]
        imageCord ([list]): [x y Cordinates of where to draw tiles ]
        sudokuBoard ([list]): [Contains the values of the sudoku board]
        canvas ([ezGraphics method]): [The window]
        tileImage ([tuple]): [Contains the images of the tile to draw on board]
        win ([ezGraphics]): [The window]
        history ([list]): [Adds user's input to the history list]
    '''
    correctX, correctY = getTilePos(click[0], click[1], imageCord)

    if correctX != -1 and correctY != -1 and not sudokuBoard[correctY][correctX].isPerm():
        tile = imageCord[correctX][correctY].split()
        canvas.drawImage(tile[0],tile[1], tileImage[10])
        click = win.getMouse()
        playMusic(sounds[1])

        numBox = ClickBox(89, 810, 671, 750)
        if numBox.checkBox(click):
            botNum = int(((click[0] - 89) // ((810-90)/9) + 1))
            canvas.drawImage(tile[0],tile[1], tileImage[botNum])
            sudokuBoard[correctY][correctX].setValue(botNum)
            updateHistory(history, str(correctY) + " " + str(correctX) + " " +  str(botNum))
        else:
            canvas.drawImage(tile[0],tile[1], tileImage[0])
            sudokuBoard[correctY][correctX].setValue(0)
            history.append(str(correctY) + " " + str(correctX) + " " +  str(0))

def clearButton(clearBox, click, canvas, board, buttons, imageCord, sudokuBoard, tileImage, helpMenu, helpImage):
    '''clearButton [Clears the screen if selected]
    
    Args:
        clearBox ([object]): [Checks whether the box has been selected]
        click ([string]): [string containing the x y cordinates]
        canvas ([ezGraphics method]): [The window]
        buttons ([string]): [The image of the buttons on the GUI]
        imageCord ([list]): [x y Cordinates of where to draw tiles]
        sudokuBoard ([list]): [The game board]
        tileImage ([tuple]): [Contains the images of the tile to draw on board]
    '''
    if clearBox.checkBox(click):
        canvas.clear()
        canvas.drawImage(0,0,board)
        canvas.drawImage(0,0,buttons)
        drawBoard(imageCord, sudokuBoard, canvas, tileImage)
        if helpMenu: canvas.drawImage(0,0,helpImage)

def historyButton(box, mouseClick, historyList, imageCordList, board, winCanvas, tile, removedList, forward = False):
    '''historyButton [Goes through the history and retrieves old of future values user input]
    
    Args:
        box ([object]): [Checks whether the box has been selected]
        mouseClick ([string]): [string containing the x y cordinates]
        historyList ([list]): [A list to traverse and get the value]
        imageCordList ([list]): [x y Cordinates of where to draw tiles ]
        board ([list]): [The game board]
        winCanvas ([ezGraphics]): [The window]
        tile ([tuple]): [Contains the images of the tile to draw on board]
        removedList ([list]): [A list to store the removed values from the list]
        forward (bool, optional): [Determines whether to traverse the list for back button or forward button]. Defaults to False.
    '''
    if box.checkBox(mouseClick) and len(historyList) > 0:
        prevList = historyList[-1].split()
        yCord = int(prevList[0])
        xCord = int(prevList[1])
        
        tileCord = imageCordList[xCord][yCord].split()
        if not forward: value = int(getOldValue(historyList, removedList))
        else: value = int(prevList[2])
        board[yCord][xCord].setValue(value)
        winCanvas.drawImage(tileCord[0], tileCord[1], tile[value])
        if forward: removedList.append(historyList.pop())

def getOldValue(historyList, removedList):
    '''getOldValue [Goes through a list and obtains the previous value]
    
    Args:
        historyList ([list]): [A list to traverse and get the value]
        removedList ([list]): [A list to store the removed values from the list]
    
    Returns:
        [int]: [A number to draw on the board]
    '''
    compare = (historyList[-1])[:3]
    #Go through list backwards
    value = 0
    for i in range(2,len(historyList)+1):
        prev = (historyList[-i])[:3]
        if compare == prev:
            value = (historyList[-i])[-1]
            break

    removedList.append(historyList.pop())

    return value

def updateHistory(historyList, prevValue):
    '''updateHistory [Adds previous value to the history, not adding duplicate previous value]
    
    Args:
        historyList ([list]): [Store the history]
        prevValue ([string]): [Containing the value to add to the history]
    '''
    if len(historyList) > 0:
        if historyList[-1] != prevValue:
            historyList.append(prevValue)

    elif prevValue != None:
        historyList.append(prevValue)

def getTilePos(xClick, yClick, imageCord):
    '''getTilePos [summary]
    
    Args:
        xClick ([int]): [x cordinate of mouse click]
        yClick ([int]): [y cordinate of mouse click]
        imageCord ([list]): [A list of where to draw the images]
    
    Returns:
        [int]: [valid cordinates of where to draw a tile]
    '''
    correctX = -1
    correctY = -1

    if(xClick >= 215 and  xClick <= 685):
        for i in range(len(imageCord)):
            for j in range(len(imageCord[i])):
                pos = imageCord[i][j].split()
                tempX= pos[0]
                if xClick > int(tempX):
                    correctX = i

    if(yClick > 165 and  yClick < 634):
        for i in range(len(imageCord)):
            for j in range(len(imageCord[i])):

                pos = imageCord[i][j].split()
                tempY= pos[1]

                if correctX == i and yClick > int(tempY): 
                    correctY = j
                    
    return correctX, correctY

def drawBoard(imageCord, sudokuBoard, canvas, tiles):
    '''drawBoard [summary]
    
    Args:
        imageCord ([list]): [x y Cordinates of where to draw tiles ]
        sudokuBoard ([list]): [The game board]
        canvas ([ezGraphics method]): [The window]
        tiles ([tuple]): [images to draw]
    '''
    for i in range(len(imageCord)):
        for j in range(len(imageCord[i])):
            if sudokuBoard[i][j].isPerm():
                tileValue = sudokuBoard[i][j].getValue()
                pos = imageCord[j][i].split()
                canvas.drawImage(int(pos[0]),int(pos[1]), tiles[tileValue])
                canvas.drawImage(int(pos[0]),int(pos[1]), tiles[11])

def checkGameOver(board):
    '''checkGameOver [Checks if the sudoku board is filled correctly]
    
    Args:
        board ([list]): [The board to check]
    
    Returns:
        [bool]: [Returns True if game is over otherwise false]
    '''
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j].getValue() == 0: 
                return False
            elif checkTaken(i, j, board):
                return False
    return True

def checkTaken(rowCheck, colCheck, table):
    '''checkTaken [Checks row and column if the row and column has the same digit as the one passed in]
    
    Args:
        rowCheck ([int]): [A number for which row to check]
        colCheck ([int]): [A number for which column to check]
        table ([list]): [A list to check the value]
    
    Returns:
        [bool]: [Returns true if the values passed in are taken]
    '''
    
    toCheck = table[rowCheck][colCheck].getValue()
    if toCheck == 0: return False
    for i in range(len(table)):
        if table[i][colCheck].getValue() == toCheck and i != rowCheck:
            return True

        if table[rowCheck][i].getValue() == toCheck and i != colCheck:
            return True

def getImageCord(maxNum):
    '''getImageCord [Gets the cordinates of where the images should be drawn on the GUI]
    
    Args:
        maxNum ([int]): [max number that can be on the board]
    
    Returns:
        [list]: [the cordinates of the tiles]
    '''
    posList = createTable(maxNum, maxNum)
    imageCoordList = []

    for i in range(215, 633,52):
        for j in range(165, 583,52):
                imageCoordList.append(str(i) + " " + str(j))

    count = 0
    for i in range(len(posList)):
        for j in range(len(posList[i])):
            posList[i][j] = imageCoordList[count]
            count += 1

    return posList

def menu(win, canvas, option, menu, sounds):
    '''menu [Shows user the start menu and asks user for difficulty]
    
    Args:
        win ([the window]): [description]
        canvas ([ezGraphics method]): [The window]
        option ([tuple]): [images of the options on GUI]
        menu ([string]): [image of the menu]

    Returns:
        [int]: [A number to indicate the difficulty]
    '''

    easy = ClickBox(344, 540, 475, 545)
    medium = ClickBox(307, 579, 565, 637)
    hard = ClickBox(295, 540, 662, 740)
    exitButton = ClickBox(796, 900, 359, 426)

    difficulty = None
    click = win.getMouse()
    while difficulty == None:

        #Easy
        if easy.checkBox(click):
            playMusic(sounds[0])
            canvas.drawImage(340,530, option[0])
            click = win.getMouse()
            if easy.checkBox(click):
                playMusic(sounds[1])
                difficulty = 38

        #Medium
        elif medium.checkBox(click):
            playMusic(sounds[0])
            canvas.drawImage(290,623, option[1])
            click = win.getMouse()
            if medium.checkBox(click):
                playMusic(sounds[1])
                difficulty = 57

        #Hard
        elif hard.checkBox(click):
            playMusic(sounds[0])
            canvas.drawImage(290,730, option[2])
            click = win.getMouse()
            if hard.checkBox(click):
                playMusic(sounds[1])
                difficulty = 75

        elif exitButton.checkBox(click):
            difficulty = -1

        else: click = win.getMouse()
                
        canvas.drawImage(0,0,menu)

    return difficulty

def makeValidRow(minNum, maxNum):
    '''makeValidRow [Creates a valid row based on the numbers input, no duplicate numbers in row]
    
    Args:
        minNum ([int]): [The minimum number that can be on the board]
        maxNum ([int]): [The maximum number that can be on the board]
    
    Returns:
        [list]: [A row with no duplicate numbers and numbers are in random order]
    '''
    row = []
    objectRow = []
    while(len(row) < maxNum):
        random = randint(minNum, maxNum)
        while random in row:
            random =randint(minNum, maxNum)
        row.append(random)
        numObject = Number(random)
        objectRow.append(numObject)
    return objectRow

def createBoard(maxNum,squareSize, startRow):
    '''createBoard [summary]
    
    Args:
        maxNum ([int]): [The maximum number that can be on the board]
        squareSize ([int]): [The size of a square on the board]
        startRow ([list]): [A starting row of x amount of numbers to convert to a sudoku board]
    
    Returns:
        [type]: [description]
    '''
    if(len(startRow) >= maxNum*maxNum):
        return startRow
    startShift = 0
    newRow = startRow[-maxNum:] + []
    rowNum = len(startRow) // maxNum
    if rowNum % squareSize == 0:
        newRow = shift(newRow,startShift, 1)
    else:
        newRow = shift(newRow,startShift, squareSize)
    startRow += newRow
    return createBoard(maxNum, squareSize, startRow)

def shift(row,start, stop):
    '''shift [Shifts a 1D list based on parameters]
    
    Args:
        row ([list]): [The row to shift]
        start ([int]): [Where to start shifting list]
        stop ([int]): [Where to end shifting list]
    
    Returns:
        [list]: [A new list shifted list]
    '''
    newRow = []
    oldRow = [] + row
    for i in range(start,stop):
        newRow.append(oldRow.pop(0))
    newRow = oldRow + newRow
    return newRow

def validIndices(maxNum, squareSize):
    '''validIndices [Gets valid indexes of which rows and columns to swap]
    
    Args:
        maxNum ([int]): [The maximum number that can be on the board]
        squareSize ([int]): [The size of a square on the board]
    
    Returns:
        [list]: [A list of valid indexes of which rows and columns to swap]
    '''
    values = []
    for i in range(maxNum):
        if (i + 1) % squareSize != 0: values.append(i)
    return values

def swapCol(maxNum, numbers, indices, count):
    '''swapCol [Swaps the columns in a list]
    
    Args:
        maxNum ([int]): [The maximum number that can be on the board]
        numbers ([list]): [1D list to swap the columns]
        indices ([list]): [A list containing which columns to swap]
        count ([int]): [How many times to swap the columns]
    '''
    for j in range(count):
        toSwap = indices[randint(0, (len(indices)-1))]
        for i in range(toSwap,maxNum**2,maxNum):
            numbers[i],numbers[i+1] = numbers[i+1],numbers[i]

def swapRow(table, indices, count):
    '''swapRow [Swaps the rows in a 2D list]
    
    Args:
        table ([list]): [A list to swap the rows]
        indices ([list]): [A list containing which rows to swap]
        count ([int]): [How many times to swap the rows]
    '''
    for i in range(count):
        toSwap = indices[randint(0, (len(indices)-1))]
        table[toSwap], table[toSwap+1] = table[toSwap+1], table[toSwap]

def createTable(rowSize, colSize):
    '''createTable [Creates a xRow by xCol table]

    Args:
        rowSize ([int]): [row size]
        colSize ([int]): [column size]

    Returns:
        [list]: [a rowSize x colSize table filled with 0]
    '''

    table = []
    for i in range(rowSize):
        row = [Number(0)] * colSize
        table.append(row)
    return table

def listTo2D(table, listTable):
    '''listTo2D [Converts a 1D list to a 2D list]
    
    Args:
        table ([list]): [Table to store 2D list]
        listTable ([list]): [1D list to convert to 2D]
    '''
    count = 0
    for i in range(len(table)):
        for j in range(len(table[i])):
            table[i][j] = Number(listTable[count].getValue())
            count += 1

def hideValues(newBoard, percent = 38):
    '''hideValues [Empties values in a given board]
    
    Args:
        newBoard ([list]): [A list containing number objects]
        percent (int, optional): [How many values to set 0 in list]. Defaults to 38.
    '''
    randPercent = randint(percent, percent + 4)
    for i in range(len(newBoard)):
        for j in range(len(newBoard[i])):
            if randint(0 , 100) <= randPercent:
                newBoard[i][j].setPerm()
                newBoard[i][j].setValue(0)