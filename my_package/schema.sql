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
  knowledge_base_id INTEGER NOT NULL,
  params TEXT NOT NULL,
  creation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  state TEXT NOT NULL,
  passcode TEXT NOT NULL,
  statistics TEXT NOT NULL,
  FOREIGN KEY (knowledge_base_id) REFERENCES generation_schemes (id)
);



