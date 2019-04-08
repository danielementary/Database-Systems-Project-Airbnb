import pandas as pd
import numpy as np


def clean_listings_data(filename):
    file = open(filename, newline='')
    data_frame = pd.read_csv(filename)

    print(data_frame.columns)


def create_insert_queries(filename):
    file = open(filename, newline='')
    data_frame = pd.read_csv(filename)

    tables = ["Listing", "Host", "Neighbourhood", "House_properties",\
                "Economic_properties", "Administrative_properties",\
                "Review_scores", "City", "Location"]

    tables_to_attributes = \
        {"Listing": ["listing_id", "listing_url", "listing_name", "listing_summary", "listing_space", "listing_description", "listing_notes", "listing_transit", "listing_access", "listing_interaction", "host_id"],\
         "Host": ["host_id", "host_url"", ""host_name", "host_since", "host_about", "host_response_time", "host_response_rate", "host_thumbnail_url", "host_picture_url", "host_verifications", "neighbourhood_name", "city_name"],\
         "Neighbourhood": ["neighbourhood_name", "city_name", "country_code"],\
         "House_properties": ["property_type", "room_type", "accomodates", "bathrooms", "bedrooms", "beds", "bed_type", "amenities", "square_feet", "listing_id"], \
         "Economic_properties": ["price", "weekly_price", "monthly_price", "security_deposit", "cleaning_fee", "guests_included", "extra_people", "listing_id"],\
         "Administrative_properties": ["rules", "minimum_nights", "maximum_nights", "is_business_travel_ready", "cancellation_policy", "require_guest_profile_picture", "require_guest_phone_verification", "listing_id"],\
         "Review_scores": ["review_scores_rating", "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin", "review_scores_communication", "review_scores_location", "review_scores_value", "listing_id"],\
         "City": ["city_name", "country_code", "country",\
         "Location": ["latitude", "longitude", "listing_id", "neighbourhood_name", "city_name"]]}

clean_listings_data("../Dataset/barcelona_listings.csv")
