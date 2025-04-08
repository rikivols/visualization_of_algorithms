
from maze import Maze


class PathAlgorithm:
    def __init__(self, maze: Maze, wave_mode: bool):
        self.maze = maze
        self.wave_mode = wave_mode
        self.expanded_nodes = set()
        self.predecessors = {}
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def check_start(self, start: tuple[int], end: tuple[int]) -> bool:
        if not self.maze.is_valid(*start):
            self.maze.draw_maze(set())
            print("\nINCORRECT START POSITION")
            return False
        if not self.maze.is_valid(*end):
            self.maze.draw_maze(set())
            print("\nINCORRECT END POSITION")
            return False

        return True

    def reconstruct_path(self, start: tuple[int], end: tuple[int]):
        path = []
        current_node = end
        while current_node != start:
            path.append(current_node)
            current_node = self.predecessors[current_node]
        path.reverse()
        self.maze.set_path(path)

    def draw_step(self, current_distance: int, max_distance: int, **kwargs) -> int:
        if current_distance > max_distance:
            if self.wave_mode:
                self.maze.draw_maze(self.expanded_nodes, **kwargs, max_path_length=current_distance)
            max_distance = current_distance
        if not self.wave_mode and len(self.expanded_nodes) > 1:
            self.maze.draw_maze(self.expanded_nodes, **kwargs)

        return max_distance

    def find_path(self, start: tuple[int], end: tuple[int]) -> bool:
        raise NotImplementedError
