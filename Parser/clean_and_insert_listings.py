import pandas as pd
import numpy as np


def clean_listings_data(filename):
    file = open(filename, newline='')
    df = pd.read_csv(filename)

    #rename neighborhood_overview to neighboUrhood_overview to be consistent
    df = df.rename(columns = {'neighborhood_overview': 'neighbourhood_overview'})

    string_attributes = ['listing_url', 'name', 'summary',"space", "description", "notes",\
                        "transit","access","interaction","picture_url","neighbourhood_overview", "neighbourhood",\
                        "host_url", "host_name", "host_about", "host_thumbnail_url", "host_picture_url", \
                        "host_verifications", "property_type", "room_type", "bed_type",\
                        "amenities", "house_rules", "cancellation_policy", "city", "country"]
    bit_attributes = ['is_business_travel_ready', 'require_guest_profile_picture', 'require_guest_phone_verification']

    date_attributes = ["review_date", "host_since"]

    int_attributes = ['id', 'host_id', 'accomodates', 'bathrooms', 'bedrooms', 'beds', 'square_feet', 'guests_included',\
                        'minimum_nights', 'maximum_nights']

    columns = df.columns.tolist()

    # add quotes arround every string typed attributes
    for a in string_attributes:
        df[a] = df[a].apply(addQuotes)

    # replace f or t for Bit typed attributes
    for a in bit_attributes:
        df[a] = df[a].apply(replace_f_t_by_bit)


    print(df['host_since'])


def create_insert_queries(filename):


    tables = ["Listing", "Host", "Neighbourhood", "House_properties",\
                "Economic_properties", "Administrative_properties",\
                "Review_scores", "City", "Location"]

    #city of host_neighbourhood: say for now that is the same as the listing's
    # don't forget to add neighbourhood to the Table when insert host and listing
    # need to keeps tracks of neighbourhood already added
    #NEIGHBOURHOOD is special so does NOT have a dictionary
    tables_to_attributes = \
        {"Listing": {"listing_id": "id", "listing_url": "listing_url", "listing_name": "name", "listing_summary": "summary", "listing_space": "space", "listing_description": "description", "listing_notes": "notes", "listing_transit": "transit", "listing_access": "access", "listing_interaction": "interaction","listing_picture_url": "picture_url", "listing_neighbourhood_overview" : "neighbourhood_overview", "host_id": "host_id"},\
         "Host": {"host_id" : "host_id", "host_url" : "host_url", "host_name" : "host_name", "host_since" : "host_since", "host_about" : "host_about", "host_response_time" : "host_response_time", "host_response_rate" : "host_response_rate", "host_thumbnail_url" : "host_thumbnail_url", "host_picture_url" : "host_picture_url", "host_verifications" : "host_verifications", "neighbourhood_name": "host_neighbourhood", "city_name": "city"},\
         "Neighbourhood": ["neighbourhood_name", "city_name", "country_code"],\
         "House_properties": {"property_type": "property_type", "room_type": "room_type", "accomodates": "accomodates", "bathrooms": "bathrooms", "bedrooms": "bedrooms", "beds": "beds", "bed_type": "bed_type", "amenities":  "amenities", "square_feet": "square_feet", "listing_id": "id"}, \
         "Economic_properties": {"price": "price", "weekly_price": "weekly_price", "monthly_price": "monthly_price", "security_deposit": "security_deposit", "cleaning_fee": "cleaning_fee", "guests_included": "guests_included", "extra_people": "extra_people", "listing_id": "id"},\
         "Administrative_properties": {"rules": "house_rules", "minimum_nights": "minimum_nights", "maximum_nights": "maximum_nights", "is_business_travel_ready": "is_business_travel_ready", "cancellation_policy":  "cancellation_policy", "require_guest_profile_picture": "require_guest_profile_picture", "require_guest_phone_verification": "require_guest_phone_verification", "listing_id": "id"},\
         "Review_scores": {"review_scores_rating": "review_scores_rating", "review_scores_accuracy": "review_scores_accuracy", "review_scores_cleanliness": "review_scores_cleanliness", "review_scores_checkin": "review_scores_checkin", "review_scores_communication": "review_scores_communication", "review_scores_location": "review_scores_location", "review_scores_value": "review_scores_value", "listing_id": "id"},\
         "City": {"city_name": "city", "country_code": "country_code", "country": "country",\
         "Location": {"latitude": "latitude", "longitude": "longitude", "listing_id": "id", "neighbourhood_name": "neighbourhood", "city_name": "city"}}}

    # use something like INSERT INTO `BITTESTTABLE` VALUES('XYZ', b'0');
    # to insert bit values



def addQuotes(string):
    string = str(string)
    return string

def replace_f_t_by_bit(obj):
    f_t = str(obj)
    if(f_t == 't'):
        return 1
    return 0

clean_listings_data("../Dataset/barcelona_listings.csv")
