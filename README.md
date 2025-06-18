# Genetic Algorithm Utility Library

## What?

This package provides a generic class so you can work on simple GAs.
These are the parameters you can configure:

- `random_func`: A function that generates a parameter of type [T]
- `mut_func`: A function that accepts a parameter of type [T] and returns another object of type [T]
- `cross_func`: A function that accepts two parameters of type [T] and returns another object of type [T]
- `fit_func`: A function that takes [T] and returns an integer - describing the score, bigger is better
- `pop_size`: Size of the population
- `mut_size`:  Size of the population that will be replaced by mutation
- `cross_size`: Size of the population that will be replaced by cross over
- `rand_size`: Size of the population that will be replaced by random generation
- `max_gens`: Maximum number of generations
- `stop_score`: Target score to stop before generations hit the maximum amount
- `verbose`: Logs information about the process, for each generation
- `save_local_db`: Creates a duckdb database locally with all created data
- `local_db_table_name`: Name of the local duckdb table

## Use Example

```python
import logging
import random
import string
from functools import partial

from genetic_algorithm.service import GeneticAlgorithm


def get_random_phrase(k: int) -> str:
    return "".join(random.choices(string.printable, k=k))


def get_random_segment(size: int, pct: float = 0.2) -> tuple[int, int]:
    mutation_size = round(size * pct)
    start = random.randint(0, size - mutation_size - 1)
    end = start + mutation_size
    return start, end


def mutate(phrase: str, pct: float = 0.4) -> str:
    size = len(phrase)
    mutation_size = round(size * pct)
    start, end = get_random_segment(size, pct)
    random_chars = get_random_phrase(mutation_size)
    return phrase[:start] + random_chars + phrase[end:]


def cross_over(phrase_one: str, phrase_two: str, pct: float = 0.2) -> str:
    size = len(phrase_one)
    start, end = get_random_segment(size, pct)
    segment_from_two = phrase_two[start:end]
    return phrase_one[:start] + segment_from_two + phrase_one[end:]


def get_points(expected: str, current: str) -> int:
    points = 0
    for i in range(len(expected)):
        cur_expected = expected[i]
        cur_actual = current[i]
        if cur_expected == cur_actual:
            points += 1
    return points


def main():
    logging.basicConfig(level=logging.INFO)

    expected = "I'm a cool pass phrase"

    fit_func = partial(get_points, expected)
    random_func = partial(get_random_phrase, len(expected))

    ga = GeneticAlgorithm(
        random_func=random_func,
        mut_func=mutate,
        cross_func=cross_over,
        fit_func=fit_func,
        stop_score=len(expected),
        verbose=True,
    )

    end_pop = ga.run()
    ...


if __name__ == "__main__":
    main()
```