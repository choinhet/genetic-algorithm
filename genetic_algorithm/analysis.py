import duckdb

if __name__ == "__main__":
    conn = duckdb.connect("population.duckdb")
    conn.query(
        """
        select 
            timestamp,
            origin,
            avg(score) as avg_score,
        from population
        group by origin, timestamp
        order by timestamp, avg_score desc
        """
    ).show()
    conn.query(
        """
        select 
            origin,
            avg(score) as avg_score,
        from population
        group by origin
        order by avg_score desc
        """
    ).show()