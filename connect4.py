import pgzrun
import pygame
import sys
pygame.init()

WIDTH = 700
HEIGHT = 700
TITLE = 'connect4_201903590최승필'
BOX = Rect((0,0), (700, 600))
COL = 7
LOW = 6
countLow = [6,6,6,6,6,6,6]
nowColor = (255,255,0)

table = [[0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]] 

def draw():
    screen.fill('white')
    screen.draw.filled_rect(BOX, (0,0,205))
    
    for i in range(LOW):
        for j in range(COL):
            if(table[i][j]==0):
                screen.draw.filled_circle((50 + j*100 ,50+ i*100),35, 'white')
            elif(table[i][j]==1):
                screen.draw.filled_circle((50 + j*100 ,50+ i*100),35, 'yellow')
            else:
                screen.draw.filled_circle((50 + j*100 ,50+ i*100),35, 'red')
   
    if checkWinner() == 1 :
        screen.draw.text(
            'Winner is Yellow~!',
            color=(0,0,0),
            center=(150, 650),
            fontsize=40
        )

    elif checkWinner() == 2 :
        screen.draw.text(
            'Winner is Red~!',
            color=(0,0,0),
            center=(150, 650),
            fontsize=40
        )
    elif checkWinner() == 3:
        screen.draw.text(
            'Draw~!',
            color=(0,0,0),
            center=(150, 650),
            fontsize=40
        )
    if checkWinner() != 0 :
        screen.draw.text(
            'Restart button is "r"',
            color=(0,0,255),
            center=(500, 640),
            fontsize = 40
        )
        screen.draw.text(
            'EXIT button is "e"',
            color=(255,0,0),
            center=(500, 665),
            fontsize = 40
        )

def changeSet(area):
    global countLow
    global table
    global nowColor
    if nowColor == (255,0,0):
        table[countLow[area]-1][area] = 2
    else:
        table[countLow[area]-1][area] = 1
    countLow[area]-=1
    
    if countLow[area] == 0:
        countLow[area] = 1

def checkWinner():
    global table
    global LOW
    global COL
    count = 0
    #가로 네개
    for i in range(LOW):
        for j in range(4):
            if table[i][j] == 1 and table[i][j+1] == 1 and table[i][j+2] == 1 and table[i][j+3] == 1:
                return 1
            elif table[i][j] == 2 and table[i][j+1] == 2 and table[i][j+2] == 2 and table[i][j+3] == 2:
                return 2
    #세로네개
    for j in range(COL):
        for i in range(3):
            if table[i][j] == 1 and table[i+1][j] == 1 and table[i+2][j] == 1 and table[i+3][j] == 1:
                return 1  
            elif table[i][j] == 2 and table[i+1][j] == 2 and table[i+2][j] == 2 and table[i+3][j] == 2:       
                return 2
    #대각선검사/
    for i in range(3):
        for j in range(3, COL):
            if table[i][j]==1 and table[i+1][j-1]==1 and table[i+2][j-2]==1 and table[i+3][j-3]==1:
                return 1
            elif table[i][j]==2 and table[i+1][j-1]==2 and table[i+2][j-2]==2 and table[i+3][j-3]==2:
                return 2
    #대각선검사\
    for i in range(3):
       for j in range(4):
           if table[i][j]==1 and table[i+1][j+1]==1 and table[i+2][j+2]==1 and table[i+3][j+3]==1:
                return 1
           elif table[i][j]==2 and table[i+1][j+1]==2 and table[i+2][j+2]==2 and table[i+3][j+3]==2:
                return 2
    #무승부
    for i in range(LOW):
        for j in range(COL):
            if table[i][j] == 0:
                count +=1
    if count == 0:
        return 3

    return 0

def update():
    global table
    global countLow
    global nowColor

    if keyboard.r and checkWinner() != 0:
        table = [[0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0]] 
        countLow = [6,6,6,6,6,6,6]
        nowColor = (255,255,0)
    if keyboard.e and checkWinner() != 0:
        sys.exit()

def on_mouse_down(pos, button):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global nowColor

    if checkWinner() != 0:
        return

    if click[1] == 0:
        if click[0] == 1 and mouse[0] in range(0, 100) and mouse[1] in range(600):
            changeSet(0)
        elif click[0] == 1 and mouse[0] in range(100, 200) and mouse[1] in range(600):
            changeSet(1)
        elif click[0] == 1 and mouse[0] in range(200, 300) and mouse[1] in range(600):
            changeSet(2)
        elif click[0] == 1 and mouse[0] in range(300, 400) and mouse[1] in range(600):
            changeSet(3)
        elif click[0] == 1 and mouse[0] in range(400, 500) and mouse[1] in range(600):
            changeSet(4)  
        elif click[0] == 1 and mouse[0] in range(500, 600) and mouse[1] in range(600):
            changeSet(5)
        elif click[0] == 1 and mouse[0] in range(600, 700) and mouse[1] in range(600):
            changeSet(6) 
    
        if click[0] == 1 and mouse[0] in range(700) and mouse[1] in range(600):
            if nowColor == (255,255,0):
                    nowColor = (255,0,0)
            else:
                    nowColor = (255,255,0)
                              
pgzrun.go()