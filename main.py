from collections import deque
from typing import Optional
from graph import Node
from heuristics import Heuristic, manhattan_distance
from shared import Puzzle, _
from time import time

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

def solve_with_dfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by brute forcing all possible paths in a
	depth-first manner.
	"""

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
	"""
	Tries to find the shortest path to goal by brute forcing all possible paths in a
	breadth-first manner.
	"""

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

def solve_with_gbf(initial: Puzzle, goal: Puzzle, heuristic: Heuristic) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by successively going for the next possible
	empty space movement that leads to the state closest to goal.

	Given
		S 1 1 1 5 G
		2 2 2 2 2 2
	where
		S is the start,
		G is the goal,
		and there are only 2 paths from S to G: (1, 1, 1, 5) and (2, 2, 2, 2, 2, 2),
	GBF will mistakenly think that the second path is shorter.

	Why?
		Because GBF only looks ahead and the second path is full of 2s, it will think the
		first path is a no go since it contains a 5, and 5 > 2.
	"""

	expanded = deque([Node(initial)])
	visited: set[Puzzle] = set()
	visited.add(initial)

	while len(expanded) > 0:
		expanded = deque(sorted(expanded, key=lambda node: heuristic(node.value, goal)))
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

def solve_with_astar(initial: Puzzle, goal: Puzzle, heuristic: Heuristic) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by successively going for the next possible
	empty space movement that leads to the state closest to goal balanced with the least
	amount of moves already made.

	Given
		S 1 1 1 5 G
		2 2 2 2 2 2
	where
		S is the start,
		G is the goal,
		and there are only 2 paths from S to G: (1, 1, 1, 5) and (2, 2, 2, 2, 2, 2),
	A* will successfully recognize that the first path is shorter.

	Why?
		Because A* not only considers the distance remaining to reach the goal, but also the distance already traveled.
	"""

	expanded = deque([Node(initial)])
	visited: set[Puzzle] = set()
	visited.add(initial)

	while len(expanded) > 0:
		expanded = deque(sorted(expanded, key=lambda node: node.depth() + heuristic(node.value, goal)))
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

initial = (
	(_, 2, 3),
	(4, 5, 7),
	(8, 1, 6),
)

goal = (
	(1, 2, 3),
	(4, 5, 6),
	(7, 8, _),
)

# if result := solve_with_dfs(initial, goal):
# 	print("DFS:")
# 	result.display_lineage()

# if result := solve_with_bfs(initial, goal):
# 	print("\nBFS:")
# 	result.display_lineage()

# if result := solve_with_gbf(initial, goal, manhattan_distance):
# 	print("\nGBF:")
# 	result.display_lineage()

start = time()

if result := solve_with_astar(initial, goal, manhattan_distance):
	print("\nA*:")
	result.display_lineage()

end = time()

print(f"\nTime taken: {end - start:.4f}s")
