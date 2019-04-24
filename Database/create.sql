CREATE DATABASE Airbnb;

CREATE TABLE Listing (

  ---------attributes---------
  listing_id          INT,
  listing_url         TINYTEXT,
  listing_name        TINYTEXT,
  listing_summary     TEXT,
  listing_space       TEXT,
  listing_description MEDIUMTEXT,
  listing_notes       TEXT,
  listing_transit     TEXT,
  listing_access      TEXT,
  listing_interaction TEXT,
  listing_picture_url TINYTEXT,
  listing_neighbourhood_overview TEXT,

  ------House_properties------
  accommodates TINYINT,
  bathrooms    TINYINT,
  bedrooms     TINYINT,
  beds         TINYINT,
  square_feet  SMALLINT,

  ----Economic_properties-----
  price            FLOAT,
  weekly_price     FLOAT,
  monthly_price    FLOAT,
  security_deposit FLOAT,
  cleaning_fee     FLOAT,
  guests_included  TINYINT,
  extra_people     INT,

  --Administrative_properties-
  rules          TEXT,
  minimum_nights INT,
  maximum_nights INT,
  is_business_travel_ready         BIT,
  require_guest_profile_picture    BIT,
  require_guest_phone_verification BIT,

  -------Review_scores--------
  review_scores_rating        FLOAT,
  review_scores_accuracy      FLOAT,
  review_scores_cleanliness   FLOAT,
  review_scores_checkin       FLOAT,
  review_scores_communication FLOAT,
  review_scores_location      FLOAT,
  review_scores_value         FLOAT,

  ----------Location----------
  latitude  FLOAT,
  longitude FLOAT,

  -----relation attributes----
  host_id          INT NOT NULL,
  neighbourhood_id INT NOT NULL,

  property_type_id       INT,
  room_type_id           INT,
  bed_type_id            INT,
  cancellation_policy_id INT,

  ------------keys------------
  PRIMARY KEY(listing_id),
  FOREIGN KEY(host_id)                REFERENCES Host(host_id)                   ON DELETE CASCADE,
  FOREIGN KEY(neighbourhood_id)       REFERENCES Neighbourhood(neighbourhood_id) ON DELETE CASCADE,
  FOREIGN KEY(property_type_id)       REFERENCES Property_type(property_type_id),
  FOREIGN KEY(room_type_id)           REFERENCES Room_type(room_type_id),
  FOREIGN KEY(bed_type_id)            REFERENCES Bed_type(bed_type_id),
  FOREIGN KEY(cancellation_policy_id) REFERENCES Cancellation_policy(cancellation_policy_id)
);

CREATE TABLE Host (

  ---------attributes---------
  host_id    INT,
  host_url   TINYTEXT,
  host_name  TINYTEXT,
  host_since DATE,
  host_about TEXT,
  host_response_time TINYTEXT,
  host_response_rate TINYTEXT,
  host_thumbnail_url TINYTEXT,
  host_picture_url   TINYTEXT,

  -----relation attributes----
  neighbourhood_id INT,

  ------------keys------------
  PRIMARY KEY(host_id),
  FOREIGN KEY(neighbourhood_id) REFERENCES Neighbourhood(neighbourhood_id)
);

CREATE TABLE Neighbourhood (

  ---------attributes---------
  neighbourhood_id   INT,
  neighbourhood_name TINYTEXT,

  -----relation attributes----
  city_id INT NOT NULL,

  ------------keys------------
  PRIMARY KEY(neighbourhood_id),
  FOREIGN KEY(city_id) REFERENCES City(city_id) ON DELETE CASCADE
);

CREATE TABLE Property_type (

  ---------attributes---------
  property_type_id   INT,
  property_type_name TINYTEXT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(property_type_id)
);

CREATE TABLE Room_type (

  ---------attributes---------
  room_type_id   INT,
  room_type_name TINYTEXT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(room_type_id)
);

CREATE TABLE Bed_type (

  ---------attributes---------
  bed_type_id   INT,
  bed_type_name TINYTEXT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(bed_type_id)
);

CREATE TABLE Cancellation_policy (

  ---------attributes---------
  cancellation_policy_id          INT,
  cancellation_policy_description TEXT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(cancellation_policy_id)
);

CREATE TABLE City (

  ---------attributes---------
  city_id   INT,
  city_name TINYTEXT NOT NULL,

  -----relation attributes----
  country_id INT NOT NULL,

  ------------keys------------
  PRIMARY KEY(city_id),
  FOREIGN KEY(country_id) REFERENCES Country(country_id) ON DELETE CASCADE
);

CREATE TABLE Country (

  ---------attributes---------
  country_id   INT,
  country_code VARCHAR(2) NOT NULL,
  country_name TINYTEXT,

  ------------keys------------
  PRIMARY KEY(country_id)
);

CREATE TABLE Review (

  ---------attributes---------
  review_id       INT,
  review_date     DATE,
  review_comments TEXT,

  -----relation attributes----
  reviewer_id INT NOT NULL,
  listing_id  INT NOT NULL,

  ------------keys------------
  PRIMARY KEY(review_id),
  FOREIGN KEY(reviewer_id) REFERENCES Reviewer(reviewer_id) ON DELETE CASCADE,
  FOREIGN KEY(listing_id)  REFERENCES Listing(listing_id)   ON DELETE CASCADE
);

CREATE TABLE Reviewer (

  ---------attributes---------
  reviewer_id   INT,
  reviewer_name TINYTEXT,

  ------------keys------------
  PRIMARY KEY(reviewer_id)
);

CREATE TABLE Calendar (

  ---------attributes---------
  calendar_id        INT,
  calendar_available BIT   NOT NULL,
  calendar_price     FLOAT NOT NULL,

  -----relation attributes----
  listing_id INT NOT NULL,
  calendar_day_id      INT  NOT NULL,

  ------------keys------------
  PRIMARY KEY(calendar_id),
  FOREIGN KEY(listing_id) REFERENCES Listing(listing_id) ON DELETE CASCADE,
  FOREIGN KEY(calendar_day_id) REFERENCES Day(day_id)
);

CREATE TABLE Day (
  ---------attributes---------
  day_id        INT,
  day_date      DATE  NOT NULL,
)

CREATE TABLE Amenity (

  ---------attributes---------
  amenity_id   INT,
  amenity_name TEXT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(amenity_id)
);

CREATE TABLE Host_verification (

  ---------attributes---------
  host_verification_id          INT,
  host_verification_description TEXT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(host_verification_id)
);

CREATE TABLE Listing_amenity_map (

  ---------attributes---------
  -----relation attributes----
  listing_id INT NOT NULL,
  amenity_id INT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(listing_id, amenity_id),
  FOREIGN KEY(listing_id) REFERENCES Listing(listing_id) ON DELETE CASCADE,
  FOREIGN KEY(amenity_id) REFERENCES Amenity(amenity_id) ON DELETE CASCADE
);

CREATE TABLE Host_verification_map (

  ---------attributes---------
  -----relation attributes----
  host_id              INT NOT NULL,
  host_verification_id INT NOT NULL,

  ---------keys---------------
  PRIMARY KEY(host_id, host_verification_id),
  FOREIGN KEY(host_id)              REFERENCES Host(host_id)                           ON DELETE CASCADE,
  FOREIGN KEY(host_verification_id) REFERENCES Host_verification(host_verification_id) ON DELETE CASCADE
);
