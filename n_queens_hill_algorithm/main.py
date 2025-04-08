
import random
import time
import os
import json


class QueenPosition:

    def __init__(self, board_size: int):
        self.board_size = board_size
        self.queen_positions = set()
        # for quick random
        self.queen_positions_list = []
        self.queen_rows = [0] * board_size
        self.queen_columns = [0] * board_size
        self.queen_diagonals = [0] * (board_size * 2)
        self.queen_reverse_diagonals = [0] * (board_size * 2)

    def get_random_coordinates(self) -> (int, int):
        return random.randrange(0, self.board_size), random.randrange(0, self.board_size)

    def calculate_diagonal(self, position: (int, int)) -> int:
        """ convert queen's position into a diagonal """
        return position[0] + position[1]

    def calculate_reverse_diagonal(self, position: (int, int)) -> int:
        return self.board_size - position[0] + position[1]

    def is_move_possible(self, new_move: (int, int)) -> bool:
        return new_move not in self.queen_positions

    def get_queen_position(self, n: int) -> (int, int):
        return self.queen_positions_list[n]

    def get_random_queen(self) -> (int, int):
        return random.choice(self.queen_positions_list)

    def calculate_potential_move(self, old_position: (int, int), new_position: (int, int)) -> int:
        score_difference = 0
        queen_position_i, queen_position_j = old_position
        diagonal_coordinate = self.calculate_diagonal(old_position)
        reverse_diagonal_coordinate = self.calculate_reverse_diagonal(old_position)

        new_queen_position_i, new_queen_position_j = new_position
        new_diagonal_coordinate = self.calculate_diagonal(new_position)
        new_reverse_diagonal_coordinate = self.calculate_reverse_diagonal(new_position)

        # remove old position coordinates - check if we have less queens attacking each other
        if queen_position_i != new_queen_position_i:
            if self.queen_rows[queen_position_i] > 1:
                score_difference -= 1
            if self.queen_rows[new_queen_position_i] > 0:
                score_difference += 1

        if queen_position_j != new_queen_position_j:
            if self.queen_columns[queen_position_j] > 1:
                score_difference -= 1
            if self.queen_columns[new_queen_position_j] > 0:
                score_difference += 1

        if diagonal_coordinate != new_diagonal_coordinate:
            if self.queen_diagonals[diagonal_coordinate] > 1:
                score_difference -= 1
            if self.queen_diagonals[new_diagonal_coordinate] > 0:
                score_difference += 1

        if reverse_diagonal_coordinate != new_reverse_diagonal_coordinate:
            if self.queen_reverse_diagonals[reverse_diagonal_coordinate] > 1:
                score_difference -= 1

            if self.queen_reverse_diagonals[new_reverse_diagonal_coordinate] > 0:
                score_difference += 1

        return score_difference

    def move_queen(self, n: int, new_position: (int, int)):
        old_position = self.queen_positions_list[n]
        self.queen_positions_list[n] = new_position
        queen_position_i, queen_position_j = old_position
        diagonal_coordinate = self.calculate_diagonal(old_position)
        reverse_diagonal_coordinate = self.calculate_reverse_diagonal(old_position)

        # remove old position coordinates - check if we have less queens attacking each other
        self.queen_rows[queen_position_i] -= 1
        self.queen_columns[queen_position_j] -= 1
        self.queen_diagonals[diagonal_coordinate] -= 1
        self.queen_reverse_diagonals[reverse_diagonal_coordinate] -= 1

        queen_position_i, queen_position_j = new_position
        diagonal_coordinate = self.calculate_diagonal(new_position)
        reverse_diagonal_coordinate = self.calculate_reverse_diagonal(new_position)

        self.queen_rows[queen_position_i] += 1
        self.queen_columns[queen_position_j] += 1
        self.queen_diagonals[diagonal_coordinate] += 1
        self.queen_reverse_diagonals[reverse_diagonal_coordinate] += 1

        self.queen_positions.remove(old_position)
        self.queen_positions.add(new_position)

    def random_initial_position(self):
        """ Generate N random queens """

        # temporary queen positions
        points = 0
        queen_positions = set()

        self.queen_positions = set()
        self.queen_rows = [0] * self.board_size
        self.queen_columns = [0] * self.board_size
        self.queen_diagonals = [0] * (self.board_size * 2)
        self.queen_reverse_diagonals = [0] * (self.board_size * 2)

        for i in range(self.board_size):
            while True:
                queen_position = self.get_random_coordinates()
                if queen_position not in queen_positions:
                    queen_positions.add(queen_position)
                    self.queen_rows[queen_position[0]] += 1
                    self.queen_columns[queen_position[1]] += 1
                    self.queen_diagonals[self.calculate_diagonal(queen_position)] += 1
                    self.queen_reverse_diagonals[self.calculate_reverse_diagonal(queen_position)] += 1
                    break

        for v in self.queen_rows:
            points += max(0, v - 1)
        for v in self.queen_columns:
            points += max(0, v - 1)
        for v in self.queen_diagonals:
            points += max(0, v - 1)
        for v in self.queen_reverse_diagonals:
            points += max(0, v - 1)

        self.queen_positions = queen_positions
        self.queen_positions_list = list(queen_positions)
        return points

    def color_red(self, text: str):
        return f"\033[91m{text}\033[0m"

    def color_blue(self, text: str):
        return f"\033[94m{text}\033[0m"

    def print_queens(self, queen_to_move: (int, int)=None, positions_to_choose: set[(int, int)]=None,
                 queen_destination: (int, int)=None):
        print("-" * (self.board_size * 2 + 1))
        for i in range(self.board_size):
            for j in range(self.board_size):
                symbol_print = " "
                if queen_to_move and (i, j) == queen_to_move:
                    symbol_print = self.color_red("Q")
                elif queen_destination and (i, j) == queen_destination:
                    symbol_print = self.color_blue("Q")
                elif positions_to_choose and (i, j) in positions_to_choose:
                    symbol_print = self.color_blue(".")
                elif not self.is_move_possible((i, j)):
                    symbol_print = "Q"
                print(f"|{symbol_print}", end="")
            print("|")

        print("-" * (self.board_size * 2 + 1))

class NQueens:

    def __init__(self, config_file: str):
        self.board_size = 0
        self.visualization_print = False
        self.use_resets = False
        self.time_sleep = 0
        self.open_config(config_file)

        self.queen_positions = QueenPosition(self.board_size)
        self.best_score = self.queen_positions.random_initial_position()
        self.k = self.board_size
        self.stuck_counter = 0
        self.stuck_counter_max = self.board_size * 10

    def open_config(self, config_file: str):
        with open(config_file, encoding="utf-8") as f:
            config_res = json.load(f)

        self.board_size = config_res["board_size"]
        self.visualization_print = config_res["visualize"]
        self.use_resets = config_res["use_resets"]
        self.time_sleep = config_res["time_sleep"]

    def generate_random_positions(self, n: int) -> set[(int, int)]:
        result = set()

        for _ in range(n):
            while True:
                random_position = (random.randrange(0, self.board_size), random.randrange(0, self.board_size))
                if self.queen_positions.is_move_possible(random_position) and random_position not in result:
                    result.add(random_position)
                    break
        return result

    def do_print(self, queen_to_move: (int, int)=None, positions_to_choose: set[(int, int)]=None,
                 queen_destination: (int, int)=None):
        if not self.visualization_print:
            return

        os.system("clear")
        print(f"queens attacking each other: {self.best_score}, Board size: {self.board_size}, stuck counter: {self.stuck_counter}, K: {self.k}")
        self.queen_positions.print_queens(queen_to_move, positions_to_choose, queen_destination)
        print("rows:", self.queen_positions.queen_rows)
        print("cols:", self.queen_positions.queen_columns)
        print("diagonals:", self.queen_positions.queen_diagonals)
        print("reverse diagonals:", self.queen_positions.queen_reverse_diagonals)
        time.sleep(self.time_sleep)

    def start(self):
        self.do_print()

        while True:
            if self.best_score == 0:
                break

            random_queen = random.randrange(0, self.board_size)
            old_queen_position = self.queen_positions.get_queen_position(random_queen)
            self.do_print(old_queen_position)

            # find k random positions for the queen
            best_position = (-1, -1)
            best_score_difference = float('inf')
            chosen_positions = self.generate_random_positions(self.k)
            self.do_print(old_queen_position, chosen_positions)
            for random_position in chosen_positions:
                score_difference = self.queen_positions.calculate_potential_move(old_queen_position, random_position)
                if score_difference < best_score_difference:
                    best_score_difference = score_difference
                    best_position = random_position

            if best_score_difference <= 0:
                self.do_print(old_queen_position, chosen_positions, best_position)
                self.queen_positions.move_queen(random_queen, best_position)
                self.best_score += best_score_difference

                if best_score_difference == 0:
                    self.stuck_counter += 1
                else:
                    self.stuck_counter = 0
            else:
                self.stuck_counter += 1

            if not self.use_resets:
                continue

            if self.stuck_counter > self.stuck_counter_max:
                self.best_score = self.queen_positions.random_initial_position()
                if self.visualization_print:
                    print("Position has been reset!")
                self.do_print()
                self.stuck_counter = 0
            else:
                self.do_print()

        # print("FINAL RESULT:")
        os.system("clear")
        self.queen_positions.print_queens()

if __name__ == "__main__":
    st = time.time()
    n_queens = NQueens("config.json")
    n_queens.start()
    print('Time took:', time.time() - st)

