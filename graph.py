from dataclasses import dataclass, field
from typing import Optional

type Path[T] = list[Node[T]]
"""
List of nodes, where the first is the root and the last is the leaf.
"""

def pretty_path[T](path: Path[T]) -> str:
	lines = []

	for n in path:
		depth = n.depth()
		postfix = (
			" <-- root" if depth == 0
			else " <-- leaf" if depth == len(path) - 1
			else ""
		)
		lines.append(f"{n.value}, depth: {depth}{postfix}")

	return "\n".join(lines)

@dataclass
class Edge:
	src: "Node"
	dst: "Node"

@dataclass
class Node[T]:
	value: T
	_parent: Optional["Node"] = None
	_edges: list[Edge] = field(default_factory=list)

	def add_child(self, child: "Node[T]"):
		child._parent = self
		self._edges.append(Edge(self, child))

	def children(self) -> list["Node[T]"]:
		return [edge.dst for edge in self._edges]

	def depth(self) -> int:
		"""
		Returns how deep the node is in the tree, starting from 0 since we use
		the node's depth to count puzzle moves.
  		"""

		node = self
		d = 0

		while node._parent:
			d += 1
			node = node._parent

		return d

	def root(self) -> "Node[T]":
		node = self

		while node._parent:
			node = node._parent

		return node

	def path(self) -> Path[T]:
		"""
		Returns the path from root to self.
		"""

		node = self
		path = []

		while node:
			path.append(node)
			node = node._parent

		path.reverse()
		return path

	# `heapq` requires nodes to be comparable, even though the comparison has no effect on the algorithms.
	def __lt__(self, other: "Node[T]") -> bool:
		return False
