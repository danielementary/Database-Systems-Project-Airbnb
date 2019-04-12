CREATE DATABASE Airbnb;

----------------Entities-------------------

CREATE TABLE Listing (

  ---------attributes---------
  listing_id          INT,
  listing_url         TINYTEXT,
  listing_name        TINYTEXT,
  listing_summary     TINYTEXT,
  listing_space       TINYTEXT,
  listing_description TEXT,
  listing_notes       TEXT,
  listing_transit     TEXT,
  listing_access      TEXT,
  listing_interaction TEXT,
  listing_picture_url TINYTEXT,
  listing_neighbourhood_overview TEXT,

  -- House_properties
  property_type TINYTEXT,
  room_type     TINYTEXT,
  accommodates  TINYINT,
  bathrooms     TINYINT,
  bedrooms      TINYINT,
  beds          TINYINT,
  bed_type      TINYTEXT,
  amenities     TEXT,
  square_feet   SMALLINT,

  -- Economic_properties
  price            FLOAT,
  weekly_price     FLOAT,
  monthly_price    FLOAT,
  security_deposit FLOAT,
  cleaning_fee     FLOAT,
  guests_included  TINYINT,
  extra_people     FLOAT,

  -- Administrative_properties
  rules          TEXT,
  minimum_nights INT,
  maximum_nights INT,
  is_business_travel_ready BIT,
  cancellation_policy      TEXT,
  require_guest_profile_picture    BIT,
  require_guest_phone_verification BIT,

  -- Review_scores
  review_scores_rating        FLOAT,
  review_scores_accuracy      FLOAT,
  review_scores_cleanliness   FLOAT,
  review_scores_checkin       FLOAT,
  review_scores_communication FLOAT,
  review_scores_location      FLOAT,
  review_scores_value         FLOAT,

  -- Location
  latitude         FLOAT,
  longitude        FLOAT,

  -----relation attributes----
  host_id           INT NOT NULL,
  neighbourhood_id  INT NOT NULL,

  ------------keys------------
  PRIMARY KEY(id),
  FOREIGN KEY(host_id) REFERENCES Host(host_id),
  FOREIGN KEY(neighbourhood_id) REFERENCES Neighbourhood(neighbourhood_id)
);

CREATE TABLE Host (

  ---------attributes---------
  host_id    INT,
  host_url   TINYTEXT,
  host_name  TINYTEXT,
  host_since DATE,
  host_about TINYTEXT,
  host_response_time TIME,
  host_response_rate FLOAT,
  host_thumbnail_url TINYTEXT,
  host_picture_url   TINYTEXT,
  host_verifications TEXT,

  -----relation attributes----
  neighbourhood_name TINYTEXT,
  city_name          TINYTEXT,

  ------------keys------------
  PRIMARY KEY(host_id),
  FOREIGN KEY(neighbourhood_id) REFERENCES Neighbourhood(neighbourhood_id)
);

CREATE TABLE Neighbourhood (

  ---------attributes---------
  neighbourhood_id   INT,
  neighbourhood_name TINYTEXT,

  -----relation attributes----
  city_name    TINYTEXT,
  country_code VARCHAR(4),

  ------------keys------------
  PRIMARY KEY(neighbourhood_id)
  FOREIGN KEY(city_id) REFERENCES City(city_id) ON DELETE CASCADE
);

CREATE TABLE Review (

  ---------attributes---------
  review_id   INT,
  review_date DATE,
  review_comments TEXT,

  -----relation attributes----
  reviewer_id INT,
  listing_id  INT,

  ------------keys------------
  PRIMARY KEY(review_id),
  FOREIGN KEY(reviewer_id) REFERENCES Reviewer(reviewer_id),
  FOREIGN KEY(listing_id) REFERENCES Listing(listing_id)
);

CREATE TABLE Reviewer (

  ---------attributes---------
  reviewer_id   INT,
  reviewer_name TINYTEXT,
  -----relation attributes----

  ------------keys------------
  PRIMARY KEY(reviewer_id)
);


CREATE TABLE Calendar (

  ---------attributes---------
  calendar_date      DATE,
  calendar_available BIT,
  calendar_price     FLOAT,

  -----relation attributes----
  listing_id INT,

  ------------keys------------
  PRIMARY KEY(listing_id, date),
  FOREIGN KEY(listing_id) REFERENCES Listing(listing_id)
);

CREATE TABLE City (

  ---------attributes---------
  city_id      INT,
  city_name    TINYTEXT,
  country_code VARCHAR(4),
  country      TINYTEXT,

  -----relation attributes----


  ------------keys------------
  PRIMARY KEY(city_id)
);

----------------Relations------------------

CREATE TABLE Location (

  ---------attributes---------
  latitude  FLOAT,
  longitude FLOAT,

  -----relation attributes----
  listing_id         INT,
  neighbourhood_id   INT,

  ------------keys------------
  PRIMARY KEY(listing_id),
  FOREIGN KEY(listing_id) REFERENCES Listing(listing_id) ON CASCADE DELETE,
  FOREIGN KEY(neighbourhood_id REFERENCES Neighbourhood(neighbourhood_id) ON CASCADE DELETE
);
