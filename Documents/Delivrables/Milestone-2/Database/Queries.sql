-----------------query 01---------------------
SELECT AVG(price) AS price
FROM Listing
WHERE beds = 8;

-----------------query 02---------------------
SELECT AVG(L.price) AS price
FROM Listing L,
	Listing_amenity_map M
WHERE L.listing_id = M.listing_id
	AND M.amenity_id IN (
		SELECT DISTINCT amenity_id
		FROM Amenity
		WHERE amenity_name = "TV"
			OR amenity_name = "Smart TV"
		);

-----------------query 03---------------------
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

-----------------query 04---------------------
SELECT COUNT(L1.listing_id)
	Listing L2,
	Host H1,
	Host H2
WHERE L1.host_id = H1.host_id
	AND L2.host_id = H2.host_id
	AND H1.host_id <> H2.host_id
	AND H1.host_name = H2.host_name;

-----------------query 05---------------------
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

-----------------query 06---------------------
SELECT DISTINCT H.host_id,
	H.host_name
FROM Host H,
	Listing L
WHERE H.host_id = L.host_id
GROUP BY L.listing_id
HAVING COUNT(L.listing_id) = 1;

-----------------query 07---------------------
-- VERY expensive if we use the price in calendar, so we use listing.price because it is satisfying approximation and time goes from 442sec to 3sec
WITH amenities_wifi
AS (
	SELECT A.amenity_id
	FROM Amenity A
	WHERE A.amenity_name LIKE "%wifi%"
	),
prices
AS (
	SELECT avg(l.price) AS avg_price,
		(
			CASE
				WHEN lam.amenity_id IN (
						SELECT amenity_id
						FROM amenities_wifi
						)
					THEN 1
				ELSE 0
				END
			) AS wifi
	FROM Listing l,
		Listing_amenity_map lam

	WHERE l.listing_id = lam.listing_id
	GROUP BY wifi
	)
SELECT t1.avg_price - t2.avg_price as average_price_difference
FROM prices t1,
	prices t2
WHERE t1.wifi = 1
	AND t2.wifi = 0;


-----------------query 08---------------------
WITH 8 _beds_average_price
AS (
	SELECT avg(cal.calendar_price) AS avg_price,
		c.city_name
	FROM Listing l,
		Neighbourhood n,
		City c,
		Calendar cal
	WHERE cal.listing_id = l.listing_id
		AND cal.calendar_price IS NOT NULL
		AND l.beds = 8
		AND c.city_id = n.city_id
		AND n.neighbourhood_id = l.neighbourhood_id
	GROUP BY c.city_name
	)
SELECT t1.avg_price - t2.avg_price AS Berlin_minus_Madrid_8_beds_avg_price
FROM 8 _beds_average_price t1,
	8 _beds_average_price t2
WHERE t1.city_name = 'Berlin'
	AND t2.city_name = 'Madrid';

-----------------query 09---------------------
SELECT H.host_id,
	H.host_name
FROM Host H,
	Listing L,
	Neighbourhood N,
	City T,
	Country C
WHERE H.host_id = L.host_id
	AND N.city_id = T.city_id
	AND T.country_id = C.country_id
	AND C.country_name = "Spain"
GROUP BY L.listing_id
ORDER BY COUNT(*) DESC LIMIT 10;

-----------------query 10---------------------
SELECT L.listing_id,
	L.listing_name
FROM Listing L,
	Neighbourhood N,
	City C
WHERE L.neighbourhood_id = N.neighbourhood_id
	AND N.city_id = C.city_id
	AND C.city_name = "Barcelona"
ORDER BY L.review_scores_rating DESC LIMIT 10;
