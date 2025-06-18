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
