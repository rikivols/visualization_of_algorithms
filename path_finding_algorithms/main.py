import argparse

from algorithms.random_search import RandomSearch
from algorithms.djinsktra import Djinkstra
from algorithms.a_star import AStar
from algorithms.dfs import DFS
from algorithms.ldfs import LDFS
from algorithms.greedy import Greedy
from algorithms.bfs import BFS
from maze import Maze

algorithms = {
    "astar": AStar,
    "bfs": BFS,
    "dfs": DFS,
    "djinkstra": Djinkstra,
    "greedy": Greedy,
    "ldfs": LDFS,
    "random_search": RandomSearch
}

def start_main(args):
    algorithm = args.algorithm.lower()
    if algorithm not in algorithms:
        raise RuntimeError(f"Wrong algorithm selected, please select from these options: {algorithms.keys()}")

    file_name = args.file_name
    sleep_time = args.sleep_time
    wave_mode = args.wave_mode
    silent_mode = args.silent_mode
    maze = Maze(file_name, sleep_time, silent_mode)
    search_algo = algorithms[algorithm](maze, wave_mode)
    if search_algo.find_path(maze.get_start(), maze.get_end()):
        print("PATH FOUND")
    else:
        print("NO PATH FOUND")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program that visualizes different path finding algorithms step by step.'
    )

    parser.add_argument('--algorithm', type=str, required=True,
                        help=f'Choose from these algorithms: {algorithms.keys()}.')
    parser.add_argument('--file_name', type=str, required=True, help='Path to the input file.')
    parser.add_argument('--sleep_time', type=float, required=False, default=1.0,
                        help='How long to sleep after each visualization.')
    parser.add_argument('--wave_mode', type=bool, required=False, default=False,
                        help='If true, displays the maze and expanded nodes only if the newest longest path has been discovered.'
                        )
    parser.add_argument('--silent_mode', type=bool, required=False, default=False,
                        help='If true, steps are not visualized, only final result is printed.'
                        )

    args = parser.parse_args()
    start_main(args)
