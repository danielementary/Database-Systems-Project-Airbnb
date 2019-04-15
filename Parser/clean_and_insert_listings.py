import pandas as pd
import numpy as np
import math


def clean_listings_data(filename):

    string_attributes = ['listing_url', 'name', 'summary',"space", "description", "notes",\
                        "transit","access","interaction","picture_url","neighbourhood_overview", "neighbourhood",\
                        "host_url", "host_name", "host_about", "host_thumbnail_url", "host_picture_url", \
                        "host_verifications", "property_type", "room_type", "bed_type",\
                        "amenities", "house_rules", "cancellation_policy", "city", "country"]
    bit_attributes = ['is_business_travel_ready', 'require_guest_profile_picture', 'require_guest_phone_verification']

    date_attributes = ["review_date", "host_since"]

    int_attributes = ['id', 'host_id', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'square_feet', 'guests_included',\
                        'minimum_nights', 'maximum_nights']

    data_types = {}
    for a in string_attributes:
        data_types[a] = str

    file = open(filename, newline='')
    df = pd.read_csv(filename, dtype=data_types)

    #rename neighborhood_overview to neighboUrhood_overview to be consistent
    df = df.rename(columns = {'neighborhood_overview': 'neighbourhood_overview'})

    columns = df.columns.tolist()

    # add quotes arround every string typed attributes
    for a in string_attributes:
        df[a] = df[a].apply(cleanString)

    # replace f or t for Bit typed attributes
    for a in bit_attributes:
        df[a] = df[a].apply(replace_f_t_by_bit)

    return df

def cleanString(string):
    string = str(string)

    #remove ' if surrounding the string
    if string != "":
        if string[0] == "'":
            string = string[1:]
        if string[-1] == "'":
            string = string[:-1]
        #put a quote before every quotes appearing in the string to escape it
        string = string.replace("'", "''")

        #add surrounding quotes
        string = "'" + string.strip() + "'"
    return string

def replace_f_t_by_bit(obj):
    f_t = str(obj)
    if(f_t == 't'):
        return 1
    return 0


def create_insert_queries(filename):


    tables = ["Listing", "Host", "Neighbourhood", "City", "Country", "Property_type",\
        "Room_type", "Bed_type", "Amenities", "Cancellation_policy", "Host_verifications"]

    #city of host_neighbourhood: say for now that is the same as the listing's
    # don't forget to add neighbourhood to the Table when insert host and listing
    # need to keeps tracks of neighbourhood already added
    #NEIGHBOURHOOD is special so does NOT have a dictionary
    tables_to_attributes = \
        {"Listing": {"listing_id": "id", "listing_url": "listing_url", "listing_name": "name", "listing_summary": "summary", "listing_space": "space", "listing_description": "description", "listing_notes": "notes", "listing_transit": "transit", "listing_access": "access", "listing_interaction": "interaction","listing_picture_url": "picture_url", "listing_neighbourhood_overview" : "neighbourhood_overview", "host_id": "host_id",\
         "price": "price", "weekly_price": "weekly_price", "monthly_price": "monthly_price", "security_deposit": "security_deposit", "cleaning_fee": "cleaning_fee", "guests_included": "guests_included", "extra_people": "extra_people",\
         "accomodates": "accomodates", "bathrooms": "bathrooms", "bedrooms": "bedrooms", "beds": "beds", "square_feet": "square_feet",\
         "rules": "house_rules", "minimum_nights": "minimum_nights", "maximum_nights": "maximum_nights", "is_business_travel_ready": "is_business_travel_ready", "require_guest_profile_picture": "require_guest_profile_picture", "require_guest_phone_verification": "require_guest_phone_verification",\
         "review_scores_rating": "review_scores_rating", "review_scores_accuracy": "review_scores_accuracy", "review_scores_cleanliness": "review_scores_cleanliness", "review_scores_checkin": "review_scores_checkin", "review_scores_communication": "review_scores_communication", "review_scores_location": "review_scores_location", "review_scores_value": "review_scores_value",\
         "latitude": "latitude", "longitude": "longitude"},\
         "Host": {"host_id" : "host_id", "host_url" : "host_url", "host_name" : "host_name", "host_since" : "host_since", "host_about" : "host_about", "host_response_time" : "host_response_time", "host_response_rate" : "host_response_rate", "host_thumbnail_url" : "host_thumbnail_url", "host_picture_url" : "host_picture_url", "host_verifications" : "host_verifications", "neighbourhood_name": "host_neighbourhood", "city_name": "city"},\
         "Neighbourhood": ["neighbourhood_name", "city_name", "country_code"],\
         "City": {"city_name": "city", "country_id": "country_id",\
         "Location": {"latitude": "latitude", "longitude": "longitude", "listing_id": "id", "neighbourhood_name": "neighbourhood", "city_name": "city"}}}

    # use something like INSERT INTO `BITTESTTABLE` VALUES('XYZ', b'0');
    # to insert bit values

    # use math.isnan(x) to check if float is NaN value before convert to int

    df = clean_listings_data(filename)

    norm_tables = {}
    #First add all distincts normalization's tables' elements
    property_types = df["property_type"]
    property_types = property_types.drop_duplicates()
    cleaned = [cleanString(i) for i in property_types.tolist()]
    property_types_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in property_types_dict.keys():
        query = """INSERT INTO Property_type VALUES ({}, {});""".format(property_types_dict[typ], typ)

    room_types = df["room_type"]
    room_types = room_types.drop_duplicates()
    cleaned = [cleanString(i) for i in room_types.tolist()]
    room_types_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in room_types_dict.keys():
        query = """INSERT INTO Room_type VALUES ({}, {});""".format(room_types_dict[typ], typ)

    bed_types = df["bed_type"]
    bed_types = bed_types.drop_duplicates()
    cleaned = [cleanString(i) for i in bed_types.tolist()]
    bed_types_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in bed_types_dict.keys():
        query = """INSERT INTO Bed_type VALUES ({}, {});""".format(bed_types_dict[typ], typ)

    amenities = df["amenities"]
    amenities = amenities.drop_duplicates()
    amenities_list = extract_amenities(amenities)
    amenities_dict = dict(list(zip(amenities_list, range(len(amenities_list)))))
    for amenity in amenities_dict.keys():
        query = """INSERT INTO Amenity VALUES ({}, {});""".format(amenities_dict[amenity], amenity)

    cancellation_policy = df["cancellation_policy"]
    cancellation_policy = cancellation_policy.drop_duplicates()
    cleaned = [cleanString(i) for i in cancellation_policy.tolist()]
    cancellation_policy_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in cancellation_policy_dict.keys():
        query = """INSERT INTO Cancellation_policy VALUES ({}, {});""".format(cancellation_policy_dict[typ], typ)

    host_verifications = df["host_verifications"]
    host_verifications = host_verifications.drop_duplicates()
    host_verifications_list = extract_host_verifications(host_verifications)
    print(host_verifications_list)
    host_verifications_dict = dict(list(zip(host_verifications_list, range(len(host_verifications_list)))))
    for typ in host_verifications_dict.keys():
        query = """INSERT INTO Host_verification VALUES ({}, {});""".format(host_verifications_dict[typ], typ)




    

def extract_amenities(amns):
    res = []
    for ams_str in amns:
        ams_str = str(ams_str)
        ams = ams_str.split(",")
        ams = [a.replace("{", "") for a in ams]
        ams = [a.replace("}", "") for a in ams]
        ams = [a.replace('"', "") for a in ams]
        ams = [cleanString(i) for i in ams]
        res += ams
    res = list(set(res))
    cleaned = []
    for am in res:
        if "translation missing:" not in am and am != "":
            cleaned.append(am)

    return cleaned

def extract_host_verifications(hvers):
    res = []
    for hvers_str in hvers:
        hvers_str = str(hvers_str)
        hverfs = hvers_str.split(",")
        hverfs = [a.replace("[", "") for a in hverfs]
        hverfs = [a.replace("]", "") for a in hverfs]
        hverfs = [a.replace("'", "") for a in hverfs]
        hverfs = [cleanString(i) for i in hverfs]
        res += hverfs
    res = list(set(res))
    cleaned = []
    for hverf in res:
        if hverf != "":
            cleaned.append(hverf)

    return cleaned



create_insert_queries("../Dataset/barcelona_listings.csv")
