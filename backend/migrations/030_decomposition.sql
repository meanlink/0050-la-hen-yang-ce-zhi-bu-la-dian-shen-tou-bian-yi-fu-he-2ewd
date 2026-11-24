CREATE TABLE IF NOT EXISTS wax_components(
 batch text PRIMARY KEY REFERENCES wax_batches(code),
 avg_depth numeric(6,4) NOT NULL,
 bench_variance numeric(8,5) NOT NULL CHECK(bench_variance>=0),
 seam_variance numeric(8,5) NOT NULL CHECK(seam_variance>=0),
 reading_variance numeric(8,5) NOT NULL CHECK(reading_variance>=0),
 requires_recheck bool NOT NULL,
 sums jsonb NOT NULL
);
