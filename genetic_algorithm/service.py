import logging
import time
from typing import Generic, TypeVar, Callable, List, Optional

import duckdb
import pandas as pd

from genetic_algorithm.models import Unit

T = TypeVar("T")

log = logging.getLogger("genetic_algorithm")


class GeneticAlgorithm(Generic[T]):

    def __init__(
            self,
            random_func: Callable[[], T],
            mut_func: Callable[[T], T],
            cross_func: Callable[[T, T], T],
            fit_func: Callable[[T], int],
            pop_size: int = 5000,
            mut_size: int = 500,
            cross_size: int = 500,
            rand_size: int = 500,
            max_gens: int = 500,
            stop_score: Optional[int] = None,
            verbose: bool = False,
            save_local_db: bool = True,
            local_db_table_name: str = "population",
    ):
        self.stop_score = stop_score
        self.verbose = verbose
        self.save_local_db = save_local_db

        self.conn: Optional[duckdb.DuckDBPyConnection] = None
        if self.save_local_db:
            self.conn = duckdb.connect("population.duckdb")
           
        self.table_name = local_db_table_name

        self.random_func = random_func
        self.mut_func = mut_func
        self.cross_func = cross_func
        self.fit_func = fit_func

        self.pop_size = pop_size
        self.mut_size = mut_size
        self.cross_size = cross_size
        self.rand_size = rand_size
        self.max_gens = max_gens

        self.new_size = mut_size + cross_size + rand_size

        if pop_size <= 1:
            raise Exception("Population size must be greater or equal to one")

        if self.new_size > pop_size:
            raise Exception("The sum of mut_size, cross_size, and rand_size cannot exceed the size of the population")

        self.keep_size = pop_size - self.new_size
        self.population: List[Unit[T]] = list()

    def _sort_population(self):
        self.population.sort(key=lambda it: it.score, reverse=True)

    def _init_population(self):
        for _ in range(self.pop_size):
            current_content = self.random_func()
            current_unit = Unit(
                content=current_content,
                score=self.fit_func(current_content),
            )
            self.population.append(current_unit)

    def _save_to_db(self):
        df = pd.DataFrame([unit.model_dump() for unit in self.population])
        if self.conn is None:
            raise Exception("Could not find a valid local database to save information")
        self.conn.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} AS SELECT * FROM df LIMIT 0")
        self.conn.execute(f"INSERT INTO {self.table_name} SELECT * FROM df")

    def run(self) -> List[Unit[T]]:
        start_time = time.time()
        self._init_population()
        self._sort_population()

        final_gen = 0
        for idx in range(1, self.max_gens + 1):
            final_gen = idx
            keep_pop = self.population[:self.keep_size]
            new_pop = []

            for i in range(self.mut_size):
                cur = self.population[i]
                content = self.mut_func(cur.content)
                new_pop.append(Unit(
                    content=content,
                    generation=idx,
                    score=self.fit_func(content),
                    origin="mutation",
                ))

            for i in range(self.cross_size):
                cur_0 = self.population[i]
                cur_1 = self.population[i + 1]
                content = self.cross_func(cur_0.content, cur_1.content)
                new_pop.append(Unit(
                    content=content,
                    generation=idx,
                    score=self.fit_func(content),
                    origin="cross_over",
                ))

            for i in range(self.rand_size):
                content = self.random_func()
                new_pop.append(Unit(
                    content=content,
                    generation=idx,
                    score=self.fit_func(content),
                ))

            keep_pop.extend(new_pop)
            self.population = keep_pop
            self._sort_population()

            first = self.population[0]
            max_score = first.score
            if self.verbose:
                elapsed = time.time() - start_time
                log.info(f"Generation: {idx}; Max Score: {max_score}; Current: {first.content}; Elapsed: {elapsed:.2f}s")

            if self.save_local_db:
                self._save_to_db()

            if self.stop_score and max_score >= self.stop_score:
                log.info(f"Stop score reached")
                break

        first = self.population[0]
        max_score = first.score
        elapsed = time.time() - start_time
        log.info(f"Final Gen: {final_gen}; Max Score: {max_score}; Current: {first.content}; Elapsed: {elapsed:.2f}s")
        return self.population
