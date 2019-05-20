-- Query 1): number of hosts per city that put square_feet in their listing
SELECT count(DISTINCT (Host.host_id)),
	city_name
FROM Host,
	Listing,
	Neighbourhood,
	City
WHERE Listing.host_id = Host.host_id
	AND Listing.neighbourhood_id = Neighbourhood.neighbourhood_id
	AND Neighbourhood.city_id = City.city_id
	AND Host.host_id IN (
		SELECT Host.host_id
		FROM Host,
			Listing
		WHERE Listing.host_id = Host.host_id
			AND square_feet IS NOT NULL
		)
GROUP BY city_name
ORDER BY city_name;

-- Query 2): top 5 Neighbourhoods of Madrid based on median of review_scores_rating
WITH subtable
AS (
	SELECT @row:= @row + 1 AS rownum,
		review_scores_rating,
		listing_id,
		n.neighbourhood_id,
		n.neighbourhood_name
	FROM Listing l,
		Neighbourhood n,
		City c,
		(
			SELECT @row:= 0
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
ORDER BY subtable.review_scores_rating DESC Limit 5
