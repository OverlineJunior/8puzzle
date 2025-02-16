from heuristics import manhattan_distance
from shared import _
from time import time
from search_algorithms import solve_with_dfs, solve_with_bfs, solve_with_gbf, solve_with_astar

initial = (
	(2, 14, 4, 8),
    (1, 7, 3, 12),
    (5, 9, 6, _),
    (13, 10, 11, 15),
)

goal = (
	(1, 2, 3, 4),
	(5, 6, 7, 8),
	(9, 10, 11, 12),
	(13, 14, 15, _),
)

# if result := solve_with_dfs(initial, goal):
# 	print("DFS:")
# 	result.display_path()

# if result := solve_with_bfs(initial, goal):
# 	print("\nBFS:")
# 	result.display_path()

# if result := solve_with_gbf(initial, goal, manhattan_distance):
# 	print("\nGBF:")
# 	result.display_path()

start = time()

if result := solve_with_astar(initial, goal, manhattan_distance):
	print("\nA*:")
	result.display_path()

end = time()

print(f"\nTime taken: {end - start:.4f}s")
