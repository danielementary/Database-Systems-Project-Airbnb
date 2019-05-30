search_tables = ("Listing", "Host", "Neighbourhood")

select_property_type_names_ids_statements = """
SELECT property_type_name,
       property_type_id
FROM Property_type;"""

select_cancellation_policy_names_ids_statements = """
SELECT cancellation_policy_name,
       cancellation_policy_id
FROM Cancellation_policy;"""

select_city_names_ids_statements = """
SELECT city_name,
       city_id
FROM City;
"""

select_room_type_names_ids_statements = """
SELECT room_type_name,
       room_type_id
FROM Room_type;
"""

select_bed_type_names_ids_statements = """
SELECT bed_type_name,
       bed_type_id
FROM Bed_type;
"""

select_neighbourhood_names_ids_statements = """
SELECT neighbourhood_name,
       neighbourhood_id
FROM Neighbourhood
WHERE city_id = 0;
"""

select_neighbourhood_names_ids_for_city_id_statements = """
SELECT neighbourhood_name,
       neighbourhood_id
FROM Neighbourhood
WHERE city_id = {};
"""

select_listing_accomodates_min_max = """
SELECT MIN(accommodates),
       MAX(accommodates)
FROM Listing;
"""

select_listing_sqare_feet_min_max = """
SELECT MIN(square_feet),
       MAX(square_feet)
FROM Listing;
"""

select_listing_price_min_max = """
SELECT MIN(price), MAX(price)
FROM Listing;
"""

select_listing_review_score_rating_min_max = """
SELECT MIN(review_scores_rating), MAX(review_scores_rating)
FROM Listing;
"""

select_listing = """
SELECT listing_name,
       listing_url,
       accommodates,
       square_feet, price,
       review_scores_rating
FROM Listing
WHERE listing_name LIKE %s AND accommodates >= %s
                           AND square_feet  >= %s
                           AND price <= %s
                           AND is_business_travel_ready = %s
                           AND review_scores_rating >= %s
                           AND property_type_id = %s
                           AND cancellation_policy_id = %s;"""
select_host = """
SELECT host_name,
       host_since
FROM Host
WHERE host_name LIKE %s;
"""

select_neighbourhood = """
SELECT neighbourhood_name
FROM Neighbourhood
WHERE neighbourhood_name LIKE %s AND city_id = %s;"""

find_host = """
SELECT host_id
FROM Host
WHERE host_name = %s AND neighbourhood_id = %s
"""

find_neighbourhood = """
SELECT neighbourhood_id
FROM Neighbourhood
WHERE neighbourhood_name = %s AND city_id = %s;
"""

predefned_query_1 = """
SELECT AVG(price)
FROM Listing
WHERE beds = 8;
"""

predefned_query_2 = """
SELECT AVG(L.price)
FROM Listing L,
     Listing_amenity_map M
WHERE L.listing_id = M.listing_id
      AND M.amenity_id = (SELECT A.amenity_id
                          FROM Amenity A
                          WHERE A.amenity_name = "TV"
                          OR "Smart TV");
"""

predefned_query_3 = """
SELECT DISTINCT H.host_name
FROM Host H,
     Listing L,
     Day D,
     Calendar C
WHERE H.host_id = L.host_id
      AND L.listing_id = C.listing_id
      AND C.calendar_available = 1
      AND C.calendar_day_id = D.day_id
      AND D.day_date >= "2019-03-01"
      AND D.day_date < "2019-10-01";
"""

predefned_query_4 = """
SELECT COUNT(L1.listing_id)
FROM Listing L1,
     Listing L2,
     Host H1,
     Host H2
WHERE L1.host_id = H1.host_id
      AND L2.host_id = H2.host_id
      AND H1.host_id <> H2.host_id
      AND H1.host_name = H2.host_name;

"""

predefned_query_5 = """
SELECT DISTINCT D.day_date
FROM Day D,
     Calendar C,
     Listing L,
     Host H
WHERE D.day_id = C.calendar_day_id
      AND C.listing_id = L.listing_id
      AND C.calendar_available = 1
      AND L.host_id = H.host_id
      AND H.host_name = "Viajes Eco";
"""

predefned_query_6 = """
SELECT DISTINCT H.host_id, H.host_name
FROM Host H,
     Listing L
WHERE H.host_id = L.host_id
GROUP BY L.listing_id
HAVING COUNT(L.listing_id) = 1;
"""

predefned_query_7 = """
SELECT (AVG(L1.price) - AVG(L2.price))
FROM Listing L1,
     Listing L2,
     Listing_amenity_map M1,
     Listing_amenity_map M2,
WHERE L1.listing_id = M1.listing_id
      AND M1.amenity_id IN (SELECT A.amenity_id
                            FROM Amenity A
                            WHERE A.amenity_name = "Wifi"
                            OR A.amenity_name = "Pocket wifi")
      AND L2.listing_id = M2.listing_id
      AND M2.amenity_id NOT IN (SELECT A.amenity_id
                                FROM Amenity A
                                WHERE A.amenity_name = "Wifi"
                                OR A.amenity_name = "Pocket wifi");
"""

predefned_query_8 = """
SELECT AVG(L1.price) - AVG(L2.price)
FROM Listing L1,
     Listing L2
WHERE (L1.listing_id IN (SELECT L.listing_id
                        FROM Listing L,
                             Neighbourhood N,
                             City C
                        WHERE L.neighbourhood_id = N.neighbourhood_id
                        AND N.city_id = C.city_id
                        AND C.city_name = "Berlin"
                     ))
AND (L1.beds = 8)
AND (L2.listing_id IN (SELECT L.listing_id
                      FROM Listing L
                           Neighbourhood N,
                           City C
                      WHERE L.neighbourhood_id = N.neighbourhood_id
                      AND N.city_id = C.city_id
                      AND C.city_name = "Madrid"))
AND (L2.beds = 8);
"""

predefned_query_9 = """
SELECT H.host_id, H.host_name
FROM  Host H,
      Listing L,
      Neighbourhood N,
      City T,
      Country C
WHERE H.host_id = L.host_id
AND   N.city_id = T.city_id
AND   T.country_id = C.country_id
AND   C.country_name = "Spain"
GROUP BY L.listing_id
ORDER BY COUNT(*) DESC LIMIT 10;
"""

predefned_query_10 = """
SELECT L.listing_id, L.listing_name
FROM Listing L, Neighbourhood N, City C
WHERE L.neighbourhood_id = N.neighbourhood_id
AND   N.city_id = C.city_id
AND   C.city_name = "Barcelona"
ORDER BY L.review_scores_rating DESC LIMIT 10;
"""

predefined_queries = {"Predefined Query 1"  : predefned_query_1,
                      "Predefined Query 2"  : predefned_query_2,
                      "Predefined Query 3"  : predefned_query_3,
                      "Predefined Query 4"  : predefned_query_4,
                      "Predefined Query 5"  : predefned_query_5,
                      "Predefined Query 6"  : predefned_query_6,
                      "Predefined Query 7"  : predefned_query_7,
                      "Predefined Query 8"  : predefned_query_8,
                      "Predefined Query 9"  : predefned_query_9,
                      "Predefined Query 10" : predefned_query_10}
