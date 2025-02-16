from collections import deque
from collections.abc import Container, Callable
from typing import Optional
from graph import Node
from heuristics import Heuristic
from shared import Puzzle, _, get_possible_moves
import heapq

def search(
    initial: Puzzle,
    goal: Puzzle,
    container: Container,
    insert: Callable[[Container, Node[Puzzle], Puzzle], None],
    extract: Callable[[Container], Node[Puzzle]],
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

def search_with_dfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
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

def search_with_bfs(initial: Puzzle, goal: Puzzle) -> Optional[Node[Puzzle]]:
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

def search_with_gbf(initial: Puzzle, goal: Puzzle, heuristic: Heuristic) -> Optional[Node[Puzzle]]:
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

def search_with_astar(initial: Puzzle, goal: Puzzle, heuristic: Heuristic) -> Optional[Node[Puzzle]]:
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
