import random
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
pieceScore = {"K": 900, "Q":90, "R":50, "N":30, "B":30, "p":10}
knightScore=[[1, 1, 1, 1, 1, 1, 1, 1],
             [1, 2, 2, 2, 2, 2, 2, 1],
             [1, 2, 3, 3, 3, 3, 2, 1],
             [1, 2, 3, 4, 4, 3, 2, 1],
             [1, 2, 3, 4, 4, 3, 2, 1],
             [1, 2, 3, 3, 3, 3, 2, 1],
             [1, 2, 2, 2, 2, 2, 2, 1],
             [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores =[[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]

rootScores=[[4, 3, 4, 4, 4, 4, 3, 4],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 2, 3, 4, 4, 3, 2, 1],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [4, 4, 4, 4, 4, 4, 4, 4],
            [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores =[[0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 0, 0, 1, 1, 1],
                  [1, 1, 2, 3, 3, 2, 1, 1],
                  [1, 2, 3, 4, 4, 3, 2, 1],
                  [2, 3, 3, 5, 5, 3, 3, 2],
                  [5, 6, 6, 7, 7, 6, 6, 5],
                  [8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8]]
piecePositionScores ={"N": knightScore, "Q": queenScores, "B":bishopScores , "R":rootScores,
                      "bp":blackPawnScores, "wp":whitePawnScores}


def randomMove(validMoves):
    return validMoves[random.randint(0,len(validMoves)-1)]

def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    AlphaBetaPruning(gs,validMoves,DEPTH,-CHECKMATE,CHECKMATE,1 if gs.whiteToMove else -1)
    return nextMove

def AlphaBetaPruning(gs, validMoves, depth, alpha, beta, turn):
    global nextMove
    if depth == 0:
        return turn * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMoved(move)
        nextMoves = gs.getValidMoves()
        score = -AlphaBetaPruning(gs, nextMoves,depth-1,-beta,-alpha, -turn)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move,score)
        gs.undoMoved()
        if maxScore > alpha: #nơi quá trình cắt tỉa xảy ra
            alpha = maxScore
        if alpha >= beta:
            break

    return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE # quân đen thắng
        else:
            return CHECKMATE # quân trắng thắng
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                #diem theo vi tri
                piecePositionScore = 0
                if square[1] !="K": #không có bảng vi trí cho vua
                    if square[1] == 'p': # cho quan tot
                        piecePositionScore = piecePositionScores[square][row][col]
                    else: #quan co khac
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore

    return score