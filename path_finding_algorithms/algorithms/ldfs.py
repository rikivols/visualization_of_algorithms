
from maze import Maze
from algorithms.path_algorithm import PathAlgorithm


class LDFS(PathAlgorithm):
    def __init__(self, maze: Maze, wave_mode: bool):
        super().__init__(maze, wave_mode)

    def find_path_max_depth(self, start: tuple[int], end: tuple[int], max_depth: int):
        stack = [(start, 0)]
        expanded_nodes_current = {start}
        self.predecessors = {}
        if not self.wave_mode:
            self.expanded_nodes = set()
        self.expanded_nodes.add(start)
        max_distance = 0


        while stack:
            current_node, distance = stack.pop()

            if current_node == end:
                return True

            if not self.wave_mode:
                max_distance = self.draw_step(distance, max_distance, max_depth=max_depth)

            if distance >= max_depth:
                continue

            for next_direction in self.directions:
                next_node = (current_node[0] + next_direction[0], current_node[1] + next_direction[1])

                if next_node not in expanded_nodes_current and self.maze.is_valid(*next_node):
                    self.expanded_nodes.add(next_node)
                    expanded_nodes_current.add(next_node)
                    stack.append((next_node, distance + 1))
                    if next_node not in self.predecessors:
                        self.predecessors[next_node] = current_node

        return False

    def find_path(self, start: tuple[int], end: tuple[int], max_depth: int=10000) -> bool:
        if not self.check_start(start, end):
            return False

        for i in range(1, max_depth):
            if self.find_path_max_depth(start, end, i):
                self.reconstruct_path(start, end)
                self.maze.draw_maze(self.expanded_nodes, max_depth=i, is_final=True)
                return True
            if self.wave_mode:
                self.maze.draw_maze(self.expanded_nodes, max_depth=i)

        return False
