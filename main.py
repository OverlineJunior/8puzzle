from heuristics import manhattan_distance
from shared import _
from search_algorithms import search_with_astar
from puzzle_io import read_puzzle, write_search_results

initial = read_puzzle()

goal = (
	(1, 2, 3, 4),
	(5, 6, 7, 8),
	(9, 10, 11, 12),
	(13, 14, 15, _),
)

match search_with_astar(initial, goal, manhattan_distance):
	case path, visited_count:
		write_search_results(path, visited_count)
