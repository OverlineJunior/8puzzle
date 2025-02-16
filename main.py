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

	search_result: SearchResult = None
	match args.algorithm:
		case "DFS":
			search_result = search_with_dfs(initial, goal)
		case "BFS":
			search_result = search_with_bfs(initial, goal)
		case "GBF":
			search_result = search_with_gbf(initial, goal, manhattan_distance)
		case "A*":
			search_result = search_with_astar(initial, goal, manhattan_distance)

	if search_result:
		write_search_results(*search_result)
