
from heapq import heappop, heappush

from maze import Maze
from algorithms.path_algorithm import PathAlgorithm


class Greedy(PathAlgorithm):
    def __init__(self, maze: Maze, wave_mode: bool):
        super().__init__(maze, wave_mode)
        self.distances = {}
        self.heap = []

    @staticmethod
    def calculate_heuristic(current_node: tuple[int], end: tuple[int]):
        return abs(current_node[0] - end[0]) + abs(current_node[1] - end[1])

    def find_path(self, start: tuple[int], end: tuple[int]) -> bool:
        if not self.check_start(start, end):
            return False

        self.expanded_nodes.add(start)
        heappush(self.heap, (self.calculate_heuristic(start, end), 0, start))
        max_distance = 0

        while self.heap:
            _, distance, current_node = heappop(self.heap)

            if current_node == end:
                self.reconstruct_path(start, end)
                self.maze.draw_maze(self.expanded_nodes, is_final=True)
                return True

            max_distance = self.draw_step(distance, max_distance)

            for next_direction in self.directions:
                next_node = (current_node[0] + next_direction[0], current_node[1] + next_direction[1])

                if not self.maze.is_valid(*next_node):
                    continue

                # check if we have a better value
                new_distance = self.calculate_heuristic(next_node, end)
                if next_node not in self.expanded_nodes:
                    self.expanded_nodes.add(next_node)
                    heappush(self.heap, (new_distance, distance + 1, next_node))
                    self.predecessors[next_node] = current_node

        return False