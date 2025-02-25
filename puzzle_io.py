import math
from graph import Path, pretty_path
from shared import Puzzle, _, pretty_puzzle

INPUT_PATH = "io/input.txt"
RESULTS_PATH = "io/results.txt"

def square_matrix[T](arr: list[T]) -> list[list[T]]:
	"""
	Converts a 1D list into a 2D square matrix.

	E.g. [1, 2, 3, 4] -> [[1, 2], [3, 4]]
	"""

	scale = int(math.sqrt(len(arr)))
	return [arr[i:(i + scale)] for i in range(0, len(arr), scale)]

def matrix2d_to_tuple2d[T](matrix: list[list[T]]) -> tuple[tuple[T]]:
	return tuple(tuple(row) for row in matrix) # type: ignore

def parse_puzzle_input() -> tuple[Puzzle, Puzzle]:
	"""
	Parses the initial and goal puzzles from the input file.

	Syntax:
	```python
	# `X` represents the empty tile.
	initial: 1 2 3 4 5 6 7 8 X
	goal: 1 2 3 4 5 6 7 8 X
	```
	"""

	def parse_tile(tile: str) -> int:
		if tile.isdigit():
			return int(tile)
		elif tile == "X":
			return 0
		else:
			raise ValueError(f"Invalid puzzle tile `{tile}` in `{INPUT_PATH}`")

	with open(INPUT_PATH) as file:
		lexemes = file.read().split()

		initial_idx = lexemes.index("initial:")
		goal_idx = lexemes.index("goal:")

		initial_nums = [parse_tile(l) for l in lexemes[initial_idx + 1:goal_idx]]
		goal_nums = [parse_tile(l) for l in lexemes[goal_idx + 1:]]

		initial_len = len(initial_nums)
		goal_len = len(goal_nums)

		if initial_len != goal_len:
			raise ValueError(f"Expected initial and goal puzzles to have the same number of tiles, got `{initial_len}` and `{goal_len}`")

		if goal_len == 9 or goal_len == 16 or goal_len == 25:
			return (
				matrix2d_to_tuple2d(square_matrix(initial_nums)),
    			matrix2d_to_tuple2d(square_matrix(goal_nums)),
			)
		else:
			raise ValueError(f"Expected `{INPUT_PATH}` puzzles to have 9, 16, or 25 tiles, got `{goal_len}`")

def write_search_results(
		path: Path[Puzzle],
		visited_count: int,
		time_taken: float,
		peak_memory: int,
):
	"""
	Writes the search results to a file in the root directory.
	"""

	with open(RESULTS_PATH, "w") as file:
		file.write(f"Nodes visited: {visited_count}\n")
		file.write(f"Time taken: {time_taken:.6f} seconds\n")
		file.write(f"Peak memory usage: {peak_memory} KB\n")
		file.write("\nPath:\n")
		file.write(pretty_path(path, pretty_puzzle))
