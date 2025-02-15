from collections import deque
import copy
from functools import lru_cache
from typing import Optional
from graph import Node

# We use tuples because they are hashable, thus can be used in a set.
type Puzzle = tuple[
	tuple[int, int, int],
	tuple[int, int, int],
	tuple[int, int, int],
]

# Represents an empty tile.
_ = 0

def get_possible_moves(puzzle: Puzzle) -> list[Puzzle]:
	empty_row, empty_col = [(r, c) for r in range(3) for c in range(3) if puzzle[r][c] == 0][0]
	moves = []

	for i in range(4):
		new_row, new_col = empty_row + [0, 0, -1, 1][i], empty_col + [-1, 1, 0, 0][i]

		if -1 < new_row < 3 and -1 < new_col < 3:
			move = [list(row) for row in puzzle] # Cloning 1 level deep.
			move[empty_row][empty_col], move[new_row][new_col] = move[new_row][new_col], move[empty_row][empty_col]
			moves.append(tuple(tuple(row) for row in move))

	return moves

def solve_with_dfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
	expanded = [Node(initial)]
	visited: set[Puzzle] = set()
	visited.add(initial)

	while len(expanded) > 0:
		node = expanded.pop()

		if node.value == goal:
			return node

		for move in get_possible_moves(node.value):
			if move in visited:
				continue

			child = Node(move, node)
			node.add_child(child)
			expanded.append(child)
			visited.add(move)

def solve_with_bfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
	expanded = deque([Node(initial)])
	visited: set[Puzzle] = set()
	visited.add(initial)

	while len(expanded) > 0:
		node = expanded.popleft()

		if node.value == goal:
			return node

		for move in get_possible_moves(node.value):
			if move in visited:
				continue

			child = Node(move, node)
			node.add_child(child)
			expanded.append(child)
			visited.add(move)

def solve_with_gbf():
	pass

def solve_with_astar():
	pass

initial = (
	(_, 2, 3),
	(1, 4, 5),
	(8, 7, 6),
)

goal = (
	(1, 2, 3),
	(8, _, 4),
	(7, 6, 5),
)

if result := solve_with_dfs(initial, goal):
	print("DFS:")
	result.display_lineage()

if result := solve_with_bfs(initial, goal):
	print("\nBFS:")
	result.display_lineage()
