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
         "Neighbourhood": []}

clean_listings_data("../Dataset/barcelona_listings.csv")
