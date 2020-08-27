DROP TABLE IF EXISTS dictionary;

CREATE TABLE dictionary (
  key TEXT PRIMARY KEY NOT NULL,
  value TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
