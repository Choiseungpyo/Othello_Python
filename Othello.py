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



screen = pygame.display.set_mode((400,400), 0,32)
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
for y in range(0,8):
    if y==0:
        continue
    else:    
        pygame.draw.line(screen, BLACK, [y*50,0],[y*50,400],5)



#각 위치에서의 블럭값들 초기화
screenArr = [] #리스트 안에 리스트. 열을 나누기 위함.

for y in range(0,SCREEN):
    colList =[]
    for x in range(0,SCREEN):
        colList.append(0)

    screenArr.append(colList)


        
screenArr[3][3]=1
screenArr[3][4]=2
screenArr[4][3]=2
screenArr[4][4]=1



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


def InspectIfItCanBePlacedInPlace(pArrx, pArry, changeValue): #해당 위치에 블럭을 놓을 수 있는 자리인지 검사
    returnValue=0

    print("현재 턴 :", currentTurn)
    
    if 1==checkIfTherisBlock(screenArr[pArry][pArrx]):
        return 0

    #print("현재 위치에는 아무것도 놓여있지 않다")

    #대각선 검사
    for diagonalValue in range(0,4):
        if diagnoalScreenArr[diagonalValue][pArry][pArrx] != 0:
            
            if diagonalValue==0: #왼쪽 위방향
                if screenArr[pArry-1][pArrx-1] == changeTurn(currentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry-a][pArrx-a]==0:
                            break
                        elif screenArr[pArry-a][pArrx-a] ==currentTurn:
                            for b in range(1, a):
                                if changeValue ==True:
                                    print("왼쪽 위 방향 변경")
                                    screenArr[pArry-b][pArrx-b] =currentTurn
                                returnValue =1

            if diagonalValue ==1: #오른쪽 위 방향
                if screenArr[pArry-1][pArrx+1] == changeTurn(currentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry-a][pArrx+a]==0:
                            break
                        elif screenArr[pArry-a][pArrx+a]==currentTurn:
                            for b in range(1, a):
                                if changeValue ==True:
                                    print("오른쪽 위 방향 변경")
                                    screenArr[pArry-b][pArrx+b]=currentTurn
                                returnValue =1

            if diagonalValue ==2: #왼쪽 아래 방향
                if screenArr[pArry+1][pArrx-1] == changeTurn(currentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry+a][pArrx-a]==0:
                            break
                        elif screenArr[pArry+a][pArrx-a]==currentTurn:
                            for b in range(1, a):
                                if changeValue ==True:
                                    print("왼쪽 아래 방향 변경")
                                    screenArr[pArry+b][pArrx-b]=currentTurn
                                returnValue =1

            if diagonalValue ==3: #오른쪽 아래 방향
                if screenArr[pArry+1][pArrx+1] == changeTurn(currentTurn):
                    for a in range(1, diagnoalScreenArr[diagonalValue][pArry][pArrx]+1):
                        if screenArr[pArry+a][pArrx+a]==0:
                            break
                        elif screenArr[pArry+a][pArrx+a]==currentTurn:
                            for b in range(1, a):
                                if changeValue ==True:
                                    print("오른쪽 아래 방향 변경")
                                    screenArr[pArry+b][pArrx+b]=currentTurn
                                returnValue =1
                        
    #행 검사 - 위 방향으로 검사
    if pArry != 0: #pArry가 0이면 검사할 때 리스트 인덱스 넘어감
        if screenArr[pArry-1][pArrx] == changeTurn(currentTurn):
            for a in range(pArry-1, -1, -1):
                if screenArr[a][pArrx] ==0:
                    break
                elif screenArr[a][pArrx] ==currentTurn:
                    for b in range(pArry-1, a,-1):
                        if changeValue ==True:
                            print("행  위 방향 변경")
                            screenArr[b][pArrx] =currentTurn
                        returnValue =1
                        
    #행 검사 - 아래  방향으로 검사
    if pArry != SCREEN-1:
        if screenArr[pArry+1][pArrx] == changeTurn(currentTurn):
            for a in range(pArry+1, SCREEN):
                if screenArr[a][pArrx] ==0:
                    break
                elif screenArr[a][pArrx]==currentTurn:
                    for b in range(pArry+1, a):
                        if changeValue ==True:
                            print("행 아래 방향 변경")
                            screenArr[b][pArrx]=currentTurn
                        returnValue =1
                    
                        
    #열 검사 - 왼쪽 방향으로 검사
    if pArrx !=0:
        if screenArr[pArry][pArrx-1] == changeTurn(currentTurn):
            for a in range(pArrx-1, -1,-1):
                if screenArr[pArry][a] ==0:
                    break
                elif screenArr[pArry][a] ==currentTurn:
                    for b in range(pArrx-1, a, -1):
                        if changeValue ==True:
                            print("열 왼쪽 방향 변경")
                            screenArr[pArry][b] =currentTurn
                        returnValue =1

                        
    #열 검사 - 오른쪽 방향으로 검사
    if pArrx != SCREEN-1:
        if screenArr[pArry][pArrx+1] == changeTurn(currentTurn):
            for a in range(pArrx+1, SCREEN):
                if screenArr[pArry][a] ==0:
                    break
                elif screenArr[pArry][a] ==currentTurn:
                    for b in range(pArrx+1, a):
                        if changeValue ==True:
                            print("열 오른쪽 방향 변경")
                            screenArr[pArry][b] =currentTurn
                        returnValue =1

                    
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

    #computerRandomPlace 모두 0으로 초기화(8x8 2차원 배)
    for y in range(0,SCREEN):
        colList =[]
        for x in range(0,SCREEN):
            colList.append(0)

        computerRandomPlace.append(colList)
    
    for row in range(0, SCREEN):
        for col in range(0,SCREEN):
            if InspectIfItCanBePlacedInPlace(col, row, False) ==1:
                computerRandomPlace[row][col] = randomComputerNum
                randomComputerNum = randomComputerNum +1
        
        print(computerRandomPlace[row])
        
    randomComputerNum = calculateComputerRandomPlace(randomComputerNum)
    print()
    print()
    
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
    noMeaningStorage = InspectIfItCanBePlacedInPlace(tmpCol, tmpRow, True)
    screenArr[tmpRow][tmpCol] = 2 #컴퓨터가 랜덤으로 놓을위치 원래색인 하얀색으로 변경
    
    viewGameScreen()
    pygame.display.update()

    

                









ComputerControl = False

setDiagonalCnt()
viewGameScreen()


#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:           
            print("마우스클릭")
           
            tmpMousePos = []
            tmpMousePos.append(changeMousePosXToArrx(pygame.mouse.get_pos()[0]))
            tmpMousePos.append(changeMousePosYToArry(pygame.mouse.get_pos()[1]))
            print(currentTurn)
            if not(tmpMousePos[0] ==-1 or tmpMousePos[1] ==-1):
                if InspectIfItCanBePlacedInPlace(tmpMousePos[0],tmpMousePos[1], True) ==1: 
                    mousePos = pygame.mouse.get_pos() #자료형 : tuple
                    screenArr[changeMousePosYToArry(mousePos[1])][changeMousePosXToArrx(mousePos[0])] =1 #클릭한 곳 색깔 바꾸기
                    #print(mousePos)     
                    currentTurn = changeTurn(currentTurn) #턴 바꾸기
                    controlComputerTurn = True
                    print("****************************")
                    time.sleep(2)
    
    viewGameScreen()
    pygame.display.update()
    if currentTurn ==2 and controlComputerTurn ==True:
        print("컴퓨터 턴 시작!!!!!!!!!!!")
        setWhereComputerCanPutBlock()
        print("컴퓨터 턴 끝!!!!!!!!!!!!!")
        #print(currentTurn)
        currentTurn = changeTurn(currentTurn)
        controlComputerTurn = False
        
















