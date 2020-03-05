import numpy

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    board = numpy.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    # Flip the board over the X access so it will start from the bottom
    print(numpy.flip(board, 0))


def winning_move(board, piece):  # Check if 4 connected pieces are together, algorithm not effieicnt, but I am just doing this for Python practice rather than building something hyper-optimized
    # Check Horizontals
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Check Verticals
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check Positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+1] == piece and board[r+3][c+1] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+1] == piece and board[r-3][c+1] == piece:
                return True


board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    # Ask for player 1 input
    if turn == 0:
        selected_column = int(input("Player 1 Make your Selection (0-6):"))

        if is_valid_location(board, selected_column):
            row = get_next_open_row(board, selected_column)
            drop_piece(board, row, selected_column, 1)

    if winning_move(board, 1):
        print("PLAYER 2 WINS!!!")
        game_over = True
        break

    # print(selection)
    # print(type(selection))
    # Ask for player 2 input
    else:
        selected_column = int(input("Player 2 Make your Selection (0-6):"))

        if is_valid_location(board, selected_column):
            row = get_next_open_row(board, selected_column)
            drop_piece(board, row, selected_column, 2)

    if winning_move(board, 2):
        print("PLAYER 2 WINS!!!")
        game_over = True
        break

    print_board(board)

    turn += 1
    turn = turn % 2  # Make it alternate between 0 and 1
