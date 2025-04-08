
# Path finding visualizer

Program that visualizes different maze path finding algorithms step by step.

To run this program:
```
python3 main.py --algorithm bfs --file_name dataset/test_1.txt --wave_mode true
```

## Kwargs
* **--algorithm**
  * astar - A star algorithm
  * bfs - BFS algorithm
  * dfs - DFS algorithm
  * djinkstra - Djinkstra's algorithm
  * greedy - Greedy algorithm with manhattan distance
  * ldfs - Iterative DFS with max depth from 1 to n
  * random_search - Randomly expand open node
* **--file_name** - path to the maze file
* **--sleep_time** - how long to sleep for between each visualization step
* **--wave_mode** - if true, will visualize in waves, so only if a new longest path has been found, otherwise it 
prints each step
* **--silent_mode** - will only output result
