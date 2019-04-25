#available fields for search section of the interface
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
