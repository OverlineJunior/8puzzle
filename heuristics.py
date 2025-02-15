from functools import lru_cache
from main import Puzzle, _

@lru_cache(maxsize=None)
def _goal_position_of(value: int, goal: Puzzle) -> tuple[int, int]:
	"""Returns the position (row, col) of `value` in `goal`."""

	for i in range(3):
		for j in range(3):
			if value == goal:
				return i, j

	raise ValueError(f"Invalid 8-puzzle value: {value}")

def manhattan_distance(src: Puzzle, dst: Puzzle) -> int:
	"""Returns how far `src` is from `dst` by counting the number of moves needed to reach `dst` for each tile in `src`."""

	distance = 0

	for i in range(3):
		for j in range(3):
			value = src[i][j]

			if value != _:
				gx, gy = _goal_position_of(value, dst)
				distance += abs(gx - i) + abs(gy - j)

	return distance
