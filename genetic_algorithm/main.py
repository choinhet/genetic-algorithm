import random
import string
from functools import partial

def get_random_phrase(k: int) -> str:
    return "".join(random.choices(string.printable, k=k))


def get_random_segment(size: int, pct: float = 0.2) -> tuple[int, int]:
    mutation_size = round(size * pct)
    start = random.randint(0, size - mutation_size - 1)
    end = start + mutation_size
    return start, end


def mutate(phrase: str, pct: float = 0.2) -> str:
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
    expected = "I'm a cool pass phrase"
    expected_len = len(expected)
    pool = len(string.printable) * len(expected)

    print(f"Target is: '{expected}' - {pool} options")
    print("")

    points = partial(get_points, expected)

    pop_size, mut_size, cross_size, rand_size, max_gens = 5000, 400, 400, 400, 500
    keep_size = pop_size - (mut_size + cross_size + rand_size)

    random_population = [get_random_phrase(expected_len) for _ in range(pop_size)]

    random_population.sort(key=points, reverse=True)
    best = points(random_population[0])
    print(f"Initial best: '{random_population[0]}' - {best} points")
    print("Starting...")
    print("")

    gens = 0
    for _ in range(max_gens):
        best = points(random_population[0])
        print(f"Current best: '{random_population[0]}' - {best} points - Gen: {gens}")
        gens += 1
        keep_pop = random_population[keep_size:]
        new_pop = []

        for i in range(mut_size):
            cur = random_population[i]
            new_pop.append(mutate(cur, 0.3))

        for i in range(cross_size):
            cur_0 = random_population[i]
            cur_1 = random_population[i + 1]
            new_pop.append(cross_over(cur_0, cur_1))

        for i in range(rand_size):
            new_pop.append(get_random_phrase(expected_len))

        keep_pop.extend(new_pop)
        random_population = keep_pop

        random_population.sort(key=points, reverse=True)
        best = points(random_population[0])

        if best == expected_len:
            break

    print("")
    print(f"Final best: '{random_population[0]}' - {best} points")
    print(f"Took {gens} generations")


if __name__ == "__main__":
    main()
