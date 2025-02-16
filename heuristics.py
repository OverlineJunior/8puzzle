from functools import lru_cache
from typing import Callable
from shared import Puzzle, _

type Heuristic = Callable[[Puzzle, Puzzle], int]

@lru_cache(maxsize=None)
def _goal_position_of(value: int, goal: Puzzle) -> tuple[int, int]:
	"""
	Returns the position (row, col) of `value` in `goal`.
	"""

	scale = len(goal)

	for row in range(scale):
		for col in range(scale):
			if value == goal[row][col]:
				return row, col

	raise ValueError(f"Invalid 8-puzzle value: {value}")

def manhattan_distance(src: Puzzle, dst: Puzzle) -> int:
	"""
	Returns how far `src` is from `dst` by counting the number of moves needed to reach `dst` for each tile in `src`.
	"""

	scale = len(src)
	distance = 0

	for row in range(scale):
		for col in range(scale):
			value = src[row][col]

			if value != _:
				g_row, g_col = _goal_position_of(value, dst)
				distance += abs(g_row - row) + abs(g_col - col)

	return distance
