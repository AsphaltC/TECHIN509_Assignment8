from logic import make_empty_board, get_winner, other_player
from cli import print_board
import numpy as np
import random
import time
import csv

class Game:
    def __init__(self):
        self.game_id = 1
        self.player_number = 0
        self.board = make_empty_board()
        self.players = ['X', 'O']
        self.winner = None
        self.coordinate_x = 0
        self.coordinate_y = 0
        self.x_win = 0
        self.o_win = 0

    def return_board(self):
        return self.board

    def update_board(self, x: int, y: int, player: str):
        self.board[x][y] = player

    def input_corrdinate(self):
        # Input a move from the player
        input_is_valid = False

        while input_is_valid is not True:
            input_x = input("Enter Row: ")
            input_y = input("Enter Col: ")
            self.coordinate_x = int(input_x) - 1
            self.coordinate_y = int(input_y) - 1

            if 0 <= self.coordinate_x <= 2 and 0 <= self.coordinate_y <= 2:
                input_is_valid = True
            else:
                print("Invalid Input! Please try again for integers between 0 and 2.")

    def write_statistic(self):
        # statistical results
        path = "statistic.csv"
        with open(path, 'a+') as f:
            csv_write = csv.writer(f)
            data_row = [time.asctime(time.localtime(time.time())), self.winner]
            csv_write.writerow(data_row)

    def count_wins(self):
        path = "statistic.csv"
        with open(path) as f:
            for line in f:
                if line[25] == 'X':
                    self.x_win = self.x_win + 1
                elif line[25] == "O":
                    self.o_win = self.o_win + 1

        print("==================================")
        print("Total Statistic:")
        print("X won:", self.x_win, "times")
        print("O won:", self.o_win, "times")



class SinglePlayerGame(Game):
    def __init__(self):
        super().__init__()
        self.is_user_turn = True

    def AI_random_step(self):
        empty_space = []

        # See how much space left
        for i in range(3):
            for j in range(3):
                if self.board[i][j] is None:
                    empty_space.append((i, j))

        # Get a random space and take a step
        step_corrdinate = empty_space[random.randint(0, len(empty_space) - 1)]

        return step_corrdinate


    def game_loop(self):
        # print(self.board)
        print_board(self.board)

        self.count_wins()

        while self.winner is None:
            if self.is_user_turn == True:
                # Print the current board
                print("==================================")
                print("User's Turn, please input")

                # Input a move from the player
                self.input_corrdinate()

                # Update the board
                self.update_board(self.coordinate_x, self.coordinate_y, 'X')

                # Print the board
                print("Board after Your input:")
                print_board(self.board)

            else:
                # Print the current board
                print("==================================")
                print("Computer AI's Turn, please wait...")
                time.sleep(3)

                # AI Bot take a step
                AI_step = self.AI_random_step()

                # Update the board
                self.update_board(AI_step[0], AI_step[1], 'O')

                # Print board
                print("current board below:")
                print_board(self.board)

            # Get Winner
            self.winner = get_winner(self.board)

            # Switch Player
            self.is_user_turn = 1 - self.is_user_turn

        print("Winner is", self.winner)

        # Write Statistic
        self.write_statistic()


class MultiPlayerGame(Game):
    def __init__(self):
        super().__init__()
        self.current_player = 'X'

    def game_loop(self):
        print_board(self.board)
        self.count_wins()

        while self.winner is None:
            print("====================================")
            print("It's player", self.current_player, "turn, please input")

            # Input a move from the player
            self.input_corrdinate()

            # Update the board
            self.update_board(self.coordinate_x, self.coordinate_y, self.current_player)
            print_board(self.board)

            # Get winner
            self.winner = get_winner(self.board)

            # Switch player
            self.current_player = other_player(self.current_player)

        print("Winner is", self.winner)
