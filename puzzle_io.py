import math
from graph import Path, pretty_path
from shared import Puzzle, _, pretty_puzzle

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
			raise ValueError(f"Invalid tile `{tile}` in `input.txt`")

	with open("input.txt") as file:
		tiles = [parse(tile) for tile in file.read().split()]
		l = len(tiles)

		if l == 9 or l == 16 or l == 25:
			return tuple(tuple(row) for row in square_matrix(tiles))
		else:
			raise ValueError(f"Expected `input.txt` to have 9, 16, or 25 tiles, got {len(tiles)}")

def write_search_results(path: Path[Puzzle], visited_count: int):
	"""
	Writes the search results to a file in the root directory.
	"""

	with open("results.txt", "w") as file:
		file.write(f"Nodes visited: {visited_count}\n")
		file.write("\nPath:\n")
		file.write(pretty_path(path, pretty_puzzle))
