from shared import Puzzle, _

def read_puzzle() -> Puzzle:
	"""
	Reads a `Puzzle` from a file in the root directory.
	"""

	with open("input.txt") as file:
		print(file.read())

def write_search_results():
	"""
	Writes the search results to a file in the root directory.
	"""

	pass
