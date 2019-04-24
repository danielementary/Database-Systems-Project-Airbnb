import pandas as pd
import numpy as np
import math

temp_review_file = "temp/temp_reviews_"
temp_calendar_file = "temp/temp_calendar_"


tables_to_attributes = \
    {"Listing": {"listing_id": "id", "listing_url": "listing_url", "listing_name": "name", "listing_summary": "summary", "listing_space": "space", "listing_description": "description", "listing_notes": "notes", "listing_transit": "transit", "listing_access": "access", "listing_interaction": "interaction","listing_picture_url": "picture_url", "listing_neighbourhood_overview" : "neighbourhood_overview",\
     "accommodates": "accommodates", "bathrooms": "bathrooms", "bedrooms": "bedrooms", "beds": "beds", "square_feet": "square_feet",\
     "price": "price", "weekly_price": "weekly_price", "monthly_price": "monthly_price", "security_deposit": "security_deposit", "cleaning_fee": "cleaning_fee", "guests_included": "guests_included", "extra_people": "extra_people",\
     "rules": "house_rules", "minimum_nights": "minimum_nights", "maximum_nights": "maximum_nights", "ess_travel_ready": "is_business_travel_ready", "require_guest_profile_picture": "require_guest_profile_picture", "require_guest_phone_verification": "require_guest_phone_verification",\
     "review_scores_rating": "review_scores_rating", "review_scores_accuracy": "review_scores_accuracy", "review_scores_cleanliness": "review_scores_cleanliness", "review_scores_checkin": "review_scores_checkin", "review_scores_communication": "review_scores_communication", "review_scores_location": "review_scores_location", "review_scores_value": "review_scores_value",\
     "latitude": "latitude", "longitude": "longitude",\
     "host_id": "host_id", "neighbourhood_id": "neighbourhood_id", "property_type_id": "property_type_id", "room_type_id": "room_type_id", "bed_type_id": "bed_type_id", "cancellation_policy_id": "cancellation_policy_id"},\
     "Host": {"host_id" : "host_id", "host_url" : "host_url", "host_name" : "host_name", "host_since" : "host_since", "host_about" : "host_about", "host_response_time" : "host_response_time", "host_response_rate" : "host_response_rate", "host_thumbnail_url" : "host_thumbnail_url", "host_picture_url" : "host_picture_url", "neighbourhood_id": "neighbourhood_id"},\
     "Neighbourhood": {"neighbourhood_id":"neighbourhood_id", "neighbourhood_name":"neighbourhood_name","city_id": "city_id"},\
     "City": {"city_id": "city_id", "city_name": "city", "country_id": "country_id"},\
     "Property_type": {"property_type_id": "property_type_id", "property_type_name": "property_type_name"}, \
     "Room_type" : {"room_type_id": "room_type_id", "room_type_name": "room_type_name"},\
     "Bed_type": {"bed_type_id": "bed_type_id", "bed_type_name": "bed_type_name"},\
     "Cancellation_policy": {"cancellation_policy_id": "cancellation_policy_id", "cancellation_policy_name": "cancellation_policy_name"},\
     "Country": {"country_id": "country_id", "country_code": "country_code", "country_name": "country_name"},\
     "Amenity": {"amenity_id": "amenity_id", "amenity_name": "amenity_name"},\
     "Host_verification": {"host_verification_id": "host_verification_id", "host_verification_description": "host_verification_description"},\
     "Listing_amenity_map": {"listing_id": "listing_id", "amenity_id": "amenity_id"},\
     "Host_verification_map" :{"host_id": "host_id", "host_verification_id": "host_verification_id"}}

def clean_listings_data(filenames_list):

    string_attributes = ['listing_url', 'name', 'summary', "space", "description", "notes",\
                        "transit", "access", "interaction","picture_url", "neighbourhood_overview", "neighbourhood",\
                        "host_url", "host_name", "host_about", "host_thumbnail_url", "host_picture_url", "host_response_time", \
                        "host_verifications", "property_type", "room_type", "bed_type",\
                        "amenities", "house_rules", "cancellation_policy", "city", "country"]
    bit_attributes = ['is_business_travel_ready', 'require_guest_profile_picture', 'require_guest_phone_verification']

    date_attributes = ["review_date", "host_since"]

    int_attributes = ['id', 'host_id', 'accommodates', 'bathrooms', 'bedrooms', 'beds', 'square_feet', 'guests_included',\
                        "extra_people", 'minimum_nights', 'maximum_nights']
    float_attributes = ["price","weekly_price","monthly_price","security_deposit",\
                        "cleaning_fee","review_scores_rating","review_scores_accuracy",\
                        "review_scores_cleanliness","review_scores_checkin",\
                        "review_scores_communication","review_scores_location",\
                        "review_scores_value", "latitude", "longitude"]

    data_types = {}
    for a in string_attributes:
        data_types[a] = str
    df = pd.DataFrame()

    offset_listing_id = 0
    offset_hosts_id = 0

    for filename in filenames_list:
        city = filename.split(".")[-2].split("/")[-1].split("_")[0].lower().capitalize()
        print(city)

        df_per_city = pd.read_csv(filename, dtype=data_types)
        df_per_city["city"] = city

        # replace all listing_ids by new ones
        all_list_id = df_per_city["id"].tolist()
        new_listing_id_dict = dict(zip(all_list_id, range(len(all_list_id))))
        for i in list(new_listing_id_dict.keys()):
            new_listing_id_dict[i] += offset_listing_id

        # now change them and in reviews and calendar file too
        df_per_city["id"] = df_per_city["id"].apply(lambda x: replace_elements(x, new_listing_id_dict))

        reviews_df = pd.read_csv("../Dataset/Provided/"+city.lower()+"_reviews.csv")
        reviews_df["listing_id"] = reviews_df["listing_id"].apply(lambda x: replace_elements(x, new_listing_id_dict))
        reviews_df.to_csv(temp_review_file + city + ".csv")

        reviews_df = pd.read_csv("../Dataset/Provided/"+city.lower()+"_calendar.csv")
        reviews_df["listing_id"] = reviews_df["listing_id"].apply(lambda x: replace_elements(x, new_listing_id_dict))
        reviews_df.to_csv(temp_calendar_file + city + ".csv")

        offset_listing_id += len(all_list_id) + 1

        #replace all host_ids by new ones
        all_hosts_id = df_per_city["host_id"].tolist()
        new_hosts_id_dict = dict(zip(all_hosts_id, range(len(all_hosts_id))))
        for i in list(new_hosts_id_dict.keys()):
            new_hosts_id_dict[i] += offset_hosts_id

        df_per_city["host_id"] = df_per_city["host_id"].apply(lambda x: replace_elements(x, new_hosts_id_dict))

        offset_hosts_id += len(all_hosts_id) + 1


        df = df.append(df_per_city)

    #rename neighborhood_overview to neighboUrhood_overview to be consistent
    df = df.rename(columns = {'neighborhood_overview': 'neighbourhood_overview'})

    columns = df.columns.tolist()

    # add quotes arround every string typed attributes
    for a in string_attributes:
        df[a] = df[a].apply(cleanString)

    # replace f or t for Bit typed attributes
    for a in bit_attributes:
        df[a] = df[a].apply(replace_f_t_by_bit)

    for a in float_attributes + int_attributes:
        df[a] = df[a].apply(clean_float_and_int)

    return df

def cleanString(string):
    string = str(string)

    string = string.replace('\n', " ")

    #remove ' if surrounding the string
    if string != "":
        if string[0] == "'":
            string = string[1:]
        if string[-1] == "'":
            string = string[:-1]
        #put a quote before every quotes appearing in the string to escape it
        string = string.replace("''", "'")
        string = string.replace("'", "''")

        #add surrounding quotes
        string = "'" + string.strip() + "'"

    if string.lower() == "'nan'":
        string = "''"
    return string

def replace_f_t_by_bit(obj):
    f_t = str(obj)
    if(f_t == 't'):
        return 1
    return 0

def clean_float_and_int(a):
    a = str(a)
    a = a.replace("$", "")
    a = a.replace(",", "")
    return float(a)


def create_insert_queries(filenames_list):

    # city = filename.split(".")[-2].split("/")[-1].split("_")[0].lower().capitalize()
    # print(city)

    country_code_to_country_name_id = {"'ES'": "'Spain'", "'DE'": "'Germany'"}

    output_files = open_output_files(tables_to_attributes)

    # use something like INSERT INTO `BITTESTTABLE` VALUES('XYZ', b'0');
    # to insert bit values

    # use math.isnan(x) to check if float is NaN value before convert to int

    df = clean_listings_data(filenames_list)

    #First add all distincts normalization's tables' elements
    output_file = output_files["Property_type"]

    property_types = df["property_type"]
    property_types = property_types.drop_duplicates()
    cleaned = [cleanString(i) for i in property_types.tolist()]
    property_types_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in property_types_dict.keys():
        csv_line = """{},{}\n""".format(property_types_dict[typ], typ)
        output_file.write(csv_line)

    output_file = output_files["Room_type"]

    room_types = df["room_type"]
    room_types = room_types.drop_duplicates()
    cleaned = [cleanString(i) for i in room_types.tolist()]
    room_types_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in room_types_dict.keys():
        csv_line = """{},{}\n""".format(room_types_dict[typ], typ)
        output_file.write(csv_line)

    output_file = output_files["Bed_type"]

    bed_types = df["bed_type"]
    bed_types = bed_types.drop_duplicates()
    cleaned = [cleanString(i) for i in bed_types.tolist()]
    bed_types_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in bed_types_dict.keys():
        csv_line = """{},{}\n""".format(bed_types_dict[typ], typ)
        output_file.write(csv_line)

    output_file = output_files["Amenity"]

    amenities = df["amenities"]
    amenities = amenities.drop_duplicates()
    amenities_list = extract_amenities(amenities)
    amenities_dict = dict(list(zip(amenities_list, range(len(amenities_list)))))
    for amenity in amenities_dict.keys():
        csv_line = """{},{}\n""".format(amenities_dict[amenity], amenity)
        output_file.write(csv_line)

    output_file = output_files["Cancellation_policy"]

    cancellation_policy = df["cancellation_policy"]
    cancellation_policy = cancellation_policy.drop_duplicates()
    cleaned = [cleanString(i) for i in cancellation_policy.tolist()]
    cancellation_policy_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for typ in cancellation_policy_dict.keys():
        csv_line = """{},{}\n""".format(cancellation_policy_dict[typ], typ)
        output_file.write(csv_line)

    output_file = output_files["Host_verification"]

    host_verifications = df["host_verifications"]
    host_verifications = host_verifications.drop_duplicates()
    host_verifications_list = extract_host_verifications(host_verifications)
    host_verifications_dict = dict(list(zip(host_verifications_list, range(len(host_verifications_list)))))
    for typ in host_verifications_dict.keys():
        csv_line = """{},{}\n""".format(host_verifications_dict[typ], typ)
        output_file.write(csv_line)


    # insert country
    output_file = output_files["Country"]
    countries = df["country_code"]
    countries = countries.drop_duplicates()
    cleaned = [cleanString(i) for i in countries.tolist()]
    countries_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for ctry in countries_dict.keys():
        csv_line = """{},{},{}\n""".format(countries_dict[ctry], ctry, country_code_to_country_name_id[ctry])
        output_file.write(csv_line)

    # insert city
    output_file = output_files["City"]
    cities = df[["city", "country_code"]]
    cities = cities.drop_duplicates()
    cleaned = [(cleanString(i), cleanString(j)) for (i,j) in cities.values]
    cleaned_city = [i for (i,j) in cleaned]
    city_to_country = dict(cleaned)
    cities_dict = dict(list(zip(cleaned_city, range(len(cleaned)))))
    for city in cities_dict.keys():
        csv_line = """{},{},{}\n""".format(cities_dict[city], city, countries_dict[city_to_country[city]])
        output_file.write(csv_line)

    # insert Neighbourhood
    output_file = output_files["Neighbourhood"]
    neighbourhoods = df[["neighbourhood", "city"]].append(df[["host_neighbourhood", "city"]].rename(columns={"host_neighbourhood": "neighbourhood"}))
    neighbourhoods = neighbourhoods.drop_duplicates()
    cleaned = []
    for id, row in neighbourhoods.iterrows():
        new_pair = (cleanString(row["neighbourhood"]), cleanString(row["city"]))
        if(new_pair[0] != ''):
            cleaned.append(new_pair)
    neighbourhoods_dict = dict(list(zip(cleaned, range(len(cleaned)))))
    for n in neighbourhoods_dict.keys():
        csv_line = """{},{},{}\n""".format(neighbourhoods_dict[n], n[0], cities_dict[n[1]])
        output_file.write(csv_line)


    # insert Hosts
    output_file = output_files["Host"]
    hosts_attributes = list(tables_to_attributes["Host"].values())
    hosts_attributes.append("host_verifications")
    hosts_attributes.append("host_neighbourhood")
    hosts_attributes.append("city")
    hosts_attributes.remove("neighbourhood_id")
    hosts = df[hosts_attributes]
    hosts = remove_duplicated_hosts(hosts, tables_to_attributes, list(tables_to_attributes["Host"].values()))
    attr = tables_to_attributes["Host"]

    for idx, row in hosts.iterrows():
        host_id = int(row[attr["host_id"]])
        host_url = row[attr["host_url"]]
        host_name = row[attr["host_name"]]
        host_since = row[attr["host_since"]]
        host_about = row[attr["host_about"]]
        host_response_time = row[attr["host_response_time"]]
        host_response_rate = row[attr["host_response_rate"]]
        host_thumbnail_url = row[attr["host_thumbnail_url"]]
        host_picture_url = row[attr["host_picture_url"]]
        neighbourhood_id = neighbourhoods_dict[(cleanString(row["host_neighbourhood"]), cleanString(row["city"]))]

        host_verifications = row["host_verifications"]
        host_verifications = extract_host_verifications_from_string(host_verifications)

        output_file = output_files["Host"]
        csv_line = """{},{},{},{},{},{},{},{},{},{}\n""".format(\
                    host_id,\
                    host_url,\
                    host_name,\
                    host_since,\
                    host_about,\
                    host_response_time,\
                    host_response_rate,\
                    host_thumbnail_url,\
                    host_picture_url,\
                    neighbourhood_id)
        output_file.write(csv_line)

        output_file = output_files["Host_verification_map"]
        for hverf in host_verifications:
            csv_line = """{},{}\n""".format(host_id, host_verifications_dict[hverf])
            output_file.write(csv_line)

    # insert Listing
    output_file = output_files["Listing"]

    listings_atttributes = list(tables_to_attributes["Listing"].values())

    listings_atttributes.remove("neighbourhood_id")
    listings_atttributes.remove("property_type_id")
    listings_atttributes.remove("room_type_id")
    listings_atttributes.remove("bed_type_id")
    listings_atttributes.remove("cancellation_policy_id")

    normalized_attr = []
    normalized_attr.append("neighbourhood")
    normalized_attr.append("property_type")
    normalized_attr.append("room_type")
    normalized_attr.append("bed_type")
    normalized_attr.append("cancellation_policy")
    normalized_attr.append("amenities")

    listings_atttributes += normalized_attr

    listings_atttributes.append("city")
    listings = df[listings_atttributes]
    listings = listings.drop_duplicates()

    automatic_attributes = listings_atttributes
    # automatic_attributes -= normalized_attr

    attributes = tables_to_attributes["Listing"]

    for idx, row in listings.iterrows():
        output_file = output_files["Listing"]
        csv_line = ""
        listing_id = str(int(row["id"]))
        csv_line += listing_id + ","

        for att in ["listing_url", "listing_name", "listing_summary", "listing_space", \
                    "listing_description", "listing_notes", "listing_transit", "listing_access", \
                    "listing_interaction", "listing_picture_url", "listing_neighbourhood_overview"]:
            csv_line += row[attributes[att]] + ","

        for att in ["accommodates", "bathrooms", "bedrooms", "beds", "square_feet"]:
            a = row[attributes[att]]
            if not math.isnan(a):
                csv_line += str(int(a)) + ","
            else:
                csv_line += "NULL" + ","

        for att in ["price", "weekly_price", "monthly_price", "security_deposit", "cleaning_fee"]:
            a = row[attributes[att]]
            if not math.isnan(a):
                csv_line += str(a) + ","
            else:
                csv_line += "NULL" + ","

        for att in ["guests_included", "extra_people"]:
            a = row[attributes[att]]
            if not math.isnan(a):
                csv_line += str(int(a)) + ","
            else:
                csv_line += "NULL" + ","

        csv_line += row[attributes["rules"]] + ','

        for att in ["minimum_nights", "maximum_nights"]:
            a = row[attributes[att]]
            if not math.isnan(a):
                csv_line += str(int(a)) + ","
            else:
                csv_line += "NULL" + ","

        for att in ["is_business_travel_ready", "require_guest_profile_picture", "require_guest_phone_verification"]:
            a = row[attributes[att]]
            if not math.isnan(a):
                csv_line += str(int(a)) + ","
            else:
                csv_line += "NULL" + ","

        for att in ["review_scores_rating","review_scores_accuracy","review_scores_cleanliness",\
                    "review_scores_checkin","review_scores_communication","review_scores_location",\
                    "review_scores_value", "latitude", "longitude"]:
            a = row[attributes[att]]
            if not math.isnan(a):
                csv_line += str(a) + ","
            else:
                csv_line += "NULL" + ","

        csv_line += str(int(row[attributes["host_id"]])) + ","

        neighbourhood_id = neighbourhoods_dict[(cleanString(row["neighbourhood"]), cleanString(row["city"]))]
        csv_line += str(neighbourhood_id) + ","

        room_type_id = room_types_dict[cleanString(row["room_type"])]
        csv_line += str(room_type_id) + ","

        property_type_id = property_types_dict[cleanString(row["property_type"])]
        csv_line += str(property_type_id) + ","

        bed_type_id = bed_types_dict[cleanString(row["bed_type"])]
        csv_line += str(bed_type_id) + ","

        cancellation_policy_id = cancellation_policy_dict[cleanString(row["cancellation_policy"])]
        csv_line += str(cancellation_policy_id) + "\n"

        output_file.write(csv_line)

        # amenities
        output_file = output_files["Listing_amenity_map"]

        amenities = extract_amenities_from_string(row['amenities'])
        for a in amenities:
            csv_line = """{},{}\n""".format(listing_id, amenities_dict[a])
            output_file.write(csv_line)





    close_files(list(output_files.values()))


def remove_duplicated_hosts(hosts, tables_to_attributes, hosts_attributes):
    """
    hosts is a DataFrame containing Host's table columns
    """


    hosts = hosts.drop_duplicates()

    duplicates = hosts.duplicated("host_id", keep=False).tolist()
    duplicates = list(zip(range(len(duplicates)), duplicates))
    duplicates = [i for (i,j) in duplicates if j]
    duplicates_with_host_id = [(hosts[idx:idx+1]["host_id"].tolist()[0], idx) for idx in duplicates]

    duplicates_with_host_id.sort(key=lambda tup: tup[0])
    dupli_dict = {}
    for (id, i) in duplicates_with_host_id:
        if id not in dupli_dict:
            dupli_dict[id] = [i]
        else:
            dupli_dict[id] += [i]

    for id in dupli_dict.keys():
        indexes = dupli_dict[id]
        i1 = indexes[0]
        h1 = hosts[["host_id", "host_response_time", "host_response_rate"]][i1:i1+1]
        i2 = indexes[0]
        h2 = hosts[["host_id", "host_response_time", "host_response_rate"]][i2:i2+1]

        if h1["host_response_time"].tolist()[0] == '' or\
            h1["host_response_rate"].tolist()[0] == 'nan':
            to_drop = i1
        else:
            to_drop = i2

        hosts.drop(hosts.index[[to_drop, to_drop+1]])

    return hosts

def extract_amenities(amns):
    res = []
    for ams_str in amns:
        res += extract_amenities_from_string(ams_str)
    res = list(set(res))
    cleaned = []
    for am in res:
        if "translation missing:" not in am and am != "":
            cleaned.append(am)

    return cleaned

def extract_amenities_from_string(ams_str):
    ams_str = str(ams_str)
    ams = ams_str.split(",")
    ams = [a.replace("{", "") for a in ams]
    ams = [a.replace("}", "") for a in ams]
    ams = [a.replace('"', "") for a in ams]
    ams = [cleanString(i) for i in ams]
    ams = list(set(ams))
    cleaned = []
    for am in ams:
        if "translation missing:" not in am and am != "":
            cleaned.append(am)
    return cleaned

def extract_host_verifications(hvers):
    res = []
    for hvers_str in hvers:
        res += extract_host_verifications_from_string(hvers_str)
    res = list(set(res))
    cleaned = []
    for hverf in res:
        if hverf != "":
            cleaned.append(hverf)

    return cleaned

def extract_host_verifications_from_string(hvers_str):
    hvers_str = str(hvers_str)
    hverfs = hvers_str.split(",")
    hverfs = [a.replace("[", "") for a in hverfs]
    hverfs = [a.replace("]", "") for a in hverfs]
    hverfs = [a.replace("'", "") for a in hverfs]
    hverfs = [cleanString(i) for i in hverfs]

    hverfs = list(set(hverfs))
    cleaned = []
    for hverf in hverfs:
        if hverf != "":
            cleaned.append(hverf)
    return cleaned

def replace_elements(elmt, new_elmt_dict):
    return new_elmt_dict[elmt]

def create_output_csvs_if_not_exist(tables_to_attributes):
    for table in tables_to_attributes.keys():
        filename = "insert/"+table+".csv"
        try:
            file = open(filename, 'r')
        except:
            file = open(filename, 'w')
            s = ""
            for att in list(tables_to_attributes[table].keys()):
                s += att + ","
            s = s[:-1]
            s += "\n"
            file.write(s)
            file.close()
        else:
            file.close()

def open_output_files(tables_to_attributes):
    create_output_csvs_if_not_exist(tables_to_attributes)
    files = {}
    for table in tables_to_attributes.keys():
        filename = "insert/"+table+".csv"
        files[table] = open(filename, 'a')

    return files

def close_files(files):
    for f in files:
        f.close()
