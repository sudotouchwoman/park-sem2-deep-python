import gc
from memory_profiler import profile

from utils import tag_factory, slotted_tag_factory

LIST_SIZE = 5_000


@profile
def memory_test():
    slotted = [slotted_tag_factory(f"div-{i}") for i in range(LIST_SIZE)]
    non_slotted = [tag_factory(f"{i}-div") for i in range(LIST_SIZE)]

    del slotted
    del non_slotted
    gc.collect()

    slotted_gen = (slotted_tag_factory(f"{i}") for i in range(LIST_SIZE))
    non_slotted_gen = (tag_factory(f"{i}") for i in range(LIST_SIZE))

    for _ in slotted_gen:
        pass
    for _ in non_slotted_gen:
        pass


if __name__ == "__main__":
    memory_test()
