CREATE TABLE IF NOT EXISTS wax_dispatch(
 batch text PRIMARY KEY REFERENCES wax_components(batch),
 decision text NOT NULL CHECK(decision IN('release','recheck')),
 destination text NOT NULL,
 note text NOT NULL CHECK(length(note)>=6),
 manager text NOT NULL
);
