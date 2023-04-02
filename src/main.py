#Import Modules
from ezgraphics import GraphicsImage, GraphicsWindow, ImageWindow, GraphicsMenu
from math import sqrt

#Import CLasses
from classes import *

#Import Functions
from functions import *

def main():
    #Sudoku Constants
    MAX_NUM = 9
    MIN_NUM = 1
    SQUARE_SIZE = int(sqrt(MAX_NUM))
    SWAPS = 14

    #Windows
    BG_HEIGHT = 900
    BG_WIDTH = 800
    LOAD_HEIGHT = 300
    LOAD_WIDTH = 750

    #Images
    FOLDER = "./Assets/"
    TITLE = "Sudoku"
    LOAD_SCREEN = FOLDER + "Load.gif"
    BUTTONS = GraphicsImage(FOLDER + "Buttons.png")
    BOARD = GraphicsImage(FOLDER + "Board.png")
    HELP = GraphicsImage(FOLDER + "Help.png")
    MENU = GraphicsImage(FOLDER + "Menu.png")
    ONE = GraphicsImage(FOLDER + "1.png")
    TWO = GraphicsImage(FOLDER + "2.png")
    THREE = GraphicsImage(FOLDER + "3.png")
    FOUR = GraphicsImage(FOLDER + "4.png")
    FIVE = GraphicsImage(FOLDER + "5.png")
    SIX = GraphicsImage(FOLDER + "6.png")
    SEVEN = GraphicsImage(FOLDER + "7.png")
    EIGHT = GraphicsImage(FOLDER + "8.png")
    NINE = GraphicsImage(FOLDER + "9.png")
    BLANK = GraphicsImage(FOLDER + "Blank.png")
    PERMANENT = GraphicsImage(FOLDER + "Permanent.png")
    HIGHLIGHT = GraphicsImage(FOLDER + "Highlight.png")
    EASY = GraphicsImage(FOLDER + "Easy.png")
    MEDIUM = GraphicsImage(FOLDER + "Medium.png")
    HARD = GraphicsImage(FOLDER + "Hard.png")
    DIFFICULTY = (EASY, MEDIUM, HARD)
    TILES = (BLANK, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, HIGHLIGHT, PERMANENT)

    #Sounds
    SOUND_FOLDER = FOLDER + "Sounds/"
    SOUND_1 = SOUND_FOLDER + "Menu.mp3"
    SOUND_2 = SOUND_FOLDER + "Tile.mp3"
    SOUND_3 = SOUND_FOLDER + "GameOver.mp3"
    SOUNDS = (SOUND_1,SOUND_2,SOUND_3)

    #Loading Screen
    loadScreen = GIF(LOAD_SCREEN)
    loadScreen.setWin(LOAD_WIDTH, LOAD_HEIGHT)
    loadScreen.play(6) #Play for 6 seconds

    #Create window
    win = GraphicsWindow(BG_HEIGHT, BG_WIDTH)
    win.setTitle(TITLE)
    canvas = win.canvas()

    gameOver = False
    while not gameOver:
        canvas.clear()

        #Get Difficulty
        canvas.drawImage(0,0,MENU)
        difficulty = menu(win,canvas, DIFFICULTY, MENU, SOUNDS)
        if difficulty == -1: break

        #Loading Screen
        loading = Animation("LoadBoard", 23)
        loading.play(canvas,FOLDER + "LoadBoard/")

        #Draw Board
        canvas.clear()
        canvas.drawImage(0,0,BOARD)
        canvas.drawImage(0,0,BUTTONS)

        #Buttons
        backBox = ClickBox(65, 182, 352, 447)
        forwardBox = ClickBox(707, 826, 352, 447)
        clearBox = ClickBox(404, 496, 10, 68)
        helpBox = ClickBox(9, 183, 10, 91)
        exitBox = ClickBox(718, 892, 10, 88)

        #Get a list for tile positions
        imageCord = getImageCord(MAX_NUM)

        #Create Sudoku Board
        #Create a random row and use that to create sudoku board
        startRow = makeValidRow(MIN_NUM, MAX_NUM)
        board = createBoard(MAX_NUM, SQUARE_SIZE, startRow)

        #Get valid indexes for swaping row and columns
        validIndex = validIndices(MAX_NUM, SQUARE_SIZE)

        swapCol(MAX_NUM, board, validIndex, SWAPS)

        #Convert list to 2D List
        sudokuBoard = createTable(MAX_NUM, MAX_NUM)
        listTo2D(sudokuBoard, board)

        swapRow(sudokuBoard, validIndex, SWAPS)
        hideValues(sudokuBoard,difficulty)

        #Draw tiles on GUI
        drawBoard(imageCord, sudokuBoard, canvas, TILES)

        #Sudoku Game
        history = []
        forward = []
        helpMenu = False
        while not gameOver:

            #Get Input from player
            click = win.getMouse()
            playMusic(SOUNDS[1])

            #Place number on board
            insertNum(click, imageCord, sudokuBoard, canvas, TILES, win, history, SOUNDS)

            #Back Button
            historyButton(backBox, click, history, imageCord, sudokuBoard, canvas, TILES, forward)

            #Forward Button
            historyButton(forwardBox, click, forward, imageCord, sudokuBoard, canvas, TILES, history, True)

            #Clear Button
            clearButton(clearBox, click, canvas, BOARD,BUTTONS, imageCord, sudokuBoard, TILES, helpMenu, HELP)

            #Help Button
            helpMenu = helpButton(helpBox, click, helpMenu, canvas, HELP, BUTTONS)

            #Exit Button
            if exitBox.checkBox(click):
                loading.play(canvas,FOLDER + "LoadBoard/")
                break

            #Check if game is over
            gameOver = checkGameOver(sudokuBoard)

        if gameOver:
            #Load Game Over Animation
            gameOver = Animation("GameOver", 60)
            playMusic(SOUNDS[2])
            gameOver.play(canvas, FOLDER + "GameOver/")
            time.sleep(2)
            gameOver = False

#Run the program
main()