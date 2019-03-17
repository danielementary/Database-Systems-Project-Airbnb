
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
  city VARCHAR(50) NOT NULL,
  --a listing is in a neigbourhood
  neigbourhood_id INTEGER NOT NULL,

  ------------keys------------
  PRIMARY KEY(id),
  FOREIGN KEY(host_id)
      REFERENCES Host(host_id),
  FOREIGN KEY(city)
      REFERENCES City
  FOREIGN KEY(neigbourhood_id)
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

CREATE TABLE City(
  ---------attributes---------
  city VARCHAR(30),
  country_code INTEGER,
  country VARCHAR(30),
  -----relation attributes----
  ------------keys------------
  PRIMARY KEY(city)
)

CREATE TABLE House_properties(
  ---------attributes---------
  listing_id INTEGER,
  property_type VARCHAR(50),
  room_type VARCHAR(50),
  accomodates INTEGER,
  bathrooms INTEGER,
  bedrooms INTEGER,
  beds INTEGER,
  bed_type VARCHAR(50),
  amenities TEXT,
  square_feet INTEGER,

  -----relation attributes----
  ------------keys------------
  PRIMARY KEY(listing_id),
  FOREIGN KEY(listing_id)
    REFERENCES Listing

)

CREATE TABLE Economic_properties(
  ---------attributes---------
  listing_id INTEGER,
  price INTEGER,
  weekly_price INTEGER,
  monthly_price INTEGER,
  security_deposit INTEGER,
  cleaning_fee INTEGER,
  guests_included INTEGER,
  extra_people INTEGER,
  -----relation attributes----
  ------------keys------------
  PRIMARY KEY(listing_id),
  FOREIGN KEY(listing_id)
    REFERENCES Listing

)

CREATE TABLE Administrative_properties(
  ---------attributes---------
  -----relation attributes----
  ------------keys------------

)

CREATE TABLE Review(
  ---------attributes---------
  -----relation attributes----
  ------------keys------------

)

CREATE TABLE Reviewer(
  ---------attributes---------
  -----relation attributes----
  ------------keys------------
)

CREATE TABLE Reservation(
  ---------attributes---------
  -----relation attributes----
  ------------keys------------

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
