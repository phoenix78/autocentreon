CREATE TABLE IF NOT EXISTS hosts (
  id SERIAL UNIQUE NOT NULL,
  hostname varchar UNIQUE NOT NULL,
  alias varchar DEFAULT '',
  templates varchar NOT NULL DEFAULT '[]',
  groups varchar DEFAULT '[]',
  categories varchar DEFAULT '[]',
  longitude varchar DEFAULT '0',
  latitude varchar DEFAULT '0',
  poller varchar
  PRIMARY KEY (product_id)
);