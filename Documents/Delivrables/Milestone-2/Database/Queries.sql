---------------------01-----------------------
SELECT AVG(price)
FROM Listing
WHERE beds = 8;

---------------------02-----------------------
--answer :  104.67844896768075

SELECT AVG(L.price)
FROM Listing L,
     Listing_amenity_map M
WHERE L.listing_id = M.listing_id
AND M.amenity_id IN ( SELECT DISTINCT amenity_id
                      FROM Amenity
                      WHERE amenity_name = "TV"
                      OR amenity_name = "Smart TV");

---------------------03-----------------------
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

---------------------04-----------------------
--to check this one
--answer : 1930788
SELECT COUNT(L1.listing_id)
FROM Listing L1,
     Listing L2,
     Host H1,
     Host H2
WHERE L1.host_id = H1.host_id
      AND L2.host_id = H2.host_id
      AND H1.host_id <> H2.host_id
      AND H1.host_name = H2.host_name;

---------------------05-----------------------
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

---------------------06-----------------------
SELECT DISTINCT H.host_id, H.host_name
FROM Host H,
     Listing L
WHERE H.host_id = L.host_id
GROUP BY L.listing_id
HAVING COUNT(L.listing_id) = 1;

---------------------07-----------------------
--c'est faux
--with wifi : 85.73360122916912

SELECT AVG(L1.price) - AVG(L2.price)
FROM Listing L1,
     Listing L2,
     Listing_amenity_map M1,
     Listing_amenity_map M2,
WHERE (L1.listing_id = M1.listing_id)
      AND (M1.amenity_id IN (SELECT A.amenity_id
                             FROM Amenity A
                             WHERE A.amenity_name = "Wifi"
                             OR A.amenity_name = "Pocket wifi"))
      AND (L2.listing_id = M2.listing_id)
      AND M2.amenity_id NOT IN (SELECT A.amenity_id
                                FROM Amenity A
                                WHERE A.amenity_name = "Wifi"
                                OR A.amenity_name = "Pocket wifi");

---------------------08-----------------------
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

---------------------09-----------------------
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


---------------------10-----------------------
SELECT L.listing_id, L.listing_name
FROM Listing L, Neighbourhood N, City C
WHERE L.neighbourhood_id = N.neighbourhood_id
AND   N.city_id = C.city_id
AND   C.city_name = "Barcelona"
ORDER BY L.review_scores_rating DESC LIMIT 10;
