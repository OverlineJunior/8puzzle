# We use tuples because they are hashable, thus can be used in a set.
type Puzzle = tuple[tuple[int, ...], ...]

# Represents an empty tile.
_ = 0
