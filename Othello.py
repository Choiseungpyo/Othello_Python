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
RED = (255,0,0)
YELLOW = (255,204,51)

screen = pygame.display.set_mode((600,400), 0,32)
pygame.display.set_caption("Othello")


#화면 세팅
screen.fill(GREEN)

#가로 줄 긋기
for x in range(0, 8):
    if x==0:
        continue
    else:    
        pygame.draw.line(screen, BLACK, [0,x*50],[400,x*50],5)

#세로 줄 긋기
for y in range(0,9):
    if y==0:
        continue
    else:    
        pygame.draw.line(screen, BLACK, [y*50,0],[y*50,400],5)

#오른쪽에 상태창 만들기
pygame.draw.rect(screen, WHITE, [403,0,200,400])


#각 위치에서의 블럭값들 초기화
screenArr = [] #리스트 안에 리스트. 열을 나누기 위함.

for y in range(0,SCREEN):
    colList =[]
    for x in range(0,SCREEN):
        colList.append(0)

    screenArr.append(colList)


screenArr[3][3]=2
screenArr[3][4]=1
screenArr[4][3]=1
screenArr[4][4]=2

#변수
currentTurn =1 #현재 턴- 플레이어 :1 컴퓨터 :2



diagnoalScreenArr =[] #대각선 검사를 위한 변수, 3차원 배열

for i in range(0,4):
    rowList =[]
    for y in range(0,SCREEN):
        colList =[]
        for x in range(0,SCREEN):
            colList.append(0)

        rowList.append(colList)
    
    diagnoalScreenArr.append(rowList)



#함수
def changeTurn(pTurn):
    if pTurn ==1: #플레이어의 턴을 컴퓨터의 턴으로 전환
        return 2
    elif pTurn ==2:
        return 1
    else:
        return -1 #오류인 경우

    
def changeArrxToX(arrx): #x, y를 arrx, arry로 바꿔서 리턴.
    for x in range(0,SCREEN):
        if arrx==x:
            return 25*(arrx*2+1)

        
def changeArryToY(arry):
    for y in range(0,SCREEN):
        if arry ==y:
            return 25*(arry*2+1)


def viewGameScreen(): #screen이 해당 값들을 가지면 해당 블럭 출력
    for arry in range(0,SCREEN):
        for arrx in range(0,SCREEN):
            if screenArr[arry][arrx] ==1: #플레이어
                pygame.draw.circle(screen, BLACK, [changeArrxToX(arrx),changeArryToY(arry)], 20)
            elif screenArr[arry][arrx] ==2: #컴퓨터
                pygame.draw.circle(screen, WHITE, [changeArrxToX(arrx),changeArryToY(arry)], 20)
            elif screenArr[arry][arrx] ==3: #컴퓨터이 블럭 랜덤위치
                pygame.draw.circle(screen, BLUE, [changeArrxToX(arrx),changeArryToY(arry)], 20)

def changeMousePosXToArrx(mousePosX):
    for i in range(0,SCREEN):
        if mousePosX < 50 * (i+1) -5 and mousePosX > 50*i +5:          
            return i
    else:
        return -1 #오류일 경우


def changeMousePosYToArry(mousePosY):
    for i in range(0,SCREEN):
        if mousePosY < 50 * (i+1) -5 and mousePosY > 50*i +5: #경계 안쪽        
            return i
    else: #화면의 검은색 경계 부분
        return -1 #오류일 경우


def checkIfTherisBlock(pScreenArr): #해당 자리에 블럭이 현재 있는지 없는지
    #iScreenArr : screenArr을 매개변수로 받아야하는데 헷갈릴까봐
    #parameter에서 p를 따옴
    if pScreenArr == 1 or pScreenArr ==2: #플레이어 또는 컴퓨터의 블럭
        return 1 #블럭이 이미 있음을 리턴
    else:
        return 0 #블럭이 해당자리에 없음을 리턴


def setDiagonalCnt(): #대각선 검사를 위해 미리 대각선 개수 설정
    
    #왼쪽 위 방향 대각선
    diagonalDir =0
    
    for row in range(0,SCREEN):
        for col in range(7, row-1,-1):
            diagnoalScreenArr[diagonalDir][row][col]=row
            
        remainingCol = row
        num =0

        for col in range(0, remainingCol):
            diagnoalScreenArr[diagonalDir][row][col] = num
            num=num+1

    #오른쪽 위 방향 대각선
    diagonalDir =1
    
    for row in range(0,SCREEN):
        for col in range(0, SCREEN-row):
            diagnoalScreenArr[diagonalDir][row][col]=row

        remainingCol = 7 -row
        num =row

        for col in range(remainingCol, SCREEN):
            diagnoalScreenArr[diagonalDir][row][col] = num
            num = num-1

    #왼쪽 아래 방향 대각선
    diagonalDir =2

    for row in range(7, -1, -1):
        for col in range(7, 6-row, -1):
            diagnoalScreenArr[diagonalDir][row][col] = 7-row

        remainingCol = 7-row
        num =0

        for col in range(0, remainingCol):
            diagnoalScreenArr[diagonalDir][row][col] = num
            num = num+1

    #오른쪽 아래 대각선 개수
    diagonalDir =3

    for row in range(7, -1, -1):
        for col in range(0, 1+row):
            diagnoalScreenArr[diagonalDir][row][col] =7-row

        remainingCol = row+1
        num = 6-row

        for col in range(remainingCol, SCREEN):
            diagnoalScreenArr[diagonalDir][row][col] = num
            num = num-1


#setDiagonalCnt()함수 시각적 확인 
##setDiagonalCnt()
##for x in range(0,8):
##    print(diagnoalScreenArr[0][x])


def InspectIfItCanBePlacedInPlace(pArrx, pArry, changeValue, pCurrentTurn): #해당 위치에 블럭을 놓을 수 있는 자리인지 검사
    returnValue=0
    
    if 1==checkIfTherisBlock(screenArr[pArry][pArrx]):
        return 0

    #대각선 검사
    for diagonalValue in range(0,4):
        if diagnoalScreenArr[diagonalValue][pArry][pArrx] != 0:
            
            if diagonalValue==0: #왼쪽 위방향
                if screenArr[pArry-1][pArrx-1] == changeTurn(pCurrentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry-a][pArrx-a]==0:
                            break
                        elif screenArr[pArry-a][pArrx-a] ==pCurrentTurn:                        
                            for b in range(1, a):
                                if changeValue ==True:
                                    screenArr[pArry-b][pArrx-b] =pCurrentTurn
                            returnValue =1
                            break

            if diagonalValue ==1: #오른쪽 위 방향
                if screenArr[pArry-1][pArrx+1] == changeTurn(pCurrentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry-a][pArrx+a]==0:
                            break
                        elif screenArr[pArry-a][pArrx+a]==pCurrentTurn:                        
                            for b in range(1, a):
                                if changeValue ==True:
                                    screenArr[pArry-b][pArrx+b]=pCurrentTurn
                            returnValue =1
                            break

            if diagonalValue ==2: #왼쪽 아래 방향
                if screenArr[pArry+1][pArrx-1] == changeTurn(pCurrentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry+a][pArrx-a]==0:
                            break
                        elif screenArr[pArry+a][pArrx-a]==pCurrentTurn:                         
                            for b in range(1, a):
                                if changeValue ==True:
                                    screenArr[pArry+b][pArrx-b]=pCurrentTurn
                            returnValue =1
                            break

            if diagonalValue ==3: #오른쪽 아래 방향
                if screenArr[pArry+1][pArrx+1] == changeTurn(pCurrentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry+a][pArrx+a]==0:
                            break
                        elif screenArr[pArry+a][pArrx+a]==pCurrentTurn:                        
                            for b in range(1, a):
                                if changeValue ==True:
                                    screenArr[pArry+b][pArrx+b]=pCurrentTurn
                            returnValue =1
                            break
                        
    #행 검사 - 위 방향으로 검사
    if pArry != 0: #pArry가 0이면 검사할 때 리스트 인덱스 넘어감
        if screenArr[pArry-1][pArrx] == changeTurn(pCurrentTurn):
            for a in range(pArry-1, -1, -1):
                if screenArr[a][pArrx] ==0:
                    break
                elif screenArr[a][pArrx] ==pCurrentTurn:
                    for b in range(pArry-1, a,-1):
                        if changeValue ==True:
                            screenArr[b][pArrx] =pCurrentTurn
                    returnValue =1
                    break
                        
    #행 검사 - 아래  방향으로 검사
    if pArry != SCREEN-1:
        if screenArr[pArry+1][pArrx] == changeTurn(pCurrentTurn):
            for a in range(pArry+1, SCREEN):
                if screenArr[a][pArrx] ==0:
                    break
                elif screenArr[a][pArrx]==pCurrentTurn:
                    for b in range(pArry+1, a):
                        if changeValue ==True:
                            screenArr[b][pArrx]=pCurrentTurn
                    returnValue =1
                    break
                    
                        
    #열 검사 - 왼쪽 방향으로 검사
    if pArrx !=0:
        if screenArr[pArry][pArrx-1] == changeTurn(pCurrentTurn):
            for a in range(pArrx-1, -1,-1):
                if screenArr[pArry][a] ==0:
                    break
                elif screenArr[pArry][a] ==pCurrentTurn:
                    for b in range(pArrx-1, a, -1):
                        if changeValue ==True:
                            screenArr[pArry][b] =pCurrentTurn
                    returnValue =1
                    break

                        
    #열 검사 - 오른쪽 방향으로 검사
    if pArrx != SCREEN-1:
        if screenArr[pArry][pArrx+1] == changeTurn(pCurrentTurn):
            for a in range(pArrx+1, SCREEN):
                if screenArr[pArry][a] ==0:
                    break
                elif screenArr[pArry][a] ==pCurrentTurn:
                    for b in range(pArrx+1, a):
                        if changeValue ==True:
                            screenArr[pArry][b] =pCurrentTurn
                    returnValue =1
                    break

                    
    return returnValue #놓을 수 있는 곳이  없을 경우:0   있을 경우 :1


def calculateComputerRandomPlace(randomComputerNum): #컴퓨터가 놓는 위치 랜덤으로 계산
    randNum=0
    randNum = random.randrange(1, randomComputerNum+1)
    return randNum
    

def setWhereComputerCanPutBlock():
    randomComputerNum =1
    tmpRow=-1
    tmpCol=-1
    noMeaningStorage=0
    computerRandomPlace =[]

    #computerRandomPlace 모두 0으로 초기화(8x8 2차원 배열)
    for y in range(0,SCREEN):
        colList =[]
        for x in range(0,SCREEN):
            colList.append(0)

        computerRandomPlace.append(colList)
    
    for row in range(0, SCREEN):
        for col in range(0,SCREEN):
            if InspectIfItCanBePlacedInPlace(col, row, False, currentTurn) ==1:
                computerRandomPlace[row][col] = randomComputerNum
                randomComputerNum = randomComputerNum +1
                       
    randomComputerNum = calculateComputerRandomPlace(randomComputerNum-1) #-1하는 이유 맨 마지막에 +1돼서 끝나기 때문
    
    for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            if computerRandomPlace[row][col] == randomComputerNum:
                screenArr[row][col] =3 #컴퓨터가 랜덤으로 놓을위치 파랑색으로 설정
                tmpRow = row
                tmpCol = col

    #컴퓨터가 랜덤으로 놓을 위치 미리 보여주기  
    viewGameScreen()
    pygame.display.update()
    
    #해당 위치 원래 컴퓨터 블럭색으로 변경
    time.sleep(2)
    noMeaningStorage = InspectIfItCanBePlacedInPlace(tmpCol, tmpRow, True, currentTurn)
    screenArr[tmpRow][tmpCol] = 2 #컴퓨터가 랜덤으로 놓을위치 원래색인 하얀색으로 변경
    
    viewGameScreen()
    pygame.display.update()


def moveNextTurn(): #둘 곳이 없을 경우 다음턴으로 넘어간다.
    global currentTurn
    global isClick
    cannotPutPlaceCnt =0
    
    for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            if screenArr[row][col] == 0:
                if InspectIfItCanBePlacedInPlace(col,row,False, currentTurn)==1:
                    cannotPutPlaceCnt = cannotPutPlaceCnt+1
                    
    if cannotPutPlaceCnt ==0 :
        currentTurn = changeTurn(currentTurn)
        print(currentTurn,"의 유저가 놓을 곳이 없습니다. ")
        clearStateScreen(False)
        printTurnInformation() #플레이어 -> 컴퓨터 턴 : 컴퓨터 턴 출력
        time.sleep(1)


def viewGameResult():
    font = pygame.font.SysFont("arial",20,True)
    playerBlockCnt =0
    computerBlockCnt =0

    for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            if screenArr[row][col] ==1:
                playerBlockCnt = playerBlockCnt+1
            elif screenArr[row][col] ==2:
                computerBlockCnt = computerBlockCnt+1
                
    tmpBlockCnt =0

    for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            if tmpBlockCnt < playerBlockCnt:
                screenArr[row][col] =1
                tmpBlockCnt = tmpBlockCnt+1
            else:
                screenArr[row][col] =2
                
    print("컴퓨터 블럭 개수 : ", computerBlockCnt)
    print("플레이어 블럭 개수 : ", playerBlockCnt)

    if computerBlockCnt < playerBlockCnt:
        print("플레이어 승리")
    elif computerBlockCnt > playerBlockCnt:
        print("컴퓨터 승리")
    else: #동점
        print("무승부")

    clearStateScreen(True)
    
    if computerBlockCnt < playerBlockCnt:
        printWinner("Player")
    elif computerBlockCnt > playerBlockCnt:
        printWinner("Computer")
    else: #동점
        printWinner("Draw")
    
    viewGameScreen()
    printBlockCnt(playerBlockCnt, computerBlockCnt)
    pygame.display.update()
    print("개수 출력화면까지 끝")
    time.sleep(3)
    sys.exit()
                

def ifNoOneDoNotPutBlock():
    enablePutBlock= [True,True]
    
    for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            #플레이어 검사와 검퓨터 모두 블럭을 둘 곳이 없을 경우
            if 1==InspectIfItCanBePlacedInPlace(col,row,False,1):
                #print("플레이어 : (",row,col,") : 0")
                enablePutBlock[0] = False
            if 1==InspectIfItCanBePlacedInPlace(col,row,False,2):
                #print("컴퓨터   : (",row,col,") : 0")
                enablePutBlock[1] = False
                

    if enablePutBlock[0] ==True and enablePutBlock[1] ==True:
        return True
    else:
        return False
    

def checkGameOver():
    spaceFilledCnt =0
    
    for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            if screenArr[row][col] ==1 or screenArr[row][col] ==2:
                spaceFilledCnt= spaceFilledCnt+1
                
    
    if spaceFilledCnt == SCREEN * SCREEN or ifNoOneDoNotPutBlock() == True:              
        clearStateScreen(True)
        printGameOverText()
        printCalculateGameResult()
        time.sleep(5) #결과 집계중 5초동안 띄운 뒤 결과 보여주기
        viewGameResult()


def printTurn(pTurn):
    if pTurn ==1:
        return "Player"
    elif pTurn ==2:
        return "Computer"
    else:
        return "Error"
    

def clearStateScreen(isGameOver):
    clearScreenScaleY =80
    
    if isGameOver == True:
        clearScreenScaleY = 400
        print("sclearScreenScaleY =400")
    
    pygame.draw.rect(screen, WHITE, [403,0,200,clearScreenScaleY])
    pygame.display.update()


def printTurnInformation():
    userTextFont = pygame.font.SysFont("arial",20, True)
    userTextContentFont = pygame.font.SysFont("arial",20)
    
    userText = userTextFont.render("Current Turn : ", True, BLACK)
    userTextContent = userTextContentFont.render(printTurn(currentTurn), True, BLACK)
    
    screen.blit(userText, (410,100))
    screen.blit(userTextContent, (525,100))
    pygame.display.update()


def printUserColorInformation():
    font = pygame.font.SysFont("arial",20,True)
    playerColor = font.render("Player Color : ", True, BLACK)
    computerColor = font.render("Computer Color : ", True, BLACK)
    
    screen.blit(playerColor, (410,150))
    screen.blit(computerColor, (410,200))

    pygame.draw.rect(screen, GREEN, (548, 148, 30, 30))
    pygame.draw.circle(screen, BLACK, [563, 163], 10) 
    pygame.draw.rect(screen, GREEN, (548, 198, 30, 30))
    pygame.draw.circle(screen, WHITE, [563, 213], 10)
    
    pygame.display.update()


def printGameOverText():
    font = pygame.font.SysFont("arial",30,True)
    text = font.render("-Game Over-", True, RED)
    
    screen.blit(text, (425,50))
    pygame.display.update()


def printCalculateGameResult(): #게임 결과 계산중 이라고 출력
    font = pygame.font.SysFont("arial",15)
    text = font.render("~Calculating Game Result~", True, BLACK)
    
    screen.blit(text, (425,100))
    pygame.display.update()


def printWinner(winner):
    
    winnerFont = pygame.font.SysFont("arial",40)
    winnerContentFont = pygame.font.SysFont("arial",30)
    
    winnerText = winnerFont.render("Winner", True, RED)
    winnerContentText = winnerContentFont.render("-"+winner+"-", True, YELLOW)
    
    screen.blit(winnerText, (450,50))
    screen.blit(winnerContentText, (440,100))
    pygame.display.update()



def printBlockCnt(playerBlockCnt, computerBlockCnt):
    font = pygame.font.SysFont("arial",20)
    
    playerBlockCntText = font.render("Player Block : "+ str(playerBlockCnt), True, BLACK)
    computerBlockCntText = font.render("Computer Block : " + str(computerBlockCnt), True, BLACK)
    
    screen.blit(playerBlockCntText, (450,200))
    screen.blit(computerBlockCntText, (440,225))
    pygame.display.update()







#둘다 블럭을  놓을 수 없는 경우
##for row in range(0,SCREEN):
##        for col in range(0,SCREEN):
##            screenArr[row][col] =2
##screenArr[2][6] =1
##screenArr[2][2] =1
##screenArr[3][3] =1
##screenArr[4][4] =1
##screenArr[4][6] =1
##screenArr[5][5] =1
##screenArr[7][7] =1
##screenArr[6][7] =0

for row in range(0,SCREEN):
        for col in range(0,SCREEN):
            screenArr[row][col] =2
screenArr[0][0] =1

setDiagonalCnt()
viewGameScreen()
printTurnInformation()
printUserColorInformation()


#Game Loop
while True:   
    checkGameOver()
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            tmpMousePos = []
            tmpMousePos.append(changeMousePosXToArrx(pygame.mouse.get_pos()[0]))
            tmpMousePos.append(changeMousePosYToArry(pygame.mouse.get_pos()[1]))
    
            if not(tmpMousePos[0] ==-1 or tmpMousePos[1] ==-1):
                if InspectIfItCanBePlacedInPlace(tmpMousePos[0],tmpMousePos[1], True, currentTurn) ==1:
                    mousePos = pygame.mouse.get_pos() #자료형 : tuple
                    screenArr[changeMousePosYToArry(mousePos[1])][changeMousePosXToArrx(mousePos[0])] =1 #클릭한 곳 색깔 바꾸기    
                    currentTurn = changeTurn(currentTurn) #턴 바꾸기
                    clearStateScreen(False)
                    printTurnInformation() #플레이어 -> 컴퓨터 턴 : 컴퓨터 턴 출력
                    
                    
    moveNextTurn()
    
    viewGameScreen()
    pygame.display.update()
    
    if currentTurn ==2 :
        time.sleep(2)
        setWhereComputerCanPutBlock()
        currentTurn = changeTurn(currentTurn)
        clearStateScreen(False)
        printTurnInformation() #컴퓨터 -> 플레이어 턴 : 컴퓨터 턴 출력
       
















