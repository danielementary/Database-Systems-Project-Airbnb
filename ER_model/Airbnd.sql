
----------------Entities-------------------

CREATE TABLE Listing(
  ---------attributes---------
  id INTEGER,
  listing_url VARCHAR(50),
  name VARCHAR(50),
  summary VARCHAR(50),
  space VARCHAR(50),
  description TEXT,
  notes TEXT,
  transit TEXT,
  access TEXT,
  interaction TEXT,
  picture_url VARCHAR(50)

  -----relation attributes----
  --a host owns a listing
  host_id INTEGER NOT NULL,
  --a listing is in a country
  country_code INTEGER NOT NULL,
  --a listing is in a neigbourhood
  neigbourhood VARCHAR(50) NOT NULL,

  ------------keys------------
  PRIMARY KEY(id),
  FOREIGN KEY(host_id)
      REFERENCES Host(host_id),
  FOREIGN KEY(country_code)
      REFERENCES Country
  FOREIGN KEY(neigbourhood)
      REFERENCES Neigbourhood


)

CREATE TABLE Host(
  ---------attributes---------
  host_id INTEGER,
  host_url VARCHAR(50),
  host_name VARCHAR(40),
  host_since DATE,
  host_about TEXT,
  host_response_time TIME,
  host_response_rate DECIMAL,
  host_thumbnail_url VARCHAR(50),
  host_picture_url VARCHAR(50),
  host_neigbourhood TEXT,
  host_verifications TEXT,
  -----relation attributes----

  ------------keys------------
  PRIMARY KEY(host_id)
)

CREATE TABLE Neigbourhood(
  neigbourhood_id INTEGER AUTO_INCREMENT,
  ---------attributes---------
  neigbourhood VARCHAR(50),
  neigbourhood_overview TEXT,
  -----relation attributes----
  ------------keys------------
  PRIMARY KEY(id)
)

CREATE TABLE Country(
  ---------attributes---------
  city VARCHAR(30),
  country_code INTEGER,
  country VARCHAR(30),
  -----relation attributes----
  ------------keys------------
  PRIMARY KEY(country_code)
)


----------------Relations------------------

CREATE TABLE Location(
  listing_id INTEGER,
  country_code INTEGER,
  latitude DECIMAL,
  longitude DECIMAL,

  ------------keys------------
  PRIMARY KEY(listing_id, country_code),
  FOREIGN KEY(listing_id)
      REFERENCES Listing(id)
  FOREIGN KEY(country_code)
      REFERENCES Country(country_code)
)

-- A mon avis elle n'est pas utile, vu qu'un listing ne peut avoir qu'un seul neigbourhood

-- CREATE TABLE NeigbourhoodLocation(
--   listing_id INTEGER,
--   neigbourhood VARCHAR(50), --peut avoir plusieurs neigbourhood par listing !
--   neigbourhood_overview TEXT,
--
--   ------------keys------------
--   PRIMARY KEY(listing_id, neigbourhood),
--   FOREIGN KEY(listing_id)
--       REFERENCES Listing(listing_id),
--   FOREIGN KEY(neigbourhood)
--       REFERENCES Neigbourhood(neigbourhood)
--
-- )
