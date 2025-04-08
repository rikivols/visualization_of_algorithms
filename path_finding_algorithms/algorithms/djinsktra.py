
from heapq import heappop, heappush

from maze import Maze
from algorithms.path_algorithm import PathAlgorithm


class Djinkstra(PathAlgorithm):
    def __init__(self, maze: Maze, wave_mode: bool):
        super().__init__(maze, wave_mode)
        self.distances = {}
        self.heap = []

    def find_path(self, start: tuple[int], end: tuple[int]) -> bool:
        if not self.check_start(start, end):
            return False

        self.distances[start] = 0
        self.expanded_nodes.add(start)
        heappush(self.heap, (0, start))
        max_distance = 0

        while self.heap:
            distance, current_node = heappop(self.heap)

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
                if next_node not in self.distances or distance + 1 < self.distances[next_node]:
                    self.distances[next_node] = distance + 1
                    self.expanded_nodes.add(next_node)

                    heappush(self.heap, (distance + 1, next_node))
                    self.predecessors[next_node] = current_node

        return False