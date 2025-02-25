from typing import Callable
from benchmark import benchmark_time, benchmark_memory
from heuristics import manhattan_distance
from shared import _
from search_algorithms import search_with_dfs, search_with_bfs, search_with_gbf, search_with_astar, SearchResult
from puzzle_io import parse_puzzle_input, write_search_results
from argparse import ArgumentParser

initial, goal = parse_puzzle_input()

parser = ArgumentParser()
parser.add_argument("algorithm", choices=["DFS", "BFS", "GBF", "A*"])

if __name__ == "__main__":
	args = parser.parse_args()

	algorithm: Callable
	match args.algorithm:
		case "DFS":
			algorithm = lambda: search_with_dfs(initial, goal)
		case "BFS":
			algorithm = lambda: search_with_bfs(initial, goal)
		case "GBF":
			algorithm = lambda: search_with_gbf(initial, goal, manhattan_distance)
		case "A*":
			algorithm = lambda: search_with_astar(initial, goal, manhattan_distance)

	# We must do everything separatedly, otherwise one benchmark will affect the other.
	search_result = algorithm()
	time_taken = benchmark_time(algorithm)
	peak_memory = benchmark_memory(algorithm)

	if search_result:
		write_search_results(*search_result, time_taken, peak_memory)
