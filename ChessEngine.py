class GameState():
    def __init__(self):
        #Bảng quân cờ, chữ cái đầu là màu quân cờ: b(black) ,w(white)
        # Chữ cái thứ 2 là tên quân cờ: R(rook), N(knight), B(bishop), Q(queen), K(king), p(pawn)
        self.board =[
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
        ]
        self.whiteToMove = True  # cho biết đến lượt quân trắng hay quân đen
        self.moveLog = []    # lưu trữ lịch sử các nước đi
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        # self.checkMate = False
        # self.staleMate = False
        self.inCheck = False
        self.pins = []
        self.checks = []


    def makeMove(self, move): # di chuyển quân cờ
        # di chuyển quân cờ từ vị trí ban đầu đến vị trí mong muốn
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        # cập nhật vị trí mới quân vua khi di chuyển
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):    # quay lại bước di chuyển trước
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            # xác định bước di chuyển cuối cùng trong lịch sử di chuyển
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.whiteToMove = not self.whiteToMove
            # cập nhật vị trí quân vua khi cần
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            
    def getValidMoves(self):
        # # các nước đi hợp lệ
        # # Trường hợp dưới mới chỉ xét hết các nước đi có thể xảy ra trong 1 lượt đi của quân trắng hoặc quân đen
        # # chưa xét trường hợp các quân không đuược di chuyển quân cờ nếu nước di chuyển sẽ làm hết cờ
        # #1) Sinh ra tất cả các nước hợp lệ
        # moves = self.getAllPossibleMoves()
        # #2) Triển khai từng nước
        # for i in range(len(moves) - 1, -1, -1):
        #     self.makeMove(moves[i])
        #     #3) Sinh ra tất cả nước của đối thủ
        #     #4) Từng nước của đối thủ xem có chiếu đến quân vua hay không
        #     self.whiteToMove = not self.whiteToMove
        #     if self.inCheck():
        #         moves.remove(moves[i]) #5) Nếu có đó không phải là nước hợp lệ 
        #     self.whiteToMove = not self.whiteToMove
        #     self.undoMove()
        # if len(moves) == 0:
        #     if self.inCheck():
        #         self.checkMate = True
        #     else:
        #         self.staleMate = True
        # else:
        #     self.checkMate = False
        #     self.staleMate = False
        # return moves

        moves = []
        self.inCheck , self.pins, self.checks = self.checkForPinAndChecks()
        if self. whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: # 
                moves = self.getAllPossibleMoves()
                # 
                check = self.checks[0] #
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #
                validSquares = [] #
                #
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) #
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                # 
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K': #
                        if not (moves[i].endRow, moves[i].endCol) in validSquares: #
                            moves.remove(moves[i])
            else: #
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        return moves
    
    def checkForPinAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == (): #
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        #
                        # 
                        # 
                        # 
                        # 
                        if (0 <= j <= 3 and type == 'R') or (4 <= j <= 7 and type == "B") or \
                            (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7))) or (enemyColor == 'b' and 4 <= j <= 5) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == (): #
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #
                                pins.append(possiblePin)
                                break
                        else:
                            break
        # kiểm tra chiếu của mã
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
    
    # Kiểm tra xem người chơi có đang bị chiếu tướng hay không
    # def inCheck(self):
    #     if self.whiteToMove:
    #         return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
    #     else:
    #         return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    # Kiểm tra xem đối thủ có thể tấn công ô (r, c)
    def squareUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()        
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False
            

    # Tất cả các nước khi không bị chiếu
    def getAllPossibleMoves(self):
        moves = []
        # duyệt các ô vuông trên bàn cờ
        for row in range(8):
            for col in range(8):
                colorPiece = self.board[row][col][0]
                if (colorPiece == 'w' and self.whiteToMove) or (colorPiece == 'b' and self.whiteToMove == False):
                    piece = self.board[row][col][1]
                    if piece == 'p':  # là quân tốt
                        self.getPawnMoves(row, col, moves)
                    elif piece == 'N':  # là quân mã
                        self.getKnightMoves(row, col, moves)
                    elif piece == 'B':  # là quân tượng
                        self.getBishopMoves(row, col, moves)
                    elif piece == 'R':  # là quân xe
                        self.getRockMoves(row, col, moves)
                    elif piece == 'Q':  # là quân hậu
                        self.getQueenMoves(row, col, moves)
                    elif piece == 'K':  # là quân vua
                        self.getKingMoves(row, col, moves)

        return moves

    # hàm tìm các vị trí có thể di chuyển của quân tốt
    def getPawnMoves(self, row, col, moves):
        # if self.whiteToMove:  # luợt của quân trắng
        #     if row > 0:
        #         if self.board[row - 1][col] =='--':  # nếu trước mặt quân tốt là khoảng trống
        #             moves.append(Move((row,col), (row-1,col), self.board))
        #             # nếu trước ô thứ 2 trước mặt là khoảng trống với điều kiện ô 1 là khoảng trống thì hợp lệ
        #             if self.board[row - 2][col] == '--' and row == 6:
        #                 moves.append(Move((row, col), (row - 2, col), self.board))
        #         # nếu có quân chéo trái hoặc tréo phải khác màu thì có thể ăn
        #         if col > 0:
        #             if self.board[row - 1][col - 1] != '--' and self.board[row - 1][col - 1][0] == 'b':
        #                 moves.append(Move((row, col), (row - 1, col - 1), self.board))
        #         if col < 7:
        #             if self.board[row - 1][col + 1] != '--' and self.board[row - 1][col + 1][0] == 'b':
        #                 moves.append(Move((row, col), (row - 1, col + 1), self.board))
        # else:
        #     # tương tự với quân đen
        #     if row < 7:
        #         if self.board[row + 1][col] =='--':
        #             moves.append(Move((row,col), (row + 1,col), self.board))
        #             if self.board[row + 2][col] == '--' and row == 1:
        #                 moves.append(Move((row, col), (row + 2, col), self.board))
        #         if col > 0:
        #             if self.board[row + 1][col - 1] != '--' and self.board[row + 1][col - 1][0] == 'w':
        #                 moves.append(Move((row, col), (row + 1, col - 1), self.board))
        #         if col < 7:
        #             if self.board[row + 1][col + 1] != '--' and self.board[row + 1][col + 1] == 'w':
        #                 moves.append(Move((row, col), (row + 1, col + 1), self.board))
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            if self.board[row - 1][col] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col), (row - 2, col), self.board))
            
            if col - 1 >= 0:
                if self.board[row - 1][col - 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, -1):
                        moves.append(Move((row, col), (row - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row - 1][col + 1][0] == 'b':
                    if not piecePinned or pinDirection == (-1, 1):
                        moves.append(Move((row, col), (row - 1, col + 1), self.board))
        else:
            if self.board[row + 1][col] == "--":
                if not piecePinned or pinDirection == (1, 0):
                    moves.append(Move((row, col), (row + 1, col), self.board)) 
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), self.board))      

            if col - 1 >= 0:
                if self.board[row + 1][col - 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, -1):
                        moves.append(Move((row, col), (row + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[row + 1][col + 1][0] == 'w':
                    if not piecePinned or pinDirection == (1, 1):
                        moves.append(Move((row, col), (row + 1, col + 1), self.board))
            
    def getKnightMoves(self, row, col, moves):  # hàm tìm các vị trí có thể di chuyển của quân mã
        # knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        # allyColor = "w" if self.whiteToMove else "b"
        # for m in knightMoves:
        #     endRow = row + m[0]
        #     endCol = col + m[1]
        #     if 0 <= endRow < 8 and 0 <= endCol < 8:
        #         endPiece = self.board[endRow][endCol]
        #         if endPiece[0] != allyColor:
        #             moves.append(Move((row, col), (endRow, endCol), self.board))

        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = row + m[0]
            endCol = col + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((row, col), (endRow, endCol), self.board))   

    def getBishopMoves(self, row, col, moves):  # hamf tìm các vị trí có thể di chuyển của quân tượng
        # dỉrections = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #di chuyển tréo
        # enemeyColor = "b" if self.whiteToMove else "w"
        # for d in dỉrections:
        #     for i in range(1, 8): #quân tượng có thể di chuyển chéo nhiều nhất 7 ô
        #         endRow = row + d[0] * i
        #         endCol = col + d[1] * i
        #         if 0 <= endRow < 8 and 0 <= endCol < 8:
        #             endPiece = self.board[endRow][endCol]
        #             if endPiece == "--":
        #                 moves.append(Move((row, col), (endRow, endCol), self.board))
        #             elif endPiece[0] == enemeyColor:
        #                 moves.append(Move((row, col), (endRow, endCol), self.board))
        #                 break
        #             else:
        #                 break
        #         else:
        #             break
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])    
                self.pins.remove(self.pins[i])
                break
        dỉrections = ((-1, -1), (-1, 1), (1, -1), (1, 1)) #di chuyển tréo
        enemeyColor = "b" if self.whiteToMove else "w"
        for d in dỉrections:
            for i in range(1, 8): #quân tượng có thể di chuyển chéo nhiều nhất 7 ô
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemeyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break
        

    def getRockMoves(self, row, col, moves):    # hàm tìm các vị trí có thể di chuyển của quân xe
        # dỉrections = ((-1, 0), (0, -1), (1, 0), (0, 1)) #di chuyển trái phải trên xuống
        # enemeyColor = "b" if self.whiteToMove else "w"
        # for d in dỉrections:
        #     for i in range(1, 8):
        #         endRow = row + d[0] * i
        #         endCol = col + d[1] * i
        #         if 0 <= endRow < 8 and 0 <= endCol < 8:
        #             endPiece = self.board[endRow][endCol]
        #             if endPiece == "--":
        #                 moves.append(Move((row, col), (endRow, endCol), self.board))
        #             elif endPiece[0] == enemeyColor:
        #                 moves.append(Move((row, col), (endRow, endCol), self.board))
        #                 break
        #             else:
        #                 break
        #         else:
        #             break

        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[row][col][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: 
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((row, col), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row, col), (endRow, endCol), self.board))     
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self, row, col, moves):   # hàm tìm các vị trí có thể di chuyển của quân hậu
        self.getRockMoves(row, col, moves)
        self.getBishopMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):    # hàm tìm các vị trí có thể di chuyển của quân vua
        # kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        # allyColor = "w" if self.whiteToMove else "b"
        # for k in kingMoves:
        #     endRow = row + k[0]
        #     endCol = col + k[1]
        #     if 0 <= endRow < 8 and 0 <= endCol < 8:
        #         endPiece = self.board[endRow][endCol]
        #         if endPiece[0] != allyColor:
        #             moves.append(Move((row, col), (endRow, endCol), self.board))
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:

                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinAndChecks()
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    
                    if allyColor == 'w':
                        self.whiteKingLocation = (row, col)
                    else:
                        self.whiteBlacLocation = (row, col)


class Move:
    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.endRow = endSq[0]
        self.startCol = startSq[1]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]   # vị trí ban đầu của quân cờ
        self.pieceCaptured = board[self.endRow][self.endCol]    # vị trí di chuyển tới
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
    # ghi đè
    def __eq__(self, other):
        if isinstance(other,Move):
            return other.moveID == self.moveID
        return False

