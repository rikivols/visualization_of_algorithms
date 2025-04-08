
import random

from maze import Maze
from algorithms.path_algorithm import PathAlgorithm


class RandomSearch(PathAlgorithm):
    def __init__(self, maze: Maze, wave_mode: bool):
        super().__init__(maze, wave_mode)
        self.open_nodes = set()

    def find_path(self, start: tuple[int], end: tuple[int]) -> bool:
        if not self.check_start(start, end):
            return False

        self.open_nodes.add((start, 0))
        max_distance = 0

        while self.open_nodes:
            current_node, distance = random.choice(list(self.open_nodes))
            self.open_nodes.remove((current_node, distance))
            self.expanded_nodes.add(current_node)

            if current_node == end:
                self.reconstruct_path(start, end)
                self.maze.draw_maze(self.expanded_nodes, is_final=True)
                return True

            max_distance = self.draw_step(distance, max_distance)

            for next_direction in self.directions:
                next_node = (current_node[0] + next_direction[0], current_node[1] + next_direction[1])
                if next_node not in self.expanded_nodes and self.maze.is_valid(*next_node):
                    self.open_nodes.add((next_node, distance + 1))
                    self.predecessors[next_node] = current_node

        return False