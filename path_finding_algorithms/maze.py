
import os
import time

START = "S"
END = "E"
WALL = "X"
OPENED_NODE = "."
PATH = "o"

maze_descriptions = {
    START: "Start",
    END: "End",
    WALL: "Wall",
    OPENED_NODE: "Opened Node",
    PATH: "Path"
}


class Maze:

    def __init__(self, input_file: str, sleep_time: float, silent_mode: bool):
        self.state = []
        self.start = None
        self.end = None
        self.path = []
        self.step = 0
        self.sleep_time = sleep_time
        self.silent_mode = silent_mode
        self.load_maze(input_file)

    def load_maze(self, input_file: str):
        with open(input_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if "start" in line:
                    start = line.split("start ")[-1]
                    s1, s2 = start.split(", ")
                    self.start = (int(s2), int(s1))
                elif "end" in line:
                    end = line.split("end ")[-1]
                    e1, e2 = end.split(", ")
                    self.end = (int(e2), int(e1))
                else:
                    self.state.append(list(line.strip()))

    def is_valid(self, i: int, j: int) -> bool:
        if i < 0 or j < 0 or i >= len(self.state) or j >= len(self.state[0]):
            return False
        return self.state[i][j] == " "

    def set_path(self, path: list):
        self.path = path

    def get_start(self) -> tuple:
        return self.start

    def get_end(self) -> tuple:
        return self.end

    @staticmethod
    def draw_line():
        print("-" * 50)

    @staticmethod
    def print_description():
        for key, value in maze_descriptions.items():
            print(f"{key}: {value}")
        print("space: Fresh node")

    def draw_maze(self, expanded_nodes: set, **kwargs):
        if not self.silent_mode:
            time.sleep(self.sleep_time)

        if self.silent_mode and "is_final" not in kwargs:
            return

        os.system("clear")
        self.step += 1

        print("STEP:", self.step, end=" ")
        for k in kwargs:
            print(k.upper(), ":", kwargs[k], end = " ")
        print("\n")

        for i in range(len(self.state)):
            for j in range(len(self.state[0])):
                if (i, j) == self.start:
                    print(START, end="")
                elif (i, j) == self.end:
                    print(END, end="")
                elif (i, j) in self.path:
                    print(PATH, end="")
                elif (i, j) in expanded_nodes:
                    print(OPENED_NODE, end="")
                else:
                    print(self.state[i][j], end="")
            print()

        self.draw_line()
        self.print_description()
        self.draw_line()
        # don't include start
        print("Nodes expanded:", max(len(expanded_nodes) - 1, 0))
        print("Path length:", len(self.path))
