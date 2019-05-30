-----------------query 01---------------------
SELECT COUNT(DISTINCT (h1.host_id)) AS number_of_hosts,
	city_name
FROM Host h1,
	Listing l1,
	Neighbourhood n1,
	City c1
WHERE l1.host_id = h1.host_id
	AND l1.neighbourhood_id = n1.neighbourhood_id
	AND n1.city_id = c1.city_id
	AND h1.host_id IN (
		SELECT h2.host_id
		FROM Host h2,
			Listing l2
		WHERE l2.host_id = h2.host_id
			AND l2.square_feet IS NOT NULL
		)
GROUP BY city_name
ORDER BY city_name ASC;


-----------------query 02---------------------
WITH subtable
AS (
	SELECT @row := @row + 1 AS rownum,
		review_scores_rating,
		listing_id,
		n.neighbourhood_id,
		n.neighbourhood_name
	FROM Listing l,
		Neighbourhood n,
		City c,
		(
			SELECT @row := 0
			) r
	WHERE l.neighbourhood_id = n.neighbourhood_id
		AND n.city_id = n.city_id
		AND c.city_name = 'Madrid'
		AND l.review_scores_rating IS NOT NULL
	ORDER BY n.neighbourhood_id,
		review_scores_rating ASC
	),
rownumbers
AS (
	SELECT Floor(Sum(rownum) / 2)
	FROM subtable
	GROUP BY neighbourhood_id
	)
SELECT subtable.neighbourhood_name,
	subtable.review_scores_rating
FROM subtable
WHERE subtable.rownum IN (
		SELECT *
		FROM rownumbers
		)
ORDER BY subtable.review_scores_rating DESC LIMIT 5;



-----------------query 03---------------------

SELECT h.host_id,
	h.host_name,
	count(DISTINCT (l.listing_id)) AS number_of_listings
FROM Listing l,
	Host h
WHERE h.host_id = l.host_id
GROUP BY h.host_id
ORDER BY number DESC LIMIT 1;



-----------------query 04---------------------
SELECT l.listing_id,
	avg(cal.calendar_price) AS price
FROM Listing l,
	Calendar cal,
	Neighbourhood n,
	City c,
	Day d,
	Cancellation_policy cp,
	Host h,
	Host_verification hv,
	Host_verification_map hvm
WHERE l.neighbourhood_id = n.neighbourhood_id
	AND n.city_id = c.city_id
	AND c.city_name = 'Berlin'
	AND cal.listing_id = l.listing_id
	AND cal.calendar_day_id = d.day_id
	AND d.day_date >= '2019-03-01'
	AND d.day_date <= '2019-04-30'
	AND cal.calendar_available = (1)
	AND l.beds >= 2
	AND l.cancellation_policy_id = cp.cancellation_policy_id
	AND cp.cancellation_policy_name = 'flexible'
	AND l.review_scores_location >= 8
	AND h.host_id = l.host_id
	AND h.host_id = hvm.host_id
	AND hv.host_verification_id = hvm.host_verification_id
	AND hv.host_verification_description = 'government_id'
GROUP BY l.listing_id
ORDER BY price ASC LIMIT 5;



-----------------query 05---------------------
WITH listings_with_facilities
AS (
	SELECT l.listing_id,
		count(a.amenity_id) AS n_amenities,
		l.review_scores_rating,
		l.accommodates
	FROM Listing l,
		Amenity a,
		Listing_amenity_map lam
	WHERE l.listing_id = lam.listing_id
		AND a.amenity_id = lam.amenity_id
		AND a.amenity_name IN ('TV', 'Wifi', 'Internet', 'Free street parking')
	GROUP BY l.listing_id
	HAVING n_amenities >= 2
	),
accommodates
AS (
	SELECT DISTINCT (l.accommodates) AS accom
	FROM Listing l
	)
SELECT l1.listing_id,
	l1.review_scores_rating,
	a.accom
FROM Listing l1,
	accommodates a
WHERE l1.listing_id IN (
		SELECT *
		FROM (
			SELECT listing_id
			FROM listings_with_facilities lwf
			WHERE lwf.accommodates = accom
			ORDER BY lwf.review_scores_rating DESC LIMIT 5
			) listings_per_accomodates
		)
ORDER BY a.accom;


-----------------query 06---------------------
WITH listings_with_number_reviews
AS (
	SELECT l.listing_id,
		l.host_id,
		count(DISTINCT (r.review_id)) AS n_reviews
	FROM Listing l,
		Review r
	WHERE l.listing_id = r.listing_id
	GROUP BY l.listing_id
	ORDER BY l.host_id,
		n_reviews DESC
	)
SELECT h.host_id,
	GROUP_CONCAT(l.listing_id SEPARATOR ', ') AS listing_ids,
	GROUP_CONCAT(l.n_reviews SEPARATOR ', ') AS n_reviews_per_listing
FROM listings_with_number_reviews l,
	(
		SELECT DISTINCT (host_id) AS host_id
		FROM Host
		) h
WHERE l.listing_id IN (
		SELECT *
		FROM (
			SELECT listing_id
			FROM listings_with_number_reviews l2
			WHERE l2.host_id = h.host_id LIMIT 3
			) z
		)
GROUP BY h.host_id;


-----------------query 07---------------------
WITH amenity_per_neigh_w_listings_n
AS (
	SELECT a.amenity_id,
		a.amenity_name,
		l.neighbourhood_id,
		n.neighbourhood_name,
		COUNT(DISTINCT (l.listing_id)) AS listings_number
	FROM Listing l,
		Room_type rt,
		Amenity a,
		Listing_amenity_map lam,
		Neighbourhood n,
		City c
	WHERE l.room_type_id = rt.room_type_id
		AND rt.room_type_name = 'Private room'
		AND a.amenity_id = lam.amenity_id
		AND lam.listing_id = l.listing_id
		AND l.neighbourhood_id = n.neighbourhood_id
		AND n.city_id = c.city_id
		AND c.city_name = 'Berlin'
	GROUP BY a.amenity_id,
		l.neighbourhood_id
	ORDER BY l.neighbourhood_id,
		listings_number DESC
	)
SELECT apn.neighbourhood_name,
	GROUP_CONCAT(ame.amenity_name SEPARATOR ', ') as amenities
FROM Amenity ame,
	amenity_per_neigh_w_listings_n apn
WHERE ame.amenity_id = apn.amenity_id
	AND ame.amenity_id IN (
		SELECT *
		FROM (
			SELECT amenity_id
			FROM amenity_per_neigh_w_listings_n apn2
			WHERE apn.neighbourhood_id = apn2.neighbourhood_id LIMIT 3
			) z
		)
GROUP BY apn.neighbourhood_id;



-----------------query 08---------------------
WITH host_id_with_n_verf
AS (
	SELECT host_id,
		count(DISTINCT (host_verification_id)) AS n_verf
	FROM Host_verification_map
	GROUP BY host_id
	)
SELECT (
		(
			SELECT avg(l.review_scores_communication)
			FROM Listing l
			WHERE l.host_id IN (
					SELECT *
					FROM (
						SELECT host_id
						FROM host_id_with_n_verf
						ORDER BY n_verf DESC limit 1
						) z
					)
			) - (
			SELECT avg(l.review_scores_communication)
			FROM Listing l
			WHERE l.host_id IN (
					SELECT *
					FROM (
						SELECT host_id
						FROM host_id_with_n_verf
						ORDER BY n_verf ASC limit 1
						) z
					)
			)
		) AS average_difference;



-----------------query 09---------------------
SELECT c1.city_name,
	total_reviews
FROM City c1,
	(
		SELECT city_id,
			sum(n_reviews) AS total_reviews
		FROM (
			SELECT l.room_type_id,
				c.city_id,
				c.city_name,
				avg(l.accommodates) AS avg_acc,
				count(DISTINCT (r.review_id)) AS n_reviews
			FROM Listing l,
				City c,
				Neighbourhood n,
				Review r
			WHERE n.neighbourhood_id = l.neighbourhood_id
				AND c.city_id = n.city_id
				AND r.listing_id = l.listing_id
			GROUP BY l.room_type_id,
				c.city_id
			) per_room_type
		WHERE avg_acc >= 3
		GROUP BY city_id
		) total_reviews_per_city
WHERE c1.city_id = total_reviews_per_city.city_id
ORDER BY total_reviews DESC LIMIT 1;


-----------------query 10---------------------
SELECT neigh_n_occupied.neighbourhood_name
FROM (
	SELECT n1.neighbourhood_name,
		n1.neighbourhood_id,
		count(DISTINCT (listing_id)) AS n_occupied
	FROM Neighbourhood n1,
		(
			SELECT l.listing_id,
				l.host_id,
				l.neighbourhood_id,
				SUM(CASE
						WHEN cal.calendar_available = (0)
							THEN 1
						WHEN cal.calendar_available = (1)
							THEN 0
						ELSE 0
						END) AS n_occupied_days
			FROM Listing l,
				Calendar cal,
				Day d,
				Neighbourhood n,
				City c,
				Host h
			WHERE l.neighbourhood_id = n.neighbourhood_id
				AND n.city_id = c.city_id
				AND c.city_name = 'Madrid'
				AND cal.listing_id = l.listing_id
				AND cal.calendar_day_id = d.day_id
				AND d.day_date >= '2019-01-01'
				AND d.day_date <= '2019-12-31'
				AND h.host_id = l.host_id
				AND h.host_since <= '2017-06-01'
			GROUP BY l.listing_id,
				l.host_id
			) listings_occupied_days
	WHERE n1.neighbourhood_id = listings_occupied_days.neighbourhood_id
		AND n_occupied_days > 0
	GROUP BY n1.neighbourhood_name,
		n1.neighbourhood_id
	) neigh_n_occupied
WHERE neigh_n_occupied.n_occupied / (
		SELECT count(DISTINCT (l1.listing_id))
		FROM Listing l1
		WHERE l1.neighbourhood_id = neigh_n_occupied.neighbourhood_id
	) >= 0.5;



-----------------query 11---------------------
SELECT DISTINCT (country_name)
FROM (
	SELECT ctry.country_id,
		ctry.country_name,
		d.day_date,
		SUM(CASE
				WHEN cal.calendar_available = (1)
					THEN 1
				WHEN cal.calendar_available = (0)
					THEN 0
				ELSE 0
				END) AS n_available
	FROM Country ctry,
		Calendar cal,
		Day d,
		Listing l,
		Neighbourhood n,
		City c
	WHERE cal.calendar_day_id = d.day_id
		AND cal.listing_id = l.listing_id
		AND l.neighbourhood_id = n.neighbourhood_id
		AND c.city_id = n.city_id
		AND c.country_id = ctry.country_id
		AND d.day_date >= '2018-01-01'
		AND d.day_date <= '2018-12-31'
	GROUP BY ctry.country_id,
		ctry.country_name,
		d.day_date
	) subtable
WHERE subtable.n_available / (
		SELECT count(DISTINCT (listing_id))
		FROM Listing l,
			Neighbourhood n,
			City c,
			Country ct
		WHERE l.neighbourhood_id = n.neighbourhood_id
			AND n.city_id = c.city_id
			AND c.country_id = ct.country_id
			AND ct.country_id = subtable.country_id
		) >= 0.2;



-----------------query 12---------------------
SELECT subtable.neighbourhood_name,
	subtable.n_strict_grace / total_list_per_neigh.n_listings as strict_over_all_ratio
FROM (
	SELECT n.neighbourhood_id,
		n.neighbourhood_name,
		count(DISTINCT (l.listing_id)) AS n_strict_grace
	FROM Neighbourhood n,
		Listing l,
		City c,
		Cancellation_policy cp
	WHERE n.neighbourhood_id = l.neighbourhood_id
		AND n.city_id = c.city_id
		AND l.cancellation_policy_id = cp.cancellation_policy_id
		AND cp.cancellation_policy_name = 'strict_14_with_grace_period'
		AND c.city_name = 'Barcelona'
	GROUP BY n.neighbourhood_id
	) subtable,
	(
		SELECT count(DISTINCT (l.listing_id)) AS n_listings,
			n.neighbourhood_id
		FROM Listing l,
			Neighbourhood n,
			City c
		WHERE n.neighbourhood_id = l.neighbourhood_id
			AND n.city_id = c.city_id
			AND c.city_name = 'Barcelona'
		GROUP BY n.neighbourhood_id
		) total_list_per_neigh
WHERE n_strict_grace / total_list_per_neigh.n_listings >= 0.05
	AND subtable.neighbourhood_id = total_list_per_neigh.neighbourhood_id;
