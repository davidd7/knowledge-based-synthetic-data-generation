DROP TABLE IF EXISTS generation_schemes;
DROP TABLE IF EXISTS post;

CREATE TABLE generation_schemes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  module_name TEXT NOT NULL,
  data TEXT NOT NULL
);

CREATE TABLE generation_jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  scheme_id INTEGER NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  state TEXT NOT NULL,
  FOREIGN KEY (scheme_id) REFERENCES generation_schemes (id)
); /* Question: should data / module_name also be saved here, because schemes might change? Or is at least data not importsant, because that data is also stored in ontology anyway after this db entry is created? */



