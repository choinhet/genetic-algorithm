import duckdb

if __name__ == "__main__":
    conn = duckdb.connect("population.duckdb")
    conn.query(
        """
        select 
            timestamp,
            origin,
            score,
        from population
        order by score desc, timestamp desc
        """
    ).show()