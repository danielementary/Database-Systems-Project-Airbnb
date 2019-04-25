search_tables = ("Listing", "Host", "Neighbourhood")

select_property_type_names_ids_statements       = "SELECT property_type_name, property_type_id from Property_type;"
select_cancellation_policy_names_ids_statements = "SELECT cancellation_policy_name, cancellation_policy_id from Cancellation_policy;"
select_city_names_ids_statements                = "SELECT city_name, city_id from City;"

select_listing_accomodates_min_max = """
SELECT MIN(accommodates), MAX(accommodates)
FROM Listing;"""
select_listing_sqare_feet_min_max = """
SELECT MIN(square_feet), MAX(square_feet)
FROM Listing;"""
select_listing_price_min_max = """
SELECT MIN(price), MAX(price)
FROM Listing;"""
select_listing_review_score_rating_min_max = """
SELECT MIN(review_scores_rating), MAX(review_scores_rating)
FROM Listing;"""

select_listing = """
SELECT listing_name, listing_url, accommodates, square_feet, price, review_scores_rating
FROM Listing
WHERE listing_name LIKE %s and accommodates >= %s
                           and square_feet  >= %s
                           and price <= %s
                           and is_business_travel_ready = %s
                           and review_scores_rating >= %s
                           and property_type_id = %s
                           and cancellation_policy_id = %s;"""
select_host = """
SELECT host_name, host_since
FROM Host
WHERE host_name LIKE %s;"""

select_neighbourhood = """
SELECT neighbourhood_name
FROM Neighbourhood
WHERE neighbourhood_name LIKE %s and city_id = %s;"""

predefned_query_1 = """
SELECT AVG(price)
FROM Listing
WHERE beds = 8;
"""

predefned_query_2 = """
SELECT AVG(L.price)
FROM  Listing L, Listing_amenity_map M
WHERE L.listing_id = M.listing_id
      AND L.amenities_id EXISTS ( SELECT A.amenities_id
                                  FROM Amenities A
                                  WHERE A.amenities = 'TV'
                                );
"""

predefned_query_3 = """
SELECT * FROM City;
"""

predefned_query_4 = """
SELECT * FROM City;
"""

predefned_query_5 = """
SELECT * FROM City;
"""

predefned_query_6 = """
SELECT * FROM City;
"""

predefned_query_7 = """
SELECT * FROM City;
"""

predefned_query_8 = """
SELECT * FROM City;
"""

predefned_query_9 = """
SELECT * FROM City;
"""

predefned_query_10 = """
SELECT * FROM City;
"""

predefined_queries = {"Predefined Query 1" : predefned_query_1, "Predefined Query 2" : predefned_query_2, "Predefined Query 3" : predefned_query_3,
                      "Predefined Query 4" : predefned_query_4, "Predefined Query 5" : predefned_query_5, "Predefined Query 6" : predefned_query_6,
                      "Predefined Query 7" : predefned_query_7, "Predefined Query 8" : predefned_query_8, "Predefined Query 9" : predefned_query_9,
                      "Predefined Query 10" : predefned_query_10}
