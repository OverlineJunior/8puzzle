from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Edge:
	src: "Node"
	dst: "Node"

@dataclass
class Node[T]:
	value: T
	parent: Optional["Node"] = None
	_edges: list[Edge] = field(default_factory=list)

	def add_child(self, node: "Node[T]"):
		self._edges.append(Edge(self, node))

	def children(self) -> list["Node[T]"]:
		return [edge.dst for edge in self._edges]

	def depth(self) -> int:
		node = self
		d = 0

		while node.parent:
			d += 1
			node = node.parent

		return d

	def root(self) -> "Node[T]":
		node = self

		while node.parent:
			node = node.parent

		return node

	def display_lineage(self):
		node = self
		lineage = []

		while node:
			lineage.append(node)
			node = node.parent

		for n in reversed(lineage):
			depth = n.depth()
			postfix = (
				" <-- root" if depth == 0
				else " <-- self" if depth == self.depth()
				else ""
			)
			print(f"{n.value}, depth: {depth}{postfix}")
