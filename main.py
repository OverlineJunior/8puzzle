from collections import deque
import copy
from functools import lru_cache
from typing import Optional
from graph import Node

type Puzzle = list[list[int]]

# Represents an empty tile.
_ = 0

# TODO! Don't forget to use other goal states to test against infinite loops.
GOAL_STATE = [
	[1, 2, 3],
	[8, _, 4],
	[7, 6, 5],
]

def get_possible_moves(puzzle: Puzzle) -> list[Puzzle]:
	empty_row, empty_col = [(r, c) for r in range(3) for c in range(3) if puzzle[r][c] == 0][0]
	moves = []

	for i in range(4):
		new_row, new_col = empty_row + [0, 0, -1, 1][i], empty_col + [-1, 1, 0, 0][i]

		if -1 < new_row < 3 and -1 < new_col < 3:
			move = [list(row) for row in puzzle] # Cloning 1 level deep.
			move[empty_row][empty_col], move[new_row][new_col] = move[new_row][new_col], move[empty_row][empty_col]
			moves.append(move)

	return moves

def solve_with_dfs(initial: Puzzle, max_depth: int) -> Optional[Node[Puzzle]]:
	expanded = [Node(initial)]

	while len(expanded) > 0:
		node = expanded.pop()

		if node.value == GOAL_STATE:
			return node

		if node.depth() < max_depth:
			for move in get_possible_moves(node.value):
				child = Node(move, node)
				node.add_child(child)
				expanded.append(child)

def solve_with_bfs(initial: Puzzle) -> Optional[Node[Puzzle]]:
	expanded = deque([Node(initial)])
	visited = set()
	# Sets can only contain hashables for fast lookups.
	visited.add(tuple(map(tuple, initial)))

	while len(expanded) > 0:
		node = expanded.popleft()

		if node.value == GOAL_STATE:
			return node

		for move in get_possible_moves(node.value):
			move_id = tuple(map(tuple, move))

			if move_id in visited:
				continue

			child = Node(move, node)
			node.add_child(child)
			expanded.append(child)
			visited.add(move_id)

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
