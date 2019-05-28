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