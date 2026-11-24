CREATE TABLE IF NOT EXISTS wax_batches(
 code text PRIMARY KEY, fabric text NOT NULL,
 stage text NOT NULL DEFAULT 'sampling' CHECK(stage IN('sampling','sealed','classified','released','recheck'))
);
CREATE TABLE IF NOT EXISTS wax_swatches(
 batch text NOT NULL REFERENCES wax_batches(code), seam text NOT NULL,
 bench text NOT NULL CHECK(bench IN('A','B','C')), weave text NOT NULL,
 PRIMARY KEY(batch,seam)
);
