# decorator to measure execution time of a function
# + take 1 argument (k), also compute sweeping average
# for execution time of last k calls (omit this output while
# number of calls is less then k)

from collections import deque
from functools import wraps
from time import sleep, time
from typing import Any, Deque, Dict

from click import secho


def sweeping_timeit(k: int):
    """
    Track execution time of decorated function
    and compute sweeping average across last k runs

    :param k, int
    """

    def _timer(func):
        runs: Deque[float] = deque(maxlen=k)
        secho(f"Tracking execution time of {func.__name__} ({k=})", fg="red")

        @wraps(func)
        def timer(*args: Any, **kwds: Dict[str, Any]):
            t_start = time()
            result = func(*args, **kwds)
            t_end = time()

            runs.append(t_end - t_start)
            secho(f"> Elapsed time: {runs[-1]:.3f}s", fg="green")

            if len(runs) < k:
                return result

            secho(
                f"> Average time for last {k} runs: {sum(runs) / k :.3f}s",
                fg="magenta",
            )

            return result

        return timer

    return _timer


# def sweeping_timeit(k: int):
#     """
#     Track exetution time and compute sweeping average execution time
#     across last k runs

#     :param k, int
#     """

#     def _timer(func):
#         runs: List[float] = []
#         calls: int = 0

#         secho(f"Tracking execution time of {func.__name__} ({k=})", fg="red")

#         @wraps(func)
#         def timer(*args: Any, **kwds: Dict[str, Any]):
#             t_start = time()
#             result = func(*args, **kwds)
#             t_end = time()

#             nonlocal calls
#             nonlocal runs

#             calls += 1
#             runs += [t_end - t_start]

#             secho(f"Elapsed time: {runs[-1]}", fg="green")
#             if calls < k:
#                 return result

#             avg_elapsed = sum(runs[-k:]) / k
#             secho(
#                 f"> Average execution time for last {k} runs: {avg_elapsed}",
#                 fg="magenta",
#             )
#             runs = runs[-k:]

#             return result

#         return timer

#     return _timer


@sweeping_timeit(k=3)
def sleeper() -> None:
    print("will just sleep...")
    sleep(0.2)
    print("woke up")


@sweeping_timeit(k=2)
def intensive_computation(work: float) -> None:
    print(f"WILL WORK FOR {work}s...")
    sleep(work)
    print("WORK DONE!")


if __name__ == "__main__":

    for _ in map(intensive_computation, (0.1, 0.2, 0.3, 0.6, 0.1, 0.4)):
        pass

    for _ in range(5):
        sleeper()
