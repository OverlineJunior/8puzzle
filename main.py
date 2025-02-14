from collections import deque
import copy
from typing import Optional
from graph import Node

type Puzzle = list[list[int]]

# Represents an empty tile.
_ = 0

SOLVED_STATES = [
	[
		[1, 2, 3],
		[8, _, 4],
		[7, 6, 5],
	],
	[
		[1, 2, 3],
		[4, 5, 6],
		[7, 8, _],
	],
	# ...
]

def is_solved(puzzle: Puzzle) -> bool:
	return puzzle in SOLVED_STATES

def get_possible_moves(puzzle: Puzzle) -> list[Puzzle]:
	empty_row, empty_col = [(r, c) for r in range(3) for c in range(3) if puzzle[r][c] == 0][0]
	moves = []

	for i in range(4):
		new_row, new_col = empty_row + [0, 0, -1, 1][i], empty_col + [-1, 1, 0, 0][i]

		if -1 < new_row < 3 and -1 < new_col < 3:
			move = copy.deepcopy(puzzle)
			move[empty_row][empty_col], move[new_row][new_col] = move[new_row][new_col], move[empty_row][empty_col]
			moves.append(move)

	return moves

def solve_with_dfs(initial: Puzzle, max_depth: int) -> Optional[Node[Puzzle]]:
	expanded = [Node(initial)]

	while len(expanded) > 0:
		node = expanded.pop()

		if is_solved(node.value):
			return node

		if node.depth() < max_depth:
			for move in get_possible_moves(node.value):
				child = Node(move, node)
				node.add_child(child)
				expanded.append(child)

def solve_with_bfs(initial: Puzzle) -> Optional[Node[Puzzle]]:
	expanded = deque([Node(initial)])

	while len(expanded) > 0:
		node = expanded.popleft()

		if is_solved(node.value):
			return node

		for move in get_possible_moves(node.value):
			child = Node(move, node)
			node.add_child(child)
			expanded.append(child)

def solve_with_gbf():
	pass

def solve_with_astar():
	pass

puzzle = [
	[_, 1, 2],
	[7, 8, 3],
	[6, 5, 4],
]

if result := solve_with_dfs(puzzle, 10):
	print("DFS:")
	result.display_lineage()

if result := solve_with_bfs(puzzle):
	print("\nBFS:")
	result.display_lineage()
