import pygame, sys #기본세팅
import random, time #내가 추가한 것
from pygame.locals import *

#Set up pygame.
pygame.init()

#상수 정의
SCREEN =8

BLACK = (0,0,0)
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
PURPLE = (125,0,255)
RED = (255,0,0)
YELLOW = (255,204,51)

screen = pygame.display.set_mode((600,400), 0,32)
pygame.display.set_caption("OthelloStartScreen")


#변수

#클릭 좌표 검사를 위한 변수
# [[x최소, x최대],[y최소, y최대]]
gameStartPos = [[210, 377],[200, 245]] 
gameRulePos = [[210, 375],[300, 345]]
goBackPos = [[550,590],[365,390]]

#클릭했는지 확인하는 변수
clickGameStart = False
clickGameRule = False
isStartScreen = True

#화면 세팅
screen.fill(WHITE)




#함수
def checkGameStartPos(mousePosX, mousePosY, pos):
    
    if mousePosX >=pos[0][0] and mousePosX <=pos[0][1]:
        if mousePosY>=pos[1][0] and mousePosY <=pos[1][1]:
            return True
    return False


def setStartScreen():
    # 오셀로 Text 띄우기
    font = pygame.font.SysFont("arial", 80)
    text = font.render("Othello", True, WHITE, GREEN)
    screen.blit(text, (190,50))

    #게임 시작 Text 띄우기
    font = pygame.font.SysFont("arial", 40)
    text = font.render("Game Start", True, WHITE, GREEN)
    screen.blit(text, (gameStartPos[0][0],gameStartPos[1][0])) 

    #게임 규칙 Text 띄우기
    text = font.render("Game Rule", True, WHITE, GREEN)
    screen.blit(text, (gameRulePos[0][0],gameRulePos[1][0]))


def setGameRuleScreen():
    screen.fill(WHITE)
    gameRuleText = [["1. The way you play : Mouse"],
                    ["2. Opponent : Computer"],
                    ["3. If more blocks are flipped over than", "the opponnent, you win."]]
    
    # 게임 규칙 Text 띄우기
    font = pygame.font.SysFont("arial", 50)
    text = font.render("Game Rule", True, BLACK, PURPLE)
    screen.blit(text, (190,25))

    #내용을 둘러싸는 직사각형
    pygame.draw.rect(screen, PURPLE, [20,120,560,230],2)
    
    #게임 규칙 내용 Text 띄우기
    yInterval = 0;
    xInterval = 0;
    for x in range(3):
        for i in range(len(gameRuleText[x])):
            if i ==1:
                # If more blocks are flipped over than"을 입력 후 그 밑에 줄에 "the opponnent, you win.을 간격맞춰서 입력하기 위함.
                xInterval = 50 
            font = pygame.font.SysFont("arial", 30)
            text = font.render(gameRuleText[x][i], True, BLACK)
            screen.blit(text, (50+xInterval,125 + yInterval))
            yInterval = yInterval + 50

    #오른쪽 하단에 되돌아가기 버튼 만들기.
    pygame.draw.rect(screen, BLACK, [570, 375, 20,5])
    pygame.draw.polygon(screen, BLACK, [(550,377),(570,365),(570,390)])
    
def clearStartScreen():
    pygame.draw.rect(screen, WHITE, [0,0,600,400])
    pygame.display.update()


        
setStartScreen()



#Game Loop
while True:   
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = []
            mousePos.append(pygame.mouse.get_pos()[0])
            mousePos.append(pygame.mouse.get_pos()[1])

            if isStartScreen == True: #시작 화면에서만 동작
                if checkGameStartPos(mousePos[0], mousePos[1], gameStartPos) == True:
                    print("게임 시작 클릭")
                    # 게임 플레이 화면으로 넘어가기
                    # 게임플레이를 눌렀는지 검사하는 변수 필요.
                    clickGameStart = True
                    isStartScreen = False
                    
                elif checkGameStartPos(mousePos[0], mousePos[1], gameRulePos) == True:
                    print("게임 룰 클릭")
                    # 게임 룰 화면으로 넘어가기
                    # 게임 룰을 눌렀는지 검사하는 변수 필요.
                    clickGameRule = True
                    isStartScreen = False
                    clearStartScreen()
                    setGameRuleScreen()
                    
            else: #시작화면이 아닐때에만 동작
##                if clickGameStart == True: #게임 플레이 중에만 동작함.
##                    #이후 좌표 검사 ~
                if clickGameRule == True: #게임 규칙을 보는 중에만 동작함.
                    print("게임 룰 스크린 출력")
                    if checkGameStartPos(mousePos[0], mousePos[1], goBackPos) == True:
                        clickGameRule = False
                        isStartScreen = True
                        clearStartScreen()
                        setStartScreen()
                        
            
    pygame.display.update()
    














