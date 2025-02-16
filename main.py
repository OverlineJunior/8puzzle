from collections import deque
from collections.abc import Container
from typing import Optional
from graph import Node
from heuristics import Heuristic, manhattan_distance
from shared import Puzzle, _
from time import time
import heapq

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

def search(
    initial: Puzzle,
    goal: Puzzle,
    container: Container,
    insert: callable[[Container, Node[Puzzle], Puzzle], None],
    extract: callable[[Container], Node[Puzzle]],
) -> Optional[Node[Puzzle]]:
	"""
	Generic search algorithm, used as the base for all other search algorithms here.
	"""

	expanded = container()
	insert(expanded, Node(initial), initial)

	visited: set[Puzzle] = set()
	visited.add(initial)

	while len(expanded) > 0:
		node = extract(expanded)

		if node.value == goal:
			return node

		for move in get_possible_moves(node.value):
			if move in visited:
				continue

			child = Node(move)
			node.add_child(child)
			insert(expanded, child, move)
			visited.add(move)

def solve_with_dfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by brute forcing all possible paths in a
	depth-first manner.
	"""

	return search(
		initial,
		goal,
		container = list,
		insert = lambda container, node: container.append(node),
		extract = lambda container: container.pop()
    )

def solve_with_bfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by brute forcing all possible paths in a
	breadth-first manner.
	"""

	return search(
		initial,
		goal,
		container = deque,
		insert = lambda container, node: container.appendleft(node),
		extract = lambda container: container.pop()
	)

def solve_with_gbf(initial: Puzzle, goal: Puzzle, heuristic: Heuristic) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by successively going for the next possible
	empty space movement that leads to the state closest to goal.

	Faster to compute when compared to A*, but does not guarantee the shortest path.

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

	return search(
		initial,
		goal,
		container = list,
		insert = lambda container, node, state:
      		heapq.heappush(container, (heuristic(state, goal), node)),
		extract = lambda container: heapq.heappop(container)[1],
	)

def solve_with_astar(initial: Puzzle, goal: Puzzle, heuristic: Heuristic) -> Optional[Node[Puzzle]]:
	"""
	Tries to find the shortest path to goal by successively going for the next possible
	empty space movement that leads to the state closest to goal balanced with the least
	amount of moves already made.

	Slower to compute when compared to GBF, but guarantees the shortest path.

	Given
		S 1 1 1 5 G
		2 2 2 2 2 2
	where
		S is the start,
		G is the goal,
		and there are only 2 paths from S to G: (1, 1, 1, 5) and (2, 2, 2, 2, 2, 2),
	A* will successfully recognize that the first path is shorter.

	Why?
		Because A* not only considers the distance remaining to reach the goal,
  		but also the distance already traveled.
	"""

	return search(
		initial,
		goal,
		container = list,
		insert = lambda container, node, state:
      		heapq.heappush(container, (node.depth() + heuristic(state, goal), node)),
		extract = lambda container: heapq.heappop(container)[1],
	)

initial = (
	(2, 14, 4, 8),
    (1, 7, 3, 12),
    (5, 9, 6, _),
    (13, 10, 11, 15),
)

goal = (
	(1, 2, 3, 4),
	(5, 6, 7, 8),
	(9, 10, 11, 12),
	(13, 14, 15, _),
)

# if result := solve_with_dfs(initial, goal):
# 	print("DFS:")
# 	result.display_path()

# if result := solve_with_bfs(initial, goal):
# 	print("\nBFS:")
# 	result.display_path()

# if result := solve_with_gbf(initial, goal, manhattan_distance):
# 	print("\nGBF:")
# 	result.display_path()

start = time()

if result := solve_with_astar(initial, goal, manhattan_distance):
	print("\nA*:")
	result.display_path()

end = time()

print(f"\nTime taken: {end - start:.4f}s")
