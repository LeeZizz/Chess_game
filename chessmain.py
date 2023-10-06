# import pip
# pip.main(['install', 'pygame'])
import pygame as p
import ChessEngine
p.init()
WIDTH = HEIGHT = 512
DIMENTION = 8
SQ_SIZE = HEIGHT//DIMENTION     #kích thước 1 cạnh của ô vuông nhỏ trên bàn cờ
MAX_FPS = 15
IMAGES = {}
# Hàm tải ảnh
def loadImages():
    pieces = ['bp','bR','bN','bB','bQ','bK','wp','wR','wN','wB','wQ','wK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
        # transform.scale nhằm làm cho hình ảnh các quân cờ phù hợp kích thước với các ô vuông trên bàn cờ
    # Có thể sử dụng hình ảnh mỗi quân cờ bằng cách IMAGES['piece']
    # VD: IMAGES['bp'] lấy hình ảnh quân tốt đen


# Hàm chính
def main():
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    loadImages()
    running = True
    sqSelect = ()   # lưu dữ liệu của ô được nhấp chuột, ban đầu chưa ô nào được nhấp (row, col)
    playerClicks = []   #lưu trữ vị trí ban đầu và vị trí muốn di chuyển tới của quân cờ trên bàn cờ
    while running:
        for i in p.event.get():
            if i.type == p.QUIT:
                running = False
            elif i.type == p.MOUSEBUTTONDOWN:
                nocation = p.mouse.get_pos()   # lấy tọa độ (x,y) trên bảng khi nhấp chuột
                # lấy vị trí hàng và cột tương ứng
                col = nocation[0]//SQ_SIZE
                row = nocation[1]//SQ_SIZE
                if sqSelect == (row,col):    # nhấp 2 lần cùng 1 ô
                    sqSelect = ()   # Đặt lại
                    playerClicks = []
                else:
                    sqSelect = (row,col)
                    playerClicks.append(sqSelect)   # mảng chỉ có tối đa 2 phần tử lưu giá trị ban đầu và giá trị muốn di chuyển đến
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    if move in validMoves:   # nếu nước đi là 1 nước đi hợp lệ
                        gs.makeMove(move)
                        moveMade = True      # thể hiện nước đi đã thực hiện
                        sqSelect = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelect]
            # Quay lại nước đi trước khi nhấn 1 phím
            elif i.type == p.KEYDOWN:
                if i.key == p.K_z:   # quay lại nước đi trước khi nhấn phím 'z'
                    gs.undoMove()
                    moveMade = True
        # Nếu nước đi thỏa mãn được điều kiện thì sẽ thực hiện các nước đi hợp lệ tiếp theo
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):   # hiển thị bàn cờ và quân cờ
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    #vẽ bàn cờ vua có ô trắng và xám
    colors = [p.Color('#789658'), p.Color('#eaedd0')]
    #duyệt các ô trên bàn cờ
    for i in range(DIMENTION):
        for j in range(DIMENTION):
            # cách xác định các ô trắng và xám trên bàn cờ
            color = colors[(i+j)%2]
            p.draw.rect(screen,color,p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    # in các quân cờ lên bàn cờ
    for row in range(DIMENTION):
        for column in range(DIMENTION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()

