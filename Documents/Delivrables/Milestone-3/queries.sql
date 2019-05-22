-- WARNIING !! when formatting, be sure that := have not a space in between. Formatter puts one but it does not work if so.
-- Query 1): number of hosts per city that put square_feet in their listing
SELECT COUNT(DISTINCT (h1.host_id)),
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
ORDER BY city_name;

-- Query 2): top 5 Neighbourhoods of Madrid based on median of review_scores_rating
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

-- Query 3): find hosts with higher number of listings
WITH hosts_with_number
AS (
	SELECT h.host_id,
		h.host_name,
		count(DISTINCT (l.listing_id)) AS number
	FROM Listing l,
		Host h
	WHERE h.host_id = l.host_id
	GROUP BY h.host_id
	ORDER BY number DESC
	),
highest_number
AS (
	SELECT number
	FROM hosts_with_number limit 1
	)
SELECT host_id,
	host_name
FROM hosts_with_number
WHERE number = (
		SELECT *
		FROM highest_number
		);

-- Query 4): 5 cheapest in Berlin with lots of specs
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


-- Query 5):
WITH listings_with_facilities
AS (
	SELECT l.listing_id,
		count(a.amenity_id) AS n_amenities,
		l.review_scores_rating, l.accommodates
	FROM Listing l,
		Amenity a,
		Listing_amenity_map lam
	WHERE l.listing_id = lam.listing_id
		AND a.amenity_id = lam.amenity_id
		AND a.amenity_name IN ('TV', 'Wifi', 'Internet', 'Free street parking')
	GROUP BY l.listing_id
	HAVING n_amenities >= 2
	)
SELECT l.listing_id,
	l.review_scores_value
FROM listings_with_facilities l
WHERE


-- Query 6): top three busiest listings per host
SELECT L.listing_name, H.host_name
FROM 	Listing L, Host H, Review R
WHERE L.host_id = H.host_id
AND R.listing_id = L.listing_id
GROUP BY H.host_id
ORDER BY COUNT(*) DESC LIMIT 3;
