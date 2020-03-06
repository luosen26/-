from tkinter import *
from tkinter.messagebox import *
import random

root = Tk('黑白棋2019')
root.title(" 黑白棋--罗森2019-9-14")
# 加载图片
imgs= [PhotoImage(file='black.png'), PhotoImage(file='white.png'),PhotoImage(file='board.png'),PhotoImage(file='info2.png')]

# 重置棋盘
def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = 'none'
    # Starting pieces:
    board[3][3] = 'black'
    board[3][4] = 'white'
    board[4][3] = 'white'
    board[4][4] = 'black'

# 开局时建立新棋盘
def getNewBoard():
    board = []
    for i in range(8):
        board.append(['none'] * 8)
    return board

# 是否是合法走法，如果合法返回需要翻转的棋子列表
def isValidMove(board, tile, xstart, ystart):
    # 如果该位置已经有棋子或者出界了，返回False
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
        return False
    # 临时将tile 放到指定的位置
    board[xstart][ystart] = tile
    if tile == 'black':
        otherTile = 'white'
    else:
        otherTile = 'black'
    # 要被翻转的棋子
    tilesToFlip = []
    for xdirection, ydirection in [ [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1] ]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            # 一直走到出界或不是对方棋子的位置
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            # 出界了，则没有棋子要翻转OXXXXX
            if not isOnBoard(x, y):
                continue
            # 是自己的棋子OXXXXXXO
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    # 回到了起点则结束
                    if x == xstart and y == ystart:
                        break
                    # 需要翻转的棋子
                    tilesToFlip.append([x, y])
    # 将前面临时放上的棋子去掉，即还原棋盘
    board[xstart][ystart] = 'none' # restore the empty space
    # 没有要被翻转的棋子，则走法非法。翻转棋的规则。
    if len(tilesToFlip) == 0:   # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

# 是否出界
def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

# 获取可落子的位置
def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

# 获取棋盘上黑白双方的棋子数
def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'black':
                xscore += 1
            if board[x][y] == 'white':
                oscore += 1
    return {'black':xscore, 'white':oscore}

# 决定谁先走
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

# 将一个tile棋子放到(xstart, ystart)
def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:    #tilesToFlip是需要翻转的棋子列表
        board[x][y] = tile      #翻转棋子
    return True
# 复制棋盘
def getBoardCopy(board):
    dupeBoard = getNewBoard()
    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard
# 是否在角上
def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

# 电脑走法，AI
def getComputerMove(board, computerTile):
    # 获取所以合法走法
    possibleMoves = getValidMoves(board, computerTile)
    if  not possibleMoves:  #如果没有合法走法
        print("电脑没有合法走法")
        return None
    
    # 打乱所有合法走法
    random.shuffle(possibleMoves)
    # [x, y]在角上，则优先走，因为角上的不会被再次翻转
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        # 按照分数选择走法，优先选择翻转后分数最多的走法
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove
# 是否游戏结束
def isGameOver(board):
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'none':
                return False
    return True

#画棋盘
def drawQiPan( ):
    img1= imgs[2]
    cv.create_image((360,360),image=img1)
    cv.pack()

def callback(event):#走棋
    global turn
    #print ("clicked at", event.x, event.y,turn)
    #x=(event.x)//40  #换算棋盘坐标
    #y=(event.y)//40
    if (gameOver == False and turn == 'computer'):#没轮到玩家走棋
         return    
    col = int((event.x-40)/80)    #换算棋盘坐标
    row = int((event.y-40)/80)
    if mainBoard[col][row]!="none":
       showinfo(title="提示",message="已有棋子")
    if makeMove(mainBoard, playerTile, col, row) == True:  # 将一个玩家棋子放到(col, row)
         if getValidMoves(mainBoard, computerTile) != []:
              turn = 'computer'
    #电脑走棋
    if getComputerMove(mainBoard, computerTile)==None:
        turn = 'player'
        showinfo(title="玩家继续",message="玩家继续")
    else:
        computerGo()        
    #重画所有的棋子和棋盘
    drawAll()
    drawCanGo()
    if isGameOver(mainBoard):         #游戏结束，显示双方棋子数量
        scorePlayer = getScoreOfBoard(mainBoard)[playerTile]
        scoreComputer = getScoreOfBoard(mainBoard)[computerTile]
        outputStr = gameoverStr + "玩家:"+str(scorePlayer) + ":"  + "电脑:"+ str(scoreComputer)
        showinfo(title="游戏结束提示",message=outputStr)
#电脑走棋
def  computerGo():
    global turn
    if (gameOver == False and turn == 'computer'):
        x, y = getComputerMove(mainBoard, computerTile) #电脑AI走法
        makeMove(mainBoard, computerTile, x, y)
        savex, savey = x, y
        # 玩家没有可行的走法了，则电脑继续，否则切换到玩家走
        if getValidMoves(mainBoard, playerTile) != []:
            turn = 'player'
        else:
            if getValidMoves(mainBoard, computerTile) != []:
                showinfo(title="电脑继续",message="电脑继续")
                computerGo()
#重画所有的棋子和棋盘
def   drawAll():
    drawQiPan()
    for x in range(8):
        for y in range(8):            
            if mainBoard[x][y] == 'black':
                cv.create_image((x*80+80,y*80+80),image=imgs[0])                
                cv.pack()
            elif mainBoard[x][y] == 'white':
                cv.create_image((x*80+80,y*80+80),image=imgs[1])
                cv.pack()
#画提示位置
def   drawCanGo():
    list1=getValidMoves(mainBoard, playerTile)
    for m in list1:
         x=m[0]
         y=m[1]         
         cv.create_image((x*80+80,y*80+80),image=imgs[3])                
         cv.pack()
    
# 初始化
gameOver = False
gameoverStr = 'Game Over Score '
mainBoard = getNewBoard()
resetBoard(mainBoard)
turn = whoGoesFirst()
showinfo(title="游戏开始提示",message=turn+"先走!")
print(turn,"先走!") 
if turn == 'player':
    playerTile = 'black'
    computerTile = 'white'
else:
    playerTile = 'white'
    computerTile = 'black'
    computerGo()

# 设置窗口
cv = Canvas(root, bg = 'green', width =720, height = 780)
#重画所有的棋子和棋盘
drawAll()
drawCanGo()
cv.bind("<Button-1>", callback)
cv.pack()
root.mainloop()

