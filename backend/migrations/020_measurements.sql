CREATE TABLE IF NOT EXISTS wax_readings(
 batch text NOT NULL, seam text NOT NULL,
 pass int NOT NULL CHECK(pass IN(1,2)),
 depth numeric(5,2) NOT NULL CHECK(depth BETWEEN 0 AND 8),
 PRIMARY KEY(batch,seam,pass),
 FOREIGN KEY(batch,seam) REFERENCES wax_swatches(batch,seam)
);
