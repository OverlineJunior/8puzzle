# We use tuples because they are hashable, thus can be used in a set.
type Puzzle = tuple[tuple[int, ...], ...]

# Represents an empty tile.
_ = 0

def get_possible_moves(puzzle: Puzzle) -> list[Puzzle]:
	"""
	Returns a list of all possible states that can be reached from `puzzle` by moving the empty tile.
	"""

	scale = len(puzzle)
	empty_row, empty_col = [(r, c) for r in range(scale) for c in range(scale) if puzzle[r][c] == 0][0]
	moves = []

	for i in range(4):
		new_row, new_col = empty_row + [0, 0, -1, 1][i], empty_col + [-1, 1, 0, 0][i]

		if -1 < new_row < scale and -1 < new_col < scale:
			move = [list(row) for row in puzzle] # Cloning 1 level deep.
			move[empty_row][empty_col], move[new_row][new_col] = move[new_row][new_col], move[empty_row][empty_col]
			moves.append(tuple(tuple(row) for row in move))

	return moves
