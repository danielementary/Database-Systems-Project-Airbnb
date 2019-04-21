#available fields for search section of the interface
search_fields = {"Listing": ("listing_name", "accommodates", "square_feet",
                             "price", "is_business_travel_ready",
                             "review_scores_rating", "property_type_id",
                             "cancellation_policy_id"),
                 "Host" : ("host_name", "host_since"),
                 "Neighbourhood" : ("neighbourhood_name", "city_id")
                 }

#mapping from field to input type : 0 text, 1 number, 2 range, 3 boolean,
# 4 option menu
map_fields_input = {"listing_name": 0,
                    "accommodates": 1,
                    "square_feet" : 2,
                    "price"       : 2,
                    "is_business_travel_ready" : 3,
                    "review_scores_rating"     : 2,
                    "property_type_id"         : 4,
                    "cancellation_policy_id"   : 4,
                    "host_name"  : 0,
                    "host_since" : 1,
                    "neighbourhood_name" : 0,
                    "city_id"     : 4}
