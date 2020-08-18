import pygame
import pgzrun
import random
import sys

INCREASESPEED = 5
SPEED = 5
TITLE = 'Pong'

WIDTH = 800
HEIGHT = 600

WINDOWWIDTH = WIDTH
WINDOWHEIGHT = HEIGHT

BASICFONTSIZE = 20
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

#Global Variables to be used through our program
LINETHICKNESS = 10
PADDLESIZE = 100
PADDLEOFFSET = 20
start = 0
check = 0
rnd = 0
# Set up the colours
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

# width and height of a player paddle
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 

#Draws the arena the game will be played in. 
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Draw centre line
    pygame.draw.line(DISPLAYSURF, WHITE, (int(WINDOWWIDTH/2),0),(int(WINDOWWIDTH/2),WINDOWHEIGHT), int(LINETHICKNESS/4))

#Draws the paddle
def drawPaddle(paddle):
    #Stops paddle moving too low
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stops paddle moving too high
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Draws paddle
    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

#draws the ball
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

#moves the ball returns new position
def moveBall(ball, ballDirX, ballDirY):
    global start, check
    global INCREASESPEED
    global rnd
    if check == 1 or check == 2:
        if(ball.y < WINDOWHEIGHT/2 + rnd - 5):
            ball.y += SPEED
        elif(ball.y > WINDOWHEIGHT/2 + rnd + 5):
            ball.y -= SPEED
        else:
            check = 0
        return ball
        
    else:
        if(start == 0):
            INCREASESPEED = SPEED
            ball.x += (ballDirX * SPEED)
            ball.y += (ballDirY * SPEED)
            return ball

        if ballDirX == -1 :
            ball.x += (ballDirX * SPEED)
            ball.y += (ballDirY * INCREASESPEED)
        else:
            ball.x += (ballDirX * SPEED)
            ball.y += (ballDirY * INCREASESPEED)
        return ball

#Checks for a collision with a wall, and 'bounces' ball off it.
#Returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY, paddle1, paddle2):
    global start, check
    global LINETHICKNESS
    global rnd
    if ball.top <= (LINETHICKNESS) or ball.bottom >= (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS):
        rnd = random.randint(-250, 250)
        ballDirX = -1
        ballDirY = -1
        start = 0
        check = 2
        ball.right = paddle2.left
        ball.y = paddle2.centery
    if ball.right == (WINDOWWIDTH - LINETHICKNESS):
        rnd = random.randint(-250, 250)
        ballDirX = 1
        ballDirY = 1
        start = 0
        check = 1
        ball.left = paddle1.right
        ball.y = paddle1.centery
    return ballDirX, ballDirY

#Checks is the ball has hit a paddle, and 'bounces' ball off it.     
def checkHitBall(ball, paddle1, paddle2, ballDirX, ballDirY):
    global start
    global INCREASESPEED
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        start = 1
        if ballDirY == -1 and paddle1.y < 0:
            if(INCREASESPEED < 9):
                INCREASESPEED += 1
        elif ballDirY == 1 and paddle1.y > 0:
            if(INCREASESPEED < 9):
                INCREASESPEED += 1
        elif ballDirY == -1 and paddle1.y > 0:
            if(INCREASESPEED > 5):
                INCREASESPEED -=1
        elif ballDirY == 1 and paddle1.y < 0:
            if(INCREASESPEED > 5):
                INCREASESPEED -= 1
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        start = 1
        if ballDirY == -1 and paddle2.y < 0:
            if(INCREASESPEED < 9):
                INCREASESPEED += 1
        elif ballDirY == 1 and paddle2.y > 0:
            if(INCREASESPEED < 9):
                INCREASESPEED += 1
        elif ballDirY == -1 and paddle2.y > 0:
            if(INCREASESPEED > 5):
                INCREASESPEED -=1
        elif ballDirY == 1 and paddle2.y < 0:
            if(INCREASESPEED > 5):
                INCREASESPEED -= 1
        return -1
    else: return 1

#Checks to see if a point has been scored returns new score
def checkPointScoredA(paddle, ball, score, ballDirX):
    #reset points if left wall is hit
    global start
    if score == 11:
        start = 3
        return score

    if ball.left == LINETHICKNESS: 
        return score
    #1 point for hitting the ball
    elif ballDirX == -1 and paddle.right == ball.left and paddle.top < ball.top and paddle.bottom > ball.bottom:
        return score
    #5 points for beating the other paddle
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 1
        return score
    #if no points scored, return score unchanged
    else: return score
def checkPointScoredB(paddle, ball, score, ballDirX):
    #reset points if left wall is hit
    global start
    if score == 11:
        start = 4
        return score

    if ball.right == WINDOWWIDTH - LINETHICKNESS: 
        return score
    #1 point for hitting the ball
    elif ballDirX == 1 and paddle.left == ball.right and paddle.top < ball.top and paddle.bottom > ball.bottom:
        return score
    #5 points for beating the other paddle
    elif ball.left == LINETHICKNESS:
        score += 1
        return score
    #if no points scored, return score unchanged
    else: return score


#Artificial Intelligence of computer player   
def artificialIntelligenceA(ball, ballDirX, paddle1):
    #If ball is moving away from paddle, center bat
    global check, rnd
    if check == 1:
        if(paddle1.centery < WINDOWHEIGHT/2 + rnd):
            paddle1.y += SPEED
        elif(paddle1.centery > WINDOWHEIGHT/2 + rnd):
            paddle1.y -= SPEED
        else:
            check = 0
        return paddle1
    elif check == 0:
        if ballDirX == 1:
            if paddle1.centery < (WINDOWHEIGHT/2):
                paddle1.y += SPEED + 1
            elif paddle1.centery > (WINDOWHEIGHT/2):
                paddle1.y -= SPEED + 1
    #if ball moving towards bat, track its movement. 
        elif ballDirX == -1:
            if paddle1.centery < ball.centery:
                paddle1.y += SPEED + 1
            else:
                paddle1.y -= SPEED + 1
        return paddle1
    else: return paddle1

def artificialIntelligenceB(ball, ballDirX, paddle2):
    #If ball is moving away from paddle, center bat
    global check, rnd
    if check == 2:
        if(paddle2.centery < WINDOWHEIGHT/2 + rnd):
            paddle2.y += SPEED
        elif(paddle2.centery > WINDOWHEIGHT/2 + rnd):
            paddle2.y -= SPEED
        else:
            check = 0
        return paddle2
    elif check == 0:
        if ballDirX == -1:
            if paddle2.centery < (WINDOWHEIGHT/2):
                paddle2.y += SPEED + 1
            elif paddle2.centery > (WINDOWHEIGHT/2):
                paddle2.y -= SPEED + 1
    #if ball moving towards bat, track its movement. 
        elif ballDirX == 1:
            if paddle2.centery < ball.centery:
                paddle2.y += SPEED + 1
            else:
                paddle2.y -= SPEED + 1
        return paddle2
    else: return paddle2

#Displays the current score on the screen
def displayScoreA(score):
    resultSurf = BASICFONT.render('AI_A_Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (50, 25)
    screen.blit(resultSurf, resultRect)

def displayScoreB(score):
    resultSurf = BASICFONT.render('AI_B_Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 200, 25)
    screen.blit(resultSurf, resultRect)

#Initiate variable and set starting positions
#any future changes made within rectangles
ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2
scoreA = 0
scoreB = 0

#Keeps track of ball direction
ballDirX = -1 ## -1 = left 1 = right
ballDirY = -1 ## -1 = up 1 = down

#Creates Rectangles for ball and paddles.
paddle1 = Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS,PADDLESIZE)
paddle2 = Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,PADDLESIZE)
ball = Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

pygame.mouse.set_visible(0) # make cursor invisible

def draw():
    global start

    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    displayScoreA(scoreA)
    displayScoreB(scoreB)
    if(start == 3):
        screen.draw.text(
            'Winner is AI_A~!',
            color=(0,0,205),
            center=(400, 300),
            fontsize=80
        )
        screen.draw.text(
            'restart button is "r"',
            color=(205,0,0),
            center=(400, 500),
            fontsize=40
        )
        screen.draw.text(
            'EXIT button is "e"',
            color=(0,205,0),
            center=(400, 545),
            fontsize=40
        )
        return
    if(start == 4):
        screen.draw.text(
            'Winner is AI_B~!',
            color=(0,0,205),
            center=(400, 300),
            fontsize=80
        )
        screen.draw.text(
            'restart button is "r"',
            color=(205,0,0),
            center=(400, 500),
            fontsize=40
        )
        screen.draw.text(
            'EXIT button is "e"',
            color=(0,205,0),
            center=(400, 545),
            fontsize=40
        )
        return
    drawBall(ball)

def update():
    global ball
    global ballDirX, ballDirY
    global scoreA, scoreB
    global paddle1, paddle2
    global start, check

    if(start == 3 or start == 4):
        if keyboard.r :
            start = 0
            scoreA = 0
            scoreB = 0
            ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2
            ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2
            paddle1.centery = (WINDOWHEIGHT - PADDLESIZE) /2
            paddle2.centery = (WINDOWHEIGHT - PADDLESIZE) /2
            ballDirX = -1
            ballDirY = -1
            check = 0
        if keyboard.e :
            exit()
        return

    ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY, paddle1, paddle2)
    ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX, ballDirY)
    ball = moveBall(ball, ballDirX, ballDirY)
    paddle1 = artificialIntelligenceA (ball, ballDirX, paddle1)
    paddle2 = artificialIntelligenceB (ball, ballDirX, paddle2)
    scoreA = checkPointScoredA(paddle1, ball, scoreA, ballDirX)
    scoreB = checkPointScoredB(paddle2, ball, scoreB, ballDirX)

pgzrun.go()