import os
import random

# Game Board List
BOARD = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.first = False

    def make_move(self):
        print("Your turn, make your move.")

        while True:
            try:
                x_pos = int(input("Enter row position [1 - 3]: "))
                y_pos = int(input("Enter col position [1 - 3]: "))

                if -1 < round(x_pos-1, 0) < 3 and -1 < round(y_pos-1, 0) < 3:
                    # If position is available, use it otherwise send a message
                    if BOARD[x_pos-1][y_pos-1] == ' ':
                        BOARD[x_pos-1][y_pos-1] = self.symbol
                        break
                    print("Position already in use, try another")
                else:
                    print("Invalid option!")
            except ValueError as err:
                print("You can only enter whole numbers!")


class Computer:
    def __init__(self, symbol='X'):
        self.name = 'Computer'
        self.symbol = symbol

        # Set enemy symbol
        self.enemy = 'X' if self.symbol != 'X' else 'O'

        # Set weights for each position in the matrix
        self.weights = [
        [0.75, 0.5, 0.75],
        [0.50, 0.9, 0.50],
        [0.75, 0.5, 0.75]
        ]
        # States for unused positions
        self.valid_states = [0.5, 0.75, 0.9]
        # This weights correspond to unused normal, border and center

    def check_victory(self, symbol):

        # Find if the player can win with the next move, if so block it
        for i, row in enumerate(BOARD):
            # If there are two positions used by player and there is a position empty
            if row.count(symbol) == 2 and row.__contains__(' '):
                return (i, row.index(' '))

        for i, col in enumerate(list(zip(*BOARD))):
            # If there are two positions used by player and there is a position empty
            if col.count(symbol) == 2 and col.__contains__(' '):
                return (col.index(' '), i)

        diagonal = [BOARD[n][n] for n in range(len(BOARD))]
        inversed = [BOARD[n][2-n] for n in range(len(BOARD))]

        if diagonal.count(symbol) == 2 and diagonal.__contains__(' '):
            return (diagonal.index(' '), diagonal.index(' '))

        if inversed.count(symbol) == 2 and inversed.__contains__(' '):
            return (diagonal.index(' '), 2 - diagonal.index(' '))

        return None

    def select_move(self):
        # Select the most optimal movement
        # We will try using a weight system were each position has a given value given it's state

        # Board state will contains the weights for each row and column
        board_state = []

        vertical_board = [list(col) for col in list(zip(*BOARD))] # Transposed board

        for row, weights in zip(BOARD, self.weights):
            row_state = []

            for block, weight in zip(row, weights):
                row_state.append(  1 if block == self.symbol else 0 if block == self.enemy else weight )

            board_state.append( row_state )

        diagonal_state = [board_state[n][n] for n in range(len(board_state))]
        inversed_state = [board_state[n][2-n] for n in range(len(board_state))]

        best_position_row, row_best = self.select_best(board_state)
        best_position_col, col_best = self.select_best(list(zip(*board_state)))
        best_position_dig, dig_best = self.select_best_diagonal(diagonal_state)
        best_position_inv, inv_best = self.select_best_diagonal(inversed_state)

        if row_best >= col_best and row_best >= dig_best and row_best >= inv_best:
            # Case Row is Best
            x, y = best_position_row
            BOARD[x][y] = self.symbol
        elif col_best >= dig_best and col_best >= inv_best:
            # Case Column is Best
            y, x = best_position_col
            BOARD[x][y] = self.symbol
        elif dig_best >= inv_best:
            # Case Diagonal is Best
            n = best_position_dig
            BOARD[n][n] = self.symbol
        else:
            # Case Inverse Diagonal is Best
            n = best_position_inv
            BOARD[n][2-n] = self.symbol


    def select_best(self, states):
        # Select the best row for making a move, this will be the row with the highest total weight and that has a block available

        total_weights = list()

        for row_states in states:
            if any(row_state in self.valid_states for row_state in row_states):
                total_weights.append( sum(row_states) )
            else:
                total_weights.append( 0 )

        # Select the row with the highest weight
        best_row = total_weights.index( max(total_weights) )

        weights = [item for item in states[best_row] if item in self.valid_states]
        best_weight = max(weights) if len(weights) > 0 else 0

        best_block = states[best_row].index(best_weight)

        # Return the position of the best move and it's value
        return (best_row, best_block), max(total_weights)

    def select_best_diagonal(self, state):
        total_weight = sum(state)
        # In the case where all diagonals are used by enemy or player do not execute
        if total_weight < 3 and total_weight > 0.4:

            weights = [ item for item in state if item in self.valid_states]
            best_weight  = max(weights) if len(weights) > 0 else 0

            return state.index(best_weight), total_weight
        return 0, 0

    def make_move(self):
        # This function will evaluate the board and make the best possible move
        computer = self.check_victory(self.symbol)
        opponent = self.check_victory(self.enemy)

        if computer is not None:
            # If computer can win on the next move, use it
            BOARD[computer[0]][computer[1]] = self.symbol
        elif opponent is not None:
            # If enemy can win on the next move, block it
            BOARD[opponent[0]][opponent[1]] = self.symbol
        else:
            # Select the most optimal position
            # I will establish priority position by giving weights to each position
            e.select_move()

def gameboard():
    # This function is in charge of drawing the board

    print('  |-----------|')
    for i, row in enumerate(BOARD):
        print(f'{i+1} | {row[0]} | {row[1]} | {row[2]} |')
        print('  |-----------|')
    print('    1   2   3  ')

def evaluate_board(player):
    # This function will evaluate if the player/computer has won, otherwise it will return False
    for row in BOARD:
        if all([block == player.symbol for block in row]):
            return True

    for col in list(zip(*BOARD)):
        if all([block == player.symbol for block in col]):
            return True

    if all(block == player.symbol for block in [BOARD[n][n] for n in range(len(BOARD))]):
        return True

    if all(block == player.symbol for block in [BOARD[n][2-n] for n in range(len(BOARD))]):
        return True

    return False

def flip_coin():

    print("Toss a coin to decide who goes first.")
    while True:
        choice = input("Enter 1 for head and 0 for tails: ")
        if choice == '1' or choice == '0':
            return  int(choice) == random.randint(0, 1)
        print("Select a valid option.")

def intro():
    print('Welcome to Tic-Tac-Toe')
    print("What's your name as player?")
    name = input("Enter name: ")

    print("Next, do you want to be X or O?")
    while True:
        symbol = input("Enter X or O: ")
        if symbol.upper() == 'X' or symbol.upper() == 'O':
            return Player(name, symbol.upper())
        print("Enter a valid option! (X or O)")


if __name__ == '__main__':

    player = intro()

    computer_symbol = 'X' if player.symbol == 'O' else 'O'
    e = Computer(symbol=computer_symbol)

    first = flip_coin()
    os.system("cls")

    # If player choose right
    if first:
        print("You go first")

    counter = 1

    while True:

        print(f'---- Turn {counter} ----')

        # Order of the moves
        if first:
            print("Your move")
            gameboard()
            player.make_move()
            if BOARD[0].count(' ') + BOARD[1].count(' ') + BOARD[2].count(' ') == 0:
                print("There are no more available positions, it's a draw.")
                break
            if evaluate_board(e):
                print(f'{e.name} Wins!')
                break
            e.make_move()
            if BOARD[0].count(' ') + BOARD[1].count(' ') + BOARD[2].count(' ') == 0:
                print("There are no more available positions, it's a draw.")
                break
            if evaluate_board(e):
                print(f'{e.name} Wins!')
                break
        else:
            e.make_move()
            if BOARD[0].count(' ') + BOARD[1].count(' ') + BOARD[2].count(' ') == 0:
                print("There are no more available positions, it's a draw.")
                break
            if evaluate_board(e):
                print(f'{e.name} Wins!')
                break
            gameboard()
            print("Your move")
            player.make_move()
            if BOARD[0].count(' ') + BOARD[1].count(' ') + BOARD[2].count(' ') == 0:
                print("There are no more available positions, it's a draw.")
                break
            if evaluate_board(e):
                print(f'{e.name} Wins!')
                break

        counter = counter + 1