from typing import Callable
from time import time
import tracemalloc

def benchmark_time(fn: Callable, *args, **kwargs) -> float:
	start = time()
	fn(*args, **kwargs)
	end = time()
	return end - start

def benchmark_memory(fn: Callable, *args, **kwargs) -> int:
	tracemalloc.start()
	fn(*args, **kwargs)
	_, peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	return peak
