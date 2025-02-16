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

def read_puzzle() -> Puzzle:
	"""
	Reads a `Puzzle` from a file in the root directory.

	Each tile must be represented by a digit or X for the empty tile, all separated by whitespace.
	"""

	def parse(tile: str) -> int:
		if tile.isdigit():
			return int(tile)
		elif tile == "X":
			return 0
		else:
			raise ValueError(f"Invalid tile `{tile}` in `{INPUT_PATH}`")

	with open(INPUT_PATH) as file:
		tiles = [parse(tile) for tile in file.read().split()]
		l = len(tiles)

		if l == 9 or l == 16 or l == 25:
			return tuple(tuple(row) for row in square_matrix(tiles))
		else:
			raise ValueError(f"Expected `{INPUT_PATH}` to have 9, 16, or 25 tiles, got {len(tiles)}")

def write_search_results(path: Path[Puzzle], visited_count: int):
	"""
	Writes the search results to a file in the root directory.
	"""

	with open(RESULTS_PATH, "w") as file:
		file.write(f"Nodes visited: {visited_count}\n")
		file.write("\nPath:\n")
		file.write(pretty_path(path, pretty_puzzle))
