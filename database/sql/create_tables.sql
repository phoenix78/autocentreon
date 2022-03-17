CREATE TABLE IF NOT EXISTS products (
  product_id SERIAL UNIQUE NOT NULL,
  name varchar(250) UNIQUE NOT NULL,
  description varchar(250) DEFAULT '',
  stock_quantity INT DEFAULT 0,
  is_present varchar(250) DEFAULT false,
  PRIMARY KEY (product_id)
);


CREATE TABLE IF NOT EXISTS receipts (
  receipt_id SERIAL UNIQUE NOT NULL,
  ingredient varchar(250) NOT NULL,
  user_id INT NOT NULL,
  product_id INT NOT NULL, 
  PRIMARY KEY (receipt_id),
  CONSTRAINT fk_product
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id)
);

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