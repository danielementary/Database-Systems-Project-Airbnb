create_table_Listing = """
CREATE TABLE Listing (
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
  accommodates TINYINT,
  bathrooms    TINYINT,
  bedrooms     TINYINT,
  beds         TINYINT,
  square_feet  SMALLINT,
  price            FLOAT,
  weekly_price     FLOAT,
  monthly_price    FLOAT,
  security_deposit FLOAT,
  cleaning_fee     FLOAT,
  guests_included  TINYINT,
  extra_people     INT,
  rules          TEXT,
  minimum_nights INT,
  maximum_nights INT,
  is_business_travel_ready         BIT,
  require_guest_profile_picture    BIT,
  require_guest_phone_verification BIT,
  review_scores_rating        FLOAT,
  review_scores_accuracy      FLOAT,
  review_scores_cleanliness   FLOAT,
  review_scores_checkin       FLOAT,
  review_scores_communication FLOAT,
  review_scores_location      FLOAT,
  review_scores_value         FLOAT,
  latitude  FLOAT,
  longitude FLOAT,
  host_id          INT NOT NULL,
  neighbourhood_id INT NOT NULL,
  property_type_id       INT,
  room_type_id           INT,
  bed_type_id            INT,
  cancellation_policy_id INT,
  PRIMARY KEY(listing_id),
  FOREIGN KEY(host_id)                REFERENCES Host(host_id)                   ON DELETE CASCADE,
  FOREIGN KEY(neighbourhood_id)       REFERENCES Neighbourhood(neighbourhood_id) ON DELETE CASCADE,
  FOREIGN KEY(property_type_id)       REFERENCES Property_type(property_type_id),
  FOREIGN KEY(room_type_id)           REFERENCES Room_type(room_type_id),
  FOREIGN KEY(bed_type_id)            REFERENCES Bed_type(bed_type_id),
  FOREIGN KEY(cancellation_policy_id) REFERENCES Cancellation_policy(cancellation_policy_id)
);"""

create_table_Host = """
CREATE TABLE Host (
  host_id    INT,
  host_url   TINYTEXT,
  host_name  TINYTEXT,
  host_since DATE,
  host_about TEXT,
  host_response_time TINYTEXT,
  host_response_rate TINYTEXT,
  host_thumbnail_url TINYTEXT,
  host_picture_url   TINYTEXT,
  neighbourhood_id INT NOT NULL,
  PRIMARY KEY(host_id),
  FOREIGN KEY(neighbourhood_id) REFERENCES Neighbourhood(neighbourhood_id)
);"""

create_table_Neighbourhood = """
CREATE TABLE Neighbourhood (
  neighbourhood_id   INT,
  neighbourhood_name TINYTEXT,
  city_id INT NOT NULL,
  PRIMARY KEY(neighbourhood_id),
  FOREIGN KEY(city_id) REFERENCES City(city_id) ON DELETE CASCADE
);"""

create_table_Property_type = """
CREATE TABLE Property_type (
  property_type_id   INT,
  property_type_name TINYTEXT NOT NULL,
  PRIMARY KEY(property_type_id)
);"""

create_table_Room_type = """
CREATE TABLE Room_type (
  room_type_id   INT,
  room_type_name TINYTEXT NOT NULL,
  PRIMARY KEY(room_type_id)
);"""

create_table_Bed_type = """
CREATE TABLE Bed_type (
  bed_type_id   INT,
  bed_type_name TINYTEXT NOT NULL,
  PRIMARY KEY(bed_type_id)
);"""

create_table_Cancellation_policy = """
CREATE TABLE Cancellation_policy (
  cancellation_policy_id   INT,
  cancellation_policy_name TEXT NOT NULL,
  PRIMARY KEY(cancellation_policy_id)
);"""

create_table_City = """
CREATE TABLE City (
  city_id   INT,
  city_name TINYTEXT NOT NULL,
  country_id INT NOT NULL,
  PRIMARY KEY(city_id),
  FOREIGN KEY(country_id) REFERENCES Country(country_id) ON DELETE CASCADE
);"""

create_table_Country = """
CREATE TABLE Country (
  country_id   INT,
  country_code VARCHAR(2) NOT NULL,
  country_name TINYTEXT,
  PRIMARY KEY(country_id)
);"""

create_table_Review = """
CREATE TABLE Review (
  review_id       INT,
  review_date     DATE,
  review_comments TEXT,
  reviewer_id INT NOT NULL,
  listing_id  INT NOT NULL,
  PRIMARY KEY(review_id),
  FOREIGN KEY(reviewer_id) REFERENCES Reviewer(reviewer_id) ON DELETE CASCADE,
  FOREIGN KEY(listing_id)  REFERENCES Listing(listing_id)   ON DELETE CASCADE
);"""

create_table_Reviewer = """
CREATE TABLE Reviewer (
  reviewer_id   INT,
  reviewer_name TINYTEXT,
  PRIMARY KEY(reviewer_id)
);"""

create_table_Calendar = """
CREATE TABLE Calendar (
  calendar_id        INT,
  calendar_available BIT NOT NULL,
  calendar_price     FLOAT,
  listing_id         INT NOT NULL,
  calendar_day_id    INT NOT NULL,
  PRIMARY KEY(calendar_id),
  FOREIGN KEY(listing_id)      REFERENCES Listing(listing_id) ON DELETE CASCADE,
  FOREIGN KEY(calendar_day_id) REFERENCES Day(day_id)         ON DELETE CASCADE
);"""

create_table_Day = """
CREATE TABLE Day (
  day_id   INT,
  day_date DATE NOT NULL,
  PRIMARY KEY(day_id)
);"""

create_table_Amenity = """
CREATE TABLE Amenity (
  amenity_id   INT,
  amenity_name TEXT NOT NULL,
  PRIMARY KEY(amenity_id)
);"""

create_table_Host_verification = """
CREATE TABLE Host_verification (
  host_verification_id          INT,
  host_verification_description TEXT NOT NULL,
  PRIMARY KEY(host_verification_id)
);"""

create_table_Listing_amenity_map = """
CREATE TABLE Listing_amenity_map (
  listing_id INT NOT NULL,
  amenity_id INT NOT NULL,
  PRIMARY KEY(listing_id, amenity_id),
  FOREIGN KEY(listing_id) REFERENCES Listing(listing_id) ON DELETE CASCADE,
  FOREIGN KEY(amenity_id) REFERENCES Amenity(amenity_id) ON DELETE CASCADE
);"""

create_table_Host_verification_map = """
CREATE TABLE Host_verification_map (
  host_id              INT NOT NULL,
  host_verification_id INT NOT NULL,
  PRIMARY KEY(host_id, host_verification_id),
  FOREIGN KEY(host_id)              REFERENCES Host(host_id)                           ON DELETE CASCADE,
  FOREIGN KEY(host_verification_id) REFERENCES Host_verification(host_verification_id) ON DELETE CASCADE
);"""

create_statements_ordered = [create_table_Country, create_table_City, create_table_Neighbourhood,
                             create_table_Host, create_table_Property_type, create_table_Room_type,
                             create_table_Bed_type, create_table_Cancellation_policy,
                             create_table_Listing, create_table_Reviewer, create_table_Review,
                             create_table_Day, create_table_Calendar, create_table_Amenity,
                             create_table_Host_verification, create_table_Listing_amenity_map,
                             create_table_Host_verification_map]
