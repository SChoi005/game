import pgzrun
import gameinput
import gamemaps
from random import randint
from datetime import datetime
WIDTH = 600
HEIGHT = 660

player = Actor("pacman_o") # Load in the player Actor image
player.score = 0
player.lives = 3
level = 0
SPEED = 3
GHOSTSPEED = 3

def draw(): # Pygame Zero draw function
    global pacDots, player, GHOSTSPEED
    screen.blit('header', (0, 0))
    screen.blit('colourmap', (0, 80))
    pacDotsLeft = 0
    for a in range(len(pacDots)):
        if pacDots[a].status == 0:
            pacDots[a].draw()
            pacDotsLeft += 1
        if pacDots[a].collidepoint((player.x, player.y)):
            if pacDots[a].status == 0:
                if pacDots[a].type == 2:
                    GHOSTSPEED+=2
                    for g in range(len(ghosts)): ghosts[g].status = 1200
                else:
                    player.score += 10
            pacDots[a].status = 1
    if pacDotsLeft == 0: player.status = 2
    drawGhosts()
    getPlayerImage()
    player.draw()
    drawLives()
    screen.draw.text("LEVEL "+str(level) , topleft=(10, 10), owidth=0.5, ocolor=(0,0,255), color=(255,255,0) , fontsize=40)
    screen.draw.text(str(player.score) , topright=(590, 20), owidth=0.5, ocolor=(255,255,255), color=(0,64,255) , fontsize=60)
    if player.status == 3: drawCentreText("GAME OVER")
    if player.status == 2: drawCentreText("LEVEL CLEARED!\nPress Enter or Button A\nto Continue")
    if player.status == 1: drawCentreText("CAUGHT!\nPress Enter or Button A\nto Continue")

def drawCentreText(t):
    screen.draw.text(t , center=(300, 434), owidth=0.5, ocolor=(255,255,255), color=(255,64,0) , fontsize=60)

def update(): # Pygame Zero update function
    global player, moveGhostsFlag, ghosts, GHOSTSPEED, SPEED
    
    if player.status == 0:
        if moveGhostsFlag == 4: moveGhosts()
        for g in range(len(ghosts)):
            if ghosts[g].status > 0: ghosts[g].status -= 1
            if ghosts[g].collidepoint((player.x, player.y)):
                if ghosts[g].status > 0:
                    player.score += 100
                    animate(ghosts[g], pos=(290, 370), duration=1/SPEED, tween='linear', on_finished=flagMoveGhosts)
                else:
                    player.lives -= 1
                    sounds.pac2.play()
                    if player.lives == 0:
                        player.status = 3
                        music.fadeout(3)
                    else:
                        player.status = 1
        if player.inputActive:
            gameinput.checkInput(player)
            gamemaps.checkMovePoint(player)
            if player.movex or player.movey:
                inputLock()
                sounds.pac1.play()
                animate(player, pos=(player.x + player.movex, player.y + player.movey), duration=1/SPEED, tween='linear', on_finished=inputUnLock)
    if player.status == 1:
        i = gameinput.checkInput(player)
        if i == 1:
            player.status = 0
            player.x = 290
            player.y = 570
    if player.status == 2:
        i = gameinput.checkInput(player)
        if i == 1:
            init()

def init():
    global player, level
    initDots()
    initGhosts()
    player.x = 290
    player.y = 570
    player.status = 0
    inputUnLock()
    level += 1
    music.play("pm1")
    music.set_volume(0.2)

def drawLives():
    for l in range(player.lives): screen.blit("pacman_o", (10+(l*32),40))

def getPlayerImage():
    global player
    dt = datetime.now()
    a = player.angle
    tc = dt.microsecond%(500000/SPEED)/(100000/SPEED)
    if tc > 2.5 and (player.movex != 0 or player.movey !=0):
        if a != 180:
            player.image = "pacman_c"
        else:
            player.image = "pacman_cr"
    else:
        if a != 180:
            player.image = "pacman_o"
        else:
            player.image = "pacman_or"
    player.angle = a

def drawGhosts(): 
    for g in range(len(ghosts)):
        if ghosts[g].x > player.x: #ghosts가 플레이어의 x보다 오른쪽에 있을 때 
            if ghosts[g].status > 200 or (ghosts[g].status > 1 and ghosts[g].status%2 == 0): #ghosts의 상태가 200초가 이거나 ghost의 status == 0,2 일때 파란색 이미지로 바뀐다
                ghosts[g].image = "ghost5"
            else:#바라보는 눈빛방향
                ghosts[g].image = "ghost"+str(g+1)+"r"
        else: #ghosts가 플레이어의 x보다 왼쪽에 있을 때
            if ghosts[g].status > 200 or (ghosts[g].status > 1 and ghosts[g].status%2 == 0): #ghosts의 상태가 200초가 이거나 ghost의 status == 0,2 일때 파란색,본래모습 이미지로 바뀐다 
                ghosts[g].image = "ghost5"
            else:#바라보는 눈빛 방향
                ghosts[g].image = "ghost"+str(g+1)
        ghosts[g].draw()

def moveGhosts():
    global moveGhostsFlag, player
    dmoves = [(1,0),(0,1),(-1,0),(0,-1)]
    moveGhostsFlag = 0
    for g in range(len(ghosts)):
        dirs = gamemaps.getPossibleDirection(ghosts[g])
        if ghosts[g].status > 0:
            runAway(g, dirs)
        else:    
            if inTheCentre(ghosts[g]):#유령이 시작박스에 있을때 방향은 3(위로)
                ghosts[g].dir = 3
            else:#시작박스가 아니라면, 0,2번 유령은 플레이어를 추격/ 1,3번유령은 플레이어에 대해 매복후 추격
                if g == 0: followPlayer(g, dirs)
                if g == 2: followPlayer(g, dirs)
                if (player.x - ghosts[g].x)**2 + (player.y - ghosts[g].y)**2 <= 22500:
                    if g == 1: followPlayer(g, dirs)
                    if g == 3: followPlayer(g, dirs)
                else:   
                    if g == 1: ambushPlayer(g, dirs)
                    if g == 3: ambushPlayer(g, dirs)
        
        if dirs[ghosts[g].dir] == 0 or randint(0,50) == 0:#방향이 오른쪽이거나 randint(0,50) = 0이나왔을때
            d = -1 #아래
            while d == -1: # d = -1일때 
                rd = randint(0,3)
                if aboveCentre(ghosts[g]) and rd == 1: #유령이 시작박스에 있고 rd가 1일때 
                    rd = 0
                if dirs[rd] == 1: #방향이 rd일때
                    d = rd 
            ghosts[g].dir = d

        animate(ghosts[g], pos=(ghosts[g].x + dmoves[ghosts[g].dir][0]*20, ghosts[g].y + dmoves[ghosts[g].dir][1]*20), duration=1/GHOSTSPEED, tween='linear', on_finished=flagMoveGhosts)

def runAway(g, dirs): #도망(전체해당)
    d = ghosts[g].dir
    
    if player.x > ghosts[g].x and dirs[0] == 1: ghosts[g].dir = 2 #플레이어가 유령보다 오른쪽에 있고 유령의 방향이 오른쪽일때 -> 유령 방향 왼쪽
    if player.x < ghosts[g].x and dirs[2] == 1: ghosts[g].dir = 0 #플레이어가 유령보다 왼쪽에 있고 유령의 방향이 왼쪽일때 -> 유령의 방향은 오른쪽
    
    if player.y > ghosts[g].y and dirs[1] == 1: ghosts[g].dir = 3 #플레이어가 유령보다 아래에 있고 유령의 방향이 아래쪽일때-> 유령의 방향은 위
    if player.y < ghosts[g].y and dirs[3] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1 #플레이어가 유령보다 위에 있고 유령의 방향이 위쪽이고 시작박스안에 없을때-> 유령의 방향은 아래


def followPlayer(g, dirs):#플레이어 추격자(ghost[0],ghost[2])
    d = ghosts[g].dir
    if d == 1 or d == 3: #유령방향이 아래 또는 위일때
        if player.x > ghosts[g].x and dirs[0] == 1: ghosts[g].dir = 0 #플레이어가 유령보다 오른쪽에 있고 유령의 방향이 오른쪽일때 -> 유령 방향 오른쪽
        if player.x < ghosts[g].x and dirs[2] == 1: ghosts[g].dir = 2 #플레이어가 유령보다 왼쪽에 있고 유령의 방향이 왼쪽일때 -> 유령의 방향은 왼쪽
    if d == 0 or d == 2: #방향이 오른쪽 또는 왼쪽일때
        if player.y > ghosts[g].y and dirs[1] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1 #플레이어가 유령보다 아래에 있고 유령의 방향이 아래쪽이고 시작박스에 없을때-> 유령의 방향은 아래
        if player.y < ghosts[g].y and dirs[3] == 1: ghosts[g].dir = 3 #플레이어가 유령보다 위에 있고 유령의 방향이 위쪽일때 -> 유령의 방향은 위

def ambushPlayer(g, dirs):#플레이어 매복자(ghost[1],ghost[3])
    d = ghosts[g].dir
    # area1
    if player.x < 300 and player.y < 360 and not aboveCentre(ghosts[g]):
        if ghosts[g].x > 300 and ghosts[g].y > 360 and dirs[2] == 1:
            ghosts[g].dir = 2
        if ghosts[g].x > 300 and ghosts[g].y < 360 and dirs[2] == 1:
            ghosts[g].dir = 2
        if ghosts[g].y > 360 and ghosts[g].x < 300 and dirs[3] == 1:
            ghosts[g].dir = 3
    # area2
    elif player.x > 300 and player.y < 360 and not aboveCentre(ghosts[g]):
        if ghosts[g].x < 300 and ghosts[g].y > 360 and dirs[0] == 1:
            ghosts[g].dir = 0
        if ghosts[g].x < 300 and ghosts[g].y < 360 and dirs[0] == 1:
            ghosts[g].dir = 0
        if ghosts[g].y > 360 and ghosts[g].x > 300 and dirs[3] == 1:
            ghosts[g].dir = 3
    # area3
    elif player.x < 300 and player.y > 360 and not aboveCentre(ghosts[g]):
        if ghosts[g].x > 300 and ghosts[g].y < 360 and dirs[2] == 1:
            ghosts[g].dir = 2
        if ghosts[g].x > 300 and ghosts[g].y > 360 and dirs[2] == 1:
            ghosts[g].dir = 2
        if ghosts[g].y < 360 and ghosts[g].x < 300 and dirs[1] == 1:
            ghosts[g].dir = 1
    # area4
    elif player.x > 300 and player.y > 360 and not aboveCentre(ghosts[g]):
        if ghosts[g].x < 300 and ghosts[g].y < 360 and dirs[0] == 1:
            ghosts[g].dir = 0
        if ghosts[g].x < 300 and ghosts[g].y > 360 and dirs[0] == 1:
            ghosts[g].dir = 0
        if ghosts[g].y < 360 and ghosts[g].x > 300 and dirs[1] == 1:
            ghosts[g].dir = 1
    else:
        if player.movex > 0 and dirs[0] == 1: ghosts[g].dir = 0 #플레이어가 오른쪽 방향으로 움직이고 유령방향이 오른쪽일때 -> 유령의 방향은 오른쪽
        if player.movex < 0 and dirs[2] == 1: ghosts[g].dir = 2 #플레이어가 왼쪽 방향을 움직이고 유령의 방향이 왼쪽일때 -> 유령의 방향은 왼쪽
        if player.movey > 0 and dirs[1] == 1 and not aboveCentre(ghosts[g]): ghosts[g].dir = 1 #플레이어가 아래쪽으로 움직이고 유령의 방향이 아래쪽이고 시작박스에 없을때 -> 유령의 방향은 아래쪽
        if player.movey < 0 and dirs[3] == 1: ghosts[g].dir = 3 #플레이어가 위쪽으로 움직이고 유령의 방향이 위쪽일때 -> 유령의 방향은 위쪽

def inTheCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 320 and ga.y < 420:
        return True
    return False

def aboveCentre(ga):
    if ga.x > 220 and ga.x < 380 and ga.y > 300 and ga.y < 320:
        return True
    return False

def flagMoveGhosts():
    global moveGhostsFlag
    moveGhostsFlag += 1

def ghostCollided(ga,gn):
    for g in range(len(ghosts)):
        if ghosts[g].colliderect(ga) and g != gn:
            return True
    return False
    
def initDots():
    global pacDots
    pacDots = []
    a = x = 0
    while x < 30:
        y = 0
        while y < 29:
            d = gamemaps.checkDotPoint(10+x*20, 10+y*20)
            if d == 1:
                pacDots.append(Actor("dot",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                pacDots[a].type = 1
                a += 1
            if d == 2:
                pacDots.append(Actor("power",(10+x*20, 90+y*20)))
                pacDots[a].status = 0
                pacDots[a].type = 2
                a += 1
            y += 1
        x += 1

def initGhosts():
    global ghosts, moveGhostsFlag
    moveGhostsFlag = 4
    ghosts = []
    g = 0
    while g < 4:
        ghosts.append(Actor("ghost"+str(g+1),(270+(g*20), 370)))
        ghosts[g].dir = randint(0, 3)
        ghosts[g].status = 0
        g += 1

def inputLock():
    global player
    player.inputActive = False

def inputUnLock():
    global player
    player.movex = player.movey = 0
    player.inputActive = True
    
init()
pgzrun.go()
