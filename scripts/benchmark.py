import time

from memex.search import (search_keywords, search_keywords_and,
                          search_keywords_or, search_url)
from scripts.utils import populate_entries


def timeit(func, desc):
    start = time.perf_counter()
    out = func()
    end = time.perf_counter()
    print("elapsed time for '" + desc + "' " + str(end - start))
    return out


if __name__ == "__main__":
    # os.remove(test_db)
    timeit(lambda: populate_entries(100), "database population")
    _ = timeit(lambda: search_keywords_or(["government"]), "one word search")
    _ = timeit(
        lambda: search_keywords_or(["government", "instruction"]), "two word search"
    )
    _ = timeit(
        lambda: search_keywords_and(["government", "instruction"]),
        "two word intersection search",
    )
