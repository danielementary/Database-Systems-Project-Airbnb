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
"""

predefned_query_2 = """
"""

predefned_query_3 = """
"""

predefned_query_4 = """
"""

predefned_query_5 = """
"""

predefned_query_6 = """
"""

predefned_query_7 = """
"""

predefned_query_8 = """
"""

predefned_query_9 = """
"""

predefned_query_10 = """
"""

predefined_queries = [predefned_query_1, predefned_query_2, predefned_query_3,
                      predefned_query_4, predefned_query_5, predefned_query_6,
                      predefned_query_7, predefned_query_8, predefned_query_9,
                      predefned_query_10]
