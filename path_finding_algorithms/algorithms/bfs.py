
import queue

from maze import Maze
from algorithms.path_algorithm import PathAlgorithm


class BFS(PathAlgorithm):
    def __init__(self, maze: Maze, wave_mode: bool):
        super().__init__(maze, wave_mode)
        self.queue = queue.Queue()

    def find_path(self, start: tuple[int], end: tuple[int]) -> bool:
        if not self.check_start(start, end):
            return False

        self.queue.put((start, 0))
        self.expanded_nodes.add(start)
        max_distance = 0


        while self.queue:
            current_node, distance = self.queue.get()

            if current_node == end:
                self.reconstruct_path(start, end)
                self.maze.draw_maze(self.expanded_nodes, is_final=True)
                return True

            max_distance = self.draw_step(distance, max_distance)

            for next_direction in self.directions:
                next_node = (current_node[0] + next_direction[0], current_node[1] + next_direction[1])
                if next_node not in self.expanded_nodes and self.maze.is_valid(*next_node):
                    self.expanded_nodes.add(next_node)
                    self.queue.put((next_node, distance + 1))
                    self.predecessors[next_node] = current_node

        return False
