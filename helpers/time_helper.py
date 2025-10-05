import time
from contextlib import contextmanager


class TimeHelper:
    _start_times = {}
    _elapsed_times = {}

    @staticmethod
    @contextmanager
    def measure(label: str):
        TimeHelper._start_times[label] = time.perf_counter()
        try:
            yield
        finally:
            start = TimeHelper._start_times.pop(label, None)
            if start is not None:
                elapsed = time.perf_counter() - start
                TimeHelper._elapsed_times[label] = (
                    TimeHelper._elapsed_times.get(label, 0.0) + elapsed
                )

    @staticmethod
    def get_elapsed(label: str):
        return TimeHelper._elapsed_times.get(label, 0.0)
